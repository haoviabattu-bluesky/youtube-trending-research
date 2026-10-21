# -*- coding: utf-8 -*-
"""Gói tư liệu cho top N cụm: đọc bài gốc (Google Trends news_item · Yahoo articles · Google News) → trích đoạn.
Đường đọc: requests + MG_STUDIO core.web_text (nhanh) → thất bại hoặc link redirect Google News thì
pw_search.py `f` (Chrome nền cổng 9461, KHÔNG mở/tắt cửa sổ — luật tim-web-bang-chrome-nen).
Tuỳ chọn: hook 0–90s của 2 video đối thủ nhiều view nhất (src/hook_fetch.py, ASR khi bị chặn)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, r"E:\CLAUDE\YOUTUBE\MG_STUDIO")


def candidate_urls(cluster: dict, per_cluster: int) -> list[tuple[str, str, str]]:
    """(url, title, source) từ signal của cụm: trends news_item → yahoo → google news (redirect, để cuối)."""
    direct, redirect, seen = [], [], set()
    for src, sigs in cluster["by_source"].items():
        for s in sigs:
            ex = s.get("extra") or {}
            if src == "google_trends":
                for n in ex.get("news", []):
                    if n.get("url") and n["url"] not in seen:
                        seen.add(n["url"])
                        direct.append((n["url"], n.get("title", ""), n.get("source", "")))
            elif src == "yahoo_ranking" and s.get("url") and s["url"] not in seen:
                seen.add(s["url"])
                direct.append((s["url"], s["keyword"], ex.get("medium", "Yahoo!ニュース")))
            elif src == "google_news" and s.get("url") and s["url"] not in seen:
                seen.add(s["url"])
                redirect.append((s["url"], s["keyword"], ex.get("medium", "")))
    return (direct + redirect)[:per_cluster]


def read_fast(url: str, max_chars: int) -> tuple[str, str] | None:
    try:
        from core import web_text as W  # MG_STUDIO
        title, text = W.tai(url, timeout=30)
    except Exception:  # noqa: BLE001
        return None
    text = re.sub(r"\n{2,}", "\n", text or "")
    return (title, text[:max_chars]) if len(text) >= 300 else None


def read_chrome(urls: list[str], max_chars: int, pw_search: Path, log=print) -> dict[str, tuple[str, str]]:
    """Một lệnh pw_search cho nhiều URL (Chrome nền dùng chung). Parse stdout '### <status> <title> | <url>  (...)'."""
    if not urls:
        return {}
    cmd = [sys.executable, "-X", "utf8", str(pw_search), "f", *urls, "--max", str(max_chars)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=90 + 40 * len(urls), cwd=str(pw_search.parent))
    except subprocess.TimeoutExpired:
        log("  ✗ pw_search quá giờ")
        return {}
    out: dict[str, tuple[str, str]] = {}
    blocks = re.split(r"\n(?=### )", "\n" + p.stdout)
    for b in blocks:
        m = re.match(r"### (\S+) (.*?) \| (\S+)\s+\((\d+) ký tự\)\n?(.*)", b.strip(), re.S)
        if not m or m.group(1) in ("LOI",):
            continue
        out[m.group(3)] = (m.group(2).strip(), m.group(5)[:max_chars])
    return out


def gather(con, cluster: dict, cfg: dict, store, log=print) -> int:
    """Đọc ≤ evidence_urls_per_cluster bài, ghi bảng evidence. Trả số bài đọc được."""
    b = cfg["brief"]
    cands = candidate_urls(cluster, b["evidence_urls_per_cluster"])
    have = {e["url"] for e in store.evidence_of(con, cluster["cluster_id"]) if e["status"] == "ok"}
    todo = [c for c in cands if c[0] not in have]
    pending = []
    for url, title, source in todo:
        r = None if "news.google.com/rss/articles" in url else read_fast(url, b["evidence_chars_per_url"])
        if r:
            store.put_evidence(con, cluster["cluster_id"], url, r[0] or title, source, r[1], "ok")
        else:
            pending.append((url, title, source))
    if pending:
        got = read_chrome([u for u, _, _ in pending], b["evidence_chars_per_url"], ROOT / cfg["tools"]["pw_search"], log)
        for url, title, source in pending:
            r = got.get(url)
            if r and len(r[1]) >= 300:
                store.put_evidence(con, cluster["cluster_id"], url, r[0] or title, source, r[1], "ok")
            else:
                store.put_evidence(con, cluster["cluster_id"], url, title, source, "", "fail")
    n = sum(1 for e in store.evidence_of(con, cluster["cluster_id"]) if e["status"] == "ok")
    log(f"  📄 {cluster['label_ja'][:30]}: {n}/{len(cands)} bài đọc được")
    return n


def gather_hooks(con, cluster: dict, cfg: dict, store, log=print) -> int:
    import hook_fetch  # src/hook_fetch.py — có đường ASR khi YouTube chặn phụ đề
    vids = store.supply_of(con, cluster["cluster_id"])[: cfg["brief"]["hooks_per_cluster"]]
    n = 0
    for v in vids:
        try:
            rec = hook_fetch.fetch(v["video_id"], lang="ja", sec=90)
        except Exception as e:  # noqa: BLE001
            log(f"  ✗ hook {v['video_id']}: {type(e).__name__}")
            continue
        text = " ".join(s.get("text", "") for s in rec.get("hook_segments", []))[:1200]
        if text:
            store.put_hook(con, cluster["cluster_id"], v["video_id"], text, rec.get("transcript_via", "?"))
            n += 1
    return n


def dump_pack(cluster: dict, evidence: list[dict], supply: list[dict], hooks: list[dict], out_dir: Path) -> Path:
    """Ghi gói tư liệu JSON cho MG_STUDIO (1 file/cụm)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{cluster['cluster_id']}.json"
    p.write_text(json.dumps({"cluster": {k: v for k, v in cluster.items() if k != "by_source"},
                             "evidence": evidence, "supply": supply[:10], "hooks": hooks},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    return p
