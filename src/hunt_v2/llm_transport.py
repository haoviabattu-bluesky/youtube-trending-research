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
import time
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
        # text/event-stream không khai charset → requests mặc định ISO-8859-1, iter_lines(decode_unicode)
        # biến tiếng Nhật thành mojibake (đo thật 17/10/2026, NEWS RADAR: JSON cụm bị băm nát). Ép UTF-8.
        r.encoding = "utf-8"
        text, usage = _read_sse(r, deadline=time.time() + timeout)
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


def _read_sse(r: requests.Response, deadline: float) -> tuple[str, dict]:
    """`deadline` là mốc TUYỆT ĐỐI phải dừng. Timeout của requests chỉ tính cho MỖI lần đọc
    socket — proxy nhỏ giọt dòng keep-alive `: ping` vài giây một lần thì không bao giờ chạm
    timeout, call treo vô hạn (đã dính thật 2026-09-22: 1 lượt đứng 20 phút không log gì)."""
    parts, usage = [], {}
    try:
        for raw in r.iter_lines(decode_unicode=True):
            if time.time() > deadline:
                raise TransportError(
                    f"Timeout: quá hạn {int(time.time() - deadline)}s "
                    f"({'chưa nhận được nội dung nào' if not parts else 'stream chưa kết thúc'})")
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


LITE_SYSTEM = "Bạn là công cụ xử lý dữ liệu. Làm đúng yêu cầu, chỉ trả đúng định dạng được yêu cầu."


def claude_cli_cmd(prov: dict, model: str, effort: str | None, sys_file: str | None) -> list[str]:
    """Lệnh `claude -p`. Provider `lite: true` (đường "Claude gọn", anh duyệt 21/10/2026) thêm 3 cờ
    --tools "" · --strict-mcp-config · --system-prompt-file (thay system prompt mặc định ~6k token)
    + --safe-mode (bỏ CLAUDE.md/skill/plugin: đo thật 6.941 → 790 token nền/lượt)."""
    cmd = [prov.get("command", "claude"), "-p", "--model", model, "--output-format", "json"]
    if effort:
        cmd += ["--effort", effort]
    if prov.get("lite"):
        cmd += ["--tools", "", "--strict-mcp-config", "--safe-mode", "--system-prompt-file", sys_file]
    return cmd


def _cli_usage(data: dict) -> dict:
    """Token thật từ modelUsage (input gồm cả cache tạo/đọc) → khoá chuẩn prompt/completion_tokens."""
    pt = ct = 0
    for mu in (data.get("modelUsage") or {}).values():
        pt += int(mu.get("inputTokens") or 0) + int(mu.get("cacheCreationInputTokens") or 0) \
            + int(mu.get("cacheReadInputTokens") or 0)
        ct += int(mu.get("outputTokens") or 0)
    return {"prompt_tokens": pt, "completion_tokens": ct, "cost_usd": data.get("total_cost_usd")}


def chat_claude_cli(prov: dict, model: str, messages: list[dict], timeout: int,
                    effort: str | None = None) -> tuple[str, dict]:
    """`claude -p` dùng gói Claude Code (không tốn API key). Chạy trong thư mục TẠM rỗng để
    không nạp CLAUDE.md của dự án vào prompt; prompt qua stdin. Đường lite: tin nhắn system của
    caller → file system prompt (không nhét vào dòng lệnh: cmd.exe vỡ với & | < >)."""
    lite = bool(prov.get("lite"))
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system") if lite else ""
    prompt = "\n\n".join(m["content"] for m in messages if not (lite and m["role"] == "system"))
    with tempfile.TemporaryDirectory(prefix="hunt_v2_claude_") as tmp:
        sys_file = str(Path(tmp, "system.txt"))
        Path(sys_file).write_text(system or LITE_SYSTEM, encoding="utf-8")
        cmd = claude_cli_cmd(prov, model, effort, sys_file)
        try:
            proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=timeout,
                                  cwd=tmp, shell=(os.name == "nt"))
        except (subprocess.TimeoutExpired, OSError) as e:
            raise TransportError(f"claude -p: {type(e).__name__}") from e
    if proc.returncode != 0:
        raise TransportError(f"claude -p rc={proc.returncode}: {(proc.stderr or proc.stdout)[-200:]}")
    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError) as e:
        raise TransportError(f"claude -p stdout lạ: {proc.stdout[:200]!r}") from e
    if data.get("is_error"):
        raise TransportError(f"claude -p is_error: {str(data.get('result'))[:200]}")
    text = data.get("result") or ""
    if not text.strip():
        raise TransportError("claude -p trả rỗng")
    return text, _cli_usage(data)


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
