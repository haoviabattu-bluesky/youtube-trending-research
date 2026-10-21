# -*- coding: utf-8 -*-
"""Đo CUNG trên YouTube cho từng cụm: InnerTube search sort=viewCount window=today (keyless, src/innertube.py).
Mỗi cụm tìm ≤2 truy vấn (label_ja + keyword nóng nhất), gộp theo video_id, chỉ giữ video ≤48h.
Bị bot-check/429 → trả rỗng + cờ `blocked`, KHÔNG dừng cả lượt (cung thiếu thì gap sẽ cao giả → brief ghi rõ)."""
from __future__ import annotations

import time

from innertube import BotCheckError, InnerTube, ProxyError

MAX_AGE_H = 48.0


def queries_for(cluster: dict) -> list[str]:
    """query_ja (LLM/short_query) + keyword NGẮN nhất của cụm (tên riêng) — tiêu đề dài trả 0 video."""
    qs = [cluster.get("query_ja") or cluster["label_ja"]]
    for k in sorted(cluster["keywords"], key=len):
        if k not in qs and len(k) <= 14:
            qs.append(k)
            break
    return qs


def measure(it: InnerTube, cluster: dict, log=print) -> dict:
    """Trả {videos: [...], n: int, views: int, blocked: bool}."""
    seen: dict[str, dict] = {}
    blocked = False
    for q in queries_for(cluster):
        try:
            rows = it.search(q, window="today", tries=2)
        except (BotCheckError, ProxyError) as e:
            blocked = True
            log(f"  ✗ YouTube chặn khi tìm {q!r}: {type(e).__name__}")
            break
        except RuntimeError as e:
            log(f"  ✗ InnerTube lỗi {q!r}: {str(e)[:80]}")
            continue
        for r in rows:
            age = r.get("age_hours_it")
            if age is not None and age > MAX_AGE_H:
                continue
            cur = seen.get(r["video_id"])
            if cur is None or (r.get("views_it") or 0) > (cur.get("views_it") or 0):
                seen[r["video_id"]] = r
        time.sleep(it.throttle)
    vids = sorted(seen.values(), key=lambda r: -(r.get("views_it") or 0))
    return {"videos": vids, "n": len(vids), "views": sum(int(v.get("views_it") or 0) for v in vids),
            "blocked": blocked}
