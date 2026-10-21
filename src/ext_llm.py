# -*- coding: utf-8 -*-
"""Cửa chung gọi model NGOÀI (deepseek / Sol / gemini qua ns24, ramclouds, hhtech) để tiết kiệm quota Claude.

Anh duyệt 21/10/2026. Mọi tool đọc nhiều / viết nháp gọi qua đây thay vì để Claude đọc thẳng:
  ask_json(gate, prompt, ids)  → LlmClient của hunt_v2 (chain fallback, cầu dao, cache SQLite, log JSONL)
  ask_text(gate, prompt)       → chuỗi văn bản (nháp markdown), cùng chain, có log
Gate + model khai ở config/models.yaml (`ext_*`). Từ 21/10 (anh duyệt phương án 4) chạy chính là
Haiku/Sonnet 5.5 trong gói Claude qua provider `claude_lite` (claude -p gọn: không tool/MCP/CLAUDE.md,
tên model đầy đủ, effort theo gate); ns24 chỉ dự phòng. Gate ext_* CẤM claude_cli không gọn.
Cache key của LlmClient không chứa prompt (bẫy 17/10) → ask_json tự gắn hash prompt vào ids.
Mỗi lượt ghi 1 dòng logs/ext_llm_usage.jsonl để so quota trước/sau.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sqlite3
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

from hunt_v2 import llm_transport as tr
from hunt_v2.llm_client import LlmClient, LlmResult

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
load_dotenv(ROOT / "config" / ".env")
_client: LlmClient | None = None


def models_cfg() -> dict:
    return yaml.safe_load((ROOT / "config" / "models.yaml").read_text(encoding="utf-8"))


def client() -> LlmClient:
    global _client
    if _client is None:
        con = sqlite3.connect(ROOT / "data" / "ext_llm_cache.db")
        _client = LlmClient(models_cfg(), con, LOGS)
    return _client


def _usage_log(gate: str, model: str, usage: dict, ok: bool, ms: int, note: str = "") -> None:
    LOGS.mkdir(exist_ok=True)
    rec = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "gate": gate, "model": model, "ok": ok,
           "ms": ms, "prompt_tokens": int(usage.get("prompt_tokens") or 0),
           "completion_tokens": int(usage.get("completion_tokens") or 0), "note": note[:160]}
    with open(LOGS / "ext_llm_usage.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def ask_json(gate: str, prompt: str, ids=(), system: str | None = None, use_cache: bool = True) -> LlmResult:
    """Trả LlmResult (res.ok, res.parsed_response, res.model, res.error). Không ném lỗi."""
    ph = hashlib.sha256(((system or "") + prompt).encode("utf-8")).hexdigest()[:16]
    t0 = time.time()
    res = client().call(gate, prompt, list(ids) + [f"p:{ph}"], None, system=system, use_cache=use_cache)
    _usage_log(gate, res.model, res.usage, res.ok, int((time.time() - t0) * 1000),
               "cache" if res.cached else (res.error or ""))
    return res


def ask_text(gate: str, prompt: str, system: str | None = None) -> tuple[str, str]:
    """Trả (văn_bản, model). Hết chain → RuntimeError kèm lý do từng model."""
    cfg = models_cfg()
    g = cfg["gates"][gate]
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    errs = []
    for prov_name, model in g["chain"]:
        prov = cfg["providers"][prov_name]
        if prov["kind"] == "claude_cli" and not prov.get("lite"):
            errs.append(f"{prov_name}: bỏ qua (claude -p không gọn)")
            continue
        t0 = time.time()
        try:
            if prov["kind"] == "claude_cli":
                text, usage = tr.chat_claude_cli(prov, model, msgs, g["timeout_s"], g.get("effort"))
            else:
                text, usage = tr.chat_http(prov, model, msgs, g["timeout_s"], g.get("max_tokens", 4000),
                                           g.get("temperature", 0.3))
        except tr.TransportError as e:
            errs.append(f"{prov_name}/{model}: {e}")
            _usage_log(gate, model, {}, False, int((time.time() - t0) * 1000), str(e))
            continue
        _usage_log(gate, model, usage or {}, True, int((time.time() - t0) * 1000))
        return text, f"{prov_name}/{model}"
    raise RuntimeError(f"{gate}: hết chain — " + " | ".join(errs))


def usage_summary(since: str | None = None) -> dict:
    """Tổng token model ngoài theo gate (để báo cáo quota)."""
    out: dict[str, dict] = {}
    p = LOGS / "ext_llm_usage.jsonl"
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if since and r["ts"] < since:
            continue
        s = out.setdefault(r["gate"], {"calls": 0, "fail": 0, "prompt_tokens": 0, "completion_tokens": 0})
        s["calls"] += 1
        s["fail"] += 0 if r["ok"] else 1
        s["prompt_tokens"] += r["prompt_tokens"]
        s["completion_tokens"] += r["completion_tokens"]
    return out


if __name__ == "__main__":
    import sys
    for gate, s in usage_summary(sys.argv[1] if len(sys.argv) > 1 else None).items():
        print(f"{gate:14s} {s['calls']:4d} lượt · lỗi {s['fail']} · in {s['prompt_tokens']:,} · out {s['completion_tokens']:,}")
