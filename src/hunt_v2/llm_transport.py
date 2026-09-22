# -*- coding: utf-8 -*-
"""Tầng vận chuyển cho llm_client: HTTP OpenAI-compatible (stream/non-stream) + `claude -p`.

Luật rút từ h2dev/pipeline/llm_client.py (đã trả giá thật):
- ramclouds/ns24 BẮT BUỘC stream:true (non-stream trả 200 + SSE rỗng, mất trắng nội dung)
- BẮT BUỘC User-Agent (thiếu → Cloudflare 403 code 1010)
- lỗi upstream có thể về DƯỚI DẠNG NỘI DUNG ("[Codex error: ...]") → quét chuỗi
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
_UPSTREAM_ERR = re.compile(r"\[(Codex|Upstream|Provider) error", re.I)


class TransportError(RuntimeError):
    """Lỗi mạng/HTTP/proc — caller đổi provider trong chain."""


def chat_http(prov: dict, model: str, messages: list[dict], timeout: int,
              max_tokens: int, temperature: float) -> tuple[str, dict]:
    key = os.getenv(prov["key_env"], "")
    if not key:
        raise TransportError(f"thiếu env {prov['key_env']}")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if prov.get("user_agent"):
        headers["User-Agent"] = UA
    body = {"model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature}
    if prov.get("stream"):
        body["stream"] = True
        body["stream_options"] = {"include_usage": True}
        headers["Accept"] = "text/event-stream"
    try:
        r = requests.post(f"{prov['base_url']}/chat/completions", headers=headers, json=body,
                          timeout=timeout, stream=bool(prov.get("stream")))
    except requests.RequestException as e:
        raise TransportError(f"{type(e).__name__}: {str(e)[:120]}") from e
    if r.status_code != 200:
        raise TransportError(f"HTTP {r.status_code}: {r.text[:200]}")
    if prov.get("stream"):
        text, usage = _read_sse(r)
    else:
        data = r.json()
        try:
            text = data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as e:
            raise TransportError(f"body lạ: {str(data)[:200]}") from e
        usage = data.get("usage") or {}
    if not text.strip():
        raise TransportError("nội dung rỗng")
    if _UPSTREAM_ERR.search(text[:300]):
        raise TransportError(f"lỗi upstream trong nội dung: {text[:120]!r}")
    return text, usage


def _read_sse(r: requests.Response) -> tuple[str, dict]:
    parts, usage = [], {}
    try:
        for raw in r.iter_lines(decode_unicode=True):
            if not raw or not raw.startswith("data:"):
                continue
            payload = raw[5:].strip()
            if payload == "[DONE]":
                break
            try:
                ev = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if ev.get("error"):  # ns24 trả lỗi upstream NGAY TRONG SSE với HTTP 200
                raise TransportError(f"SSE error: {str(ev['error'])[:160]}")
            if ev.get("usage"):
                usage = ev["usage"]
            for ch in ev.get("choices") or []:
                d = ch.get("delta") or {}
                if d.get("content"):
                    parts.append(d["content"])
    except requests.RequestException as e:
        raise TransportError(f"stream đứt: {type(e).__name__}") from e
    return "".join(parts), usage


def chat_claude_cli(prov: dict, model: str, messages: list[dict], timeout: int) -> tuple[str, dict]:
    """`claude -p` dùng gói Claude Code (không tốn API key). Chạy trong thư mục TẠM rỗng để
    không nạp CLAUDE.md của dự án vào prompt; stdin đóng (DEVNULL) kẻo chờ 3s vô ích."""
    prompt = "\n\n".join(m["content"] for m in messages)
    cmd = [prov.get("command", "claude"), "-p", "--model", model, "--output-format", "json"]
    with tempfile.TemporaryDirectory(prefix="hunt_v2_claude_") as tmp:
        Path(tmp, "prompt.txt").write_text(prompt, encoding="utf-8")
        try:
            proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=timeout,
                                  cwd=tmp, shell=(os.name == "nt"))
        except (subprocess.TimeoutExpired, OSError) as e:
            raise TransportError(f"claude -p: {type(e).__name__}") from e
    if proc.returncode != 0:
        raise TransportError(f"claude -p rc={proc.returncode}: {proc.stderr[-200:]}")
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError) as e:
        raise TransportError(f"claude -p stdout lạ: {proc.stdout[:200]!r}") from e
    if data.get("is_error"):
        raise TransportError(f"claude -p is_error: {str(data.get('result'))[:200]}")
    text = data.get("result") or ""
    if not text.strip():
        raise TransportError("claude -p trả rỗng")
    return text, data.get("usage") or {}


def repair_json(text: str):
    """Bóc JSON từ text model: bỏ fence → parse thẳng → quét TỪNG vị trí `[`/`{` từ trái sang và
    raw_decode (model reasoning hay in vài dòng dẫn nhập, mà tiêu đề video lại chứa `[`/【 nên
    "tìm ngoặc ngoài cùng" chọn nhầm điểm bắt đầu — đã dính thật 2026-09-22, JSON hợp lệ vẫn báo
    không parse được). Trả None nếu không cứu được (caller ghi error, KHÔNG nuốt)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t[3:]
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    t = t.strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    dec = json.JSONDecoder()
    tried = 0
    for i, ch in enumerate(t):
        if ch not in "[{":
            continue
        tried += 1
        if tried > 200:
            break
        try:
            obj, _end = dec.raw_decode(t[i:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, (list, dict)):
            return obj
    return None
