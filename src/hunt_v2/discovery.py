# -*- coding: utf-8 -*-
"""H1 — discovery mở rộng (guide §7, §8): thêm nguồn B concept / C format+audience / D watch channel
lên trên pool tag (nguồn A) mà đường cũ đã quét. Mỗi video gắn `discovery_sources` để trace.

Tái dùng run_video_hunt.discover_lane (đổi proxy khi bot-check) — không viết lại logic search.
Watch channel: Data API playlistItems (1 quota/kênh) lấy video ≤ N ngày, không cần keyword.
"""
from __future__ import annotations

import datetime as dt

from hunt_v2.lane_profile import LaneProfile


def expansion_queries(lane: LaneProfile, already: list[str], max_q: int) -> list[tuple[str, str]]:
    """[(query, group)] chưa có trong pool tag cũ, theo thứ tự ưu tiên, cắt max_q."""
    have = {q.replace(" ", "") for q in already}
    out = []
    for grp, qs in lane.all_queries.items():
        for q in qs:
            if q.replace(" ", "") not in have:
                out.append((q, grp))
                have.add(q.replace(" ", ""))
    return out[:max_q]


def _mark(found: dict[str, dict], vid: str, src: str) -> None:
    row = found.get(vid)
    if row is not None:
        row.setdefault("discovery_sources", [])
        if src not in row["discovery_sources"]:
            row["discovery_sources"].append(src)


def run(found: dict[str, dict], lane: LaneProfile, kws: list[str], it, pool, api, rules: dict,
        discover_fn, log) -> dict[str, dict]:
    """Bổ sung vào `found` (dict video_id → row InnerTube). Trả dict thống kê."""
    d = rules["discovery"]
    for vid in found:
        _mark(found, vid, "A:tag")
    stats = {"queries_extra": 0, "new_from_queries": 0, "watch_channels": 0, "new_from_watch": 0}

    qs = expansion_queries(lane, kws, d["max_queries_per_lane"])
    stats["queries_extra"] = len(qs)
    if qs:
        before = set(found)
        by_group: dict[str, list[str]] = {}
        for q, grp in qs:
            by_group.setdefault(grp, []).append(q)
        for grp, qlist in by_group.items():
            extra = discover_fn(it, qlist, d["windows"], d["pages_per_kw"], f"{lane.lane_id}/{grp}", pool)
            for vid, row in extra.items():
                if vid not in found:
                    found[vid] = row
                _mark(found, vid, f"B:{grp}")
        stats["new_from_queries"] = len(set(found) - before)

    if api is not None and lane.watch_channels:
        before = set(found)
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=d["watch_channel_max_age_days"])
        for wc in lane.watch_channels:
            cid = wc.get("channel_id")
            if not cid:
                continue
            stats["watch_channels"] += 1
            try:
                ids = api.recent_uploads(f"UU{cid[2:]}", limit=20)
                vids = api.videos_batch(ids)
            except Exception as e:  # quota/mạng — bỏ kênh này, không hỏng lane
                log(f"  ! watch {cid}: {type(e).__name__}")
                continue
            for vid, v in vids.items():
                try:
                    born = dt.datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
                except (ValueError, KeyError):
                    continue
                if born < cutoff:
                    continue
                if vid not in found:
                    found[vid] = {"video_id": vid, "title": v["title_api"],
                                  "channel": wc.get("channel_name", ""), "channel_id": cid,
                                  "views_it": v["views"], "duration_s_it": v["duration_s"],
                                  "age_hours_it": (dt.datetime.now(dt.timezone.utc) - born).total_seconds() / 3600,
                                  "keyword": f"watch:{cid}", "window": "watch"}
                _mark(found, vid, "D:watch")
        stats["new_from_watch"] = len(set(found) - before)
    return stats
