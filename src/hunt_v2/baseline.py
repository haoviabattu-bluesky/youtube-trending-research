# -*- coding: utf-8 -*-
"""H2b — baseline kênh cho viral engine (guide §9): 10 video gần nhất (bỏ <7 ngày, bỏ Shorts),
median views + median VPH. Cache SQLite `hunt_baseline` 7 ngày. 2 quota Data API/kênh.

Chỉ gọi cho candidate đã qua semantic/format (runner quyết) — không gọi cho cả pool
kẻo cháy quota 10k/ngày. Không có API / hết quota → None + cờ BASELINE_MISSING.
"""
from __future__ import annotations

import datetime as dt
import json
import statistics

from hunt_v2 import store_v2
from ytapi import QuotaExhausted


def _age_hours(published_at: str) -> float | None:
    try:
        born = dt.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return max((dt.datetime.now(dt.timezone.utc) - born).total_seconds() / 3600, 1.0)


def baseline_from_videos(videos: list[dict], min_vph_floor: float,
                         min_duration_s: int = 180) -> dict | None:
    """videos = output ytapi.videos_batch (published_at, views, duration_s). Thuần số, test được."""
    rv, ra, rvph = [], [], []
    for v in videos:
        if (v.get("duration_s") or 0) < min_duration_s:
            continue  # Shorts không tính vào baseline long-form
        age = _age_hours(v.get("published_at", ""))
        if age is None:
            continue
        views = int(v.get("views") or 0)
        rv.append(views)
        ra.append(round(age, 1))
        rvph.append(round(views / age, 3))
    if not rv:
        return None
    return {
        "recent_video_views": rv,
        "recent_video_age_hours": ra,
        "recent_video_vph": rvph,
        "median_recent_views": int(statistics.median(rv)),
        "median_recent_vph": round(max(statistics.median(rvph), min_vph_floor), 3),
        "n_videos": len(rv),
    }


def channel_baselines(api, con, channels: dict[str, str], rules: dict,
                      stats: dict | None = None) -> dict[str, dict | None]:
    """channels = {channel_id: uploads_playlist}. Trả {channel_id: baseline|None}."""
    b = rules["baseline"]
    out: dict[str, dict | None] = {}
    stats = stats if stats is not None else {}
    stats.setdefault("cache_hit", 0)
    stats.setdefault("fetched", 0)
    stats.setdefault("failed", 0)
    cutoff = (dt.date.today() - dt.timedelta(days=b["cache_days"])).isoformat()
    todo = []
    for cid, pl in channels.items():
        cached = store_v2.load_hunt_baseline(con, cid) if con is not None else None
        if cached and cached["updated"] >= cutoff:
            out[cid] = {**json.loads(cached["payload"]), "cached": True}
            stats["cache_hit"] += 1
        else:
            todo.append((cid, pl))
    if api is None:
        for cid, _ in todo:
            out[cid] = None
        return out
    for cid, pl in todo[: b["max_channels_per_lane"]]:
        try:
            vids = api.baseline_videos(pl or f"UU{cid[2:]}", want=b["recent_videos"],
                                       min_age_days=b["min_video_age_days"])
        except QuotaExhausted:
            stats["failed"] += len(todo)
            for c2, _ in todo:
                out.setdefault(c2, None)
            break
        except Exception:
            stats["failed"] += 1
            out[cid] = None
            continue
        bl = baseline_from_videos(vids, b["min_baseline_vph"])
        out[cid] = bl
        stats["fetched"] += 1
        if bl and con is not None:
            store_v2.save_hunt_baseline(con, cid, bl)
    for cid, _ in todo[b["max_channels_per_lane"]:]:
        out.setdefault(cid, None)
    return out
