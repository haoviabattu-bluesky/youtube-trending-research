# -*- coding: utf-8 -*-
"""Hai bước nặng của pipeline: quét keyword và tính baseline kênh.

Tách khỏi orchestrator vì đây là chỗ tiêu tốn thời gian + quota, cần đọc và chỉnh riêng.
"""
from __future__ import annotations

import sys

import score as sc
import store
from innertube import BotCheckError, InnerTube
from ytapi import QuotaExhausted, YouTubeAPI

LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731


def discover_niche(it: InnerTube, kws: list[str], windows: list[str], name: str) -> dict:
    found: dict[str, dict] = {}
    for i, kw in enumerate(kws, 1):
        for w in windows:
            try:
                for row in it.search(kw, w):
                    found.setdefault(row["video_id"], row)
            except BotCheckError:
                raise
            except Exception as e:
                LOG(f"  ! {kw}[{w}]: {type(e).__name__}")
        if i % 20 == 0:
            LOG(f"  [{name}] {i}/{len(kws)} kw → {len(found)} video")
    return found


def compute_baselines(api: YouTubeAPI | None, rows: list[dict], cfg: dict,
                      con) -> dict[str, dict]:
    """Baseline = median view của N video gần nhất mỗi kênh. Chỉ tính cho kênh ỨNG VIÊN
    (mỗi kênh tốn 2 quota) — không tính cho toàn bộ ~2000 kênh quét được."""
    cached = store.load_baselines(con)
    if not api:
        return cached
    by_ch: dict[str, dict] = {}
    for r in rows:
        cid = r["channel_id"]
        if not cid or (r.get("subs") or 0) < cfg["min_subs"]:
            continue
        if (r.get("ch_age_days") or 9999) > cfg["max_ch_age_days"]:
            continue
        prev = by_ch.get(cid)
        if prev is None or r["views"] > prev["views"]:
            by_ch[cid] = r
    strong = [r for r in by_ch.values() if r["views"] >= cfg.get("baseline_min_views", 10000)]
    ranked = sorted(strong or list(by_ch.values()),
                    key=lambda r: r["views"] / max(r.get("subs") or 1, cfg["min_subs"]),
                    reverse=True)
    todo = [r for r in ranked if r["channel_id"] not in cached][:cfg["baseline_max_channels"]]
    LOG(f"[baseline] {len(todo)} kênh mới cần tính (đã cache {len(cached)})")

    fresh: dict[str, dict] = {}
    for i, r in enumerate(todo, 1):
        cid, pl = r["channel_id"], r.get("uploads_playlist") or f"UU{r['channel_id'][2:]}"
        try:
            vids = api.baseline_videos(pl, cfg["baseline_recent_videos"],
                                       cfg.get("baseline_min_age_days", 7))
            if not vids:
                continue
            fresh[cid] = sc.channel_baseline_from_videos(vids, cfg)
        except QuotaExhausted:
            LOG(f"[baseline] dừng ở {i}/{len(todo)} — chạm ngưỡng quota an toàn")
            break
        except Exception as e:
            LOG(f"  ! baseline {cid}: {type(e).__name__}")
    if fresh:
        store.save_baselines(con, fresh)
    cached.update(fresh)
    return cached


