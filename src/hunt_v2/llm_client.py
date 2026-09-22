# -*- coding: utf-8 -*-
"""LLM client cho V2 (guide §23–§27): routing theo config/models.yaml, chain fallback,
retry, JSON repair, schema validate, cache SQLite, log JSONL, token usage, latency.

Mỗi call trả LlmResult đầy đủ raw/parsed/error — KHÔNG bao giờ nuốt lỗi thành {} như
reup_filter.classify cũ. Cache key = sha256(video_ids + lane_hash + gate + prompt_version + model).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path

from hunt_v2 import llm_transport as tr
from hunt_v2 import schemas

CACHE_SCHEMA = """
CREATE TABLE IF NOT EXISTS llm_cache(
  key TEXT PRIMARY KEY, gate TEXT, model TEXT, prompt_version TEXT,
  payload TEXT, created TEXT);
"""


@dataclass
class LlmResult:
    gate: str
    model: str = ""
    provider: str = ""
    latency_ms: int = 0
    attempt: int = 0
    raw_response: str = ""
    parsed_response: object = None
    cached: bool = False
    error: str | None = None
    usage: dict = field(default_factory=dict)
    schema_errors: list = field(default_factory=list)
    fallback_used: bool = False

    @property
    def ok(self) -> bool:
        return self.error is None and self.parsed_response is not None


class LlmClient:
    def __init__(self, models_cfg: dict, con: sqlite3.Connection | None, log_dir: str | Path,
                 lane_fingerprint: str = ""):
        self.cfg = models_cfg
        self.con = con
        if con is not None:
            con.executescript(CACHE_SCHEMA)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.lane_fp = lane_fingerprint
        self.stats = {"calls": 0, "cached": 0, "errors": 0, "prompt_tokens": 0,
                      "completion_tokens": 0, "latency_ms": 0}

    # ---------- cache ----------
    def cache_key(self, gate: str, model: str, ids: list[str]) -> str:
        pv = self.cfg["gates"][gate]["prompt_version"]
        raw = "|".join(sorted(ids)) + "|" + self.lane_fp + "|" + gate + "|" + pv + "|" + model
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _cache_get(self, key: str):
        if self.con is None:
            return None
        row = self.con.execute("SELECT payload FROM llm_cache WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def _cache_put(self, key: str, gate: str, model: str, payload) -> None:
        if self.con is None:
            return
        self.con.execute("INSERT OR REPLACE INTO llm_cache VALUES(?,?,?,?,?,?)",
                         (key, gate, model, self.cfg["gates"][gate]["prompt_version"],
                          json.dumps(payload, ensure_ascii=False), dt.datetime.now().isoformat()))
        self.con.commit()

    # ---------- log ----------
    def _log(self, res: LlmResult, ids: list[str]) -> None:
        rec = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "gate": res.gate,
               "provider": res.provider, "model": res.model, "latency_ms": res.latency_ms,
               "attempt": res.attempt, "cached": res.cached, "error": res.error,
               "schema_errors": res.schema_errors[:5], "usage": res.usage, "n_ids": len(ids),
               "raw_head": res.raw_response[:300]}
        with open(self.log_dir / f"llm_{dt.date.today().strftime('%Y%m%d')}.jsonl", "a",
                  encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---------- gọi ----------
    def call(self, gate: str, prompt: str, ids: list[str], schema_name: str | None,
             expect_list: bool = False, system: str | None = None, use_cache: bool = True) -> LlmResult:
        """`ids` = video_id trong lô (để làm cache key). `schema_name` ∈ schemas.SCHEMAS.
        `expect_list=True` → output là list object, validate từng phần tử."""
        g = self.cfg["gates"][gate]
        chain = [tuple(x) for x in g["chain"]]
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": prompt}]
        res = LlmResult(gate=gate)
        key = self.cache_key(gate, chain[0][1], ids)
        if use_cache:
            hit = self._cache_get(key)
            if hit is not None:
                res.cached, res.parsed_response = True, hit
                res.provider, res.model = chain[0]
                self.stats["cached"] += 1
                self._log(res, ids)
                return res

        last_err = None
        for idx, (prov_name, model) in enumerate(chain):
            prov = self.cfg["providers"][prov_name]
            for attempt in range(1, 3):
                t0 = time.time()
                res.attempt += 1
                res.provider, res.model, res.fallback_used = prov_name, model, idx > 0
                try:
                    if prov["kind"] == "claude_cli":
                        text, usage = tr.chat_claude_cli(prov, model, messages, g["timeout_s"])
                    else:
                        text, usage = tr.chat_http(prov, model, messages, g["timeout_s"],
                                                   g.get("max_tokens", 2000),
                                                   g.get("temperature", 0.1))
                except tr.TransportError as e:
                    last_err = f"{prov_name}:{model} lần {attempt}: {e}"
                    time.sleep(min(2 ** attempt, 8))
                    continue
                res.latency_ms = int((time.time() - t0) * 1000)
                res.raw_response, res.usage = text, usage or {}
                self.stats["calls"] += 1
                self.stats["latency_ms"] += res.latency_ms
                self.stats["prompt_tokens"] += int(res.usage.get("prompt_tokens") or 0)
                self.stats["completion_tokens"] += int(res.usage.get("completion_tokens") or 0)
                parsed = tr.repair_json(text)
                if parsed is None:
                    last_err = f"{prov_name}:{model}: không parse được JSON"
                    continue
                res.parsed_response = parsed
                if schema_name:
                    res.schema_errors = _validate(schema_name, parsed, expect_list)
                if use_cache and not res.schema_errors:
                    self._cache_put(key, gate, model, parsed)
                self._log(res, ids)
                return res
        res.error = last_err or "hết chain"
        self.stats["errors"] += 1
        self._log(res, ids)
        return res


def _validate(schema_name: str, parsed, expect_list: bool) -> list[str]:
    if expect_list:
        if not isinstance(parsed, list):
            return ["output không phải list"]
        errs = []
        for i, item in enumerate(parsed):
            errs += [f"[{i}] {e}" for e in schemas.validate(schema_name, item)]
        return errs
    return schemas.validate(schema_name, parsed)
