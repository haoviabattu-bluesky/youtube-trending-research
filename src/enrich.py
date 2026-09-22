# -*- coding: utf-8 -*-
"""Hợp nhất discovery (InnerTube) + enrich (Data API), có fallback 2 chiều.

Nguyên tắc: Data API là nguồn chính vì số liệu chính xác; field nào API không có
mới rơi xuống dữ liệu scrape. Mỗi dòng ghi cột `src` để sau này truy ngược.
"""
from __future__ import annotations

import datetime as dt
from concurrent.futures import ThreadPoolExecutor

from innertube import BotCheckError, InnerTube
from ytapi import QuotaExhausted, YouTubeAPI

ROW_FIELDS = [
    "video_id", "title", "channel", "channel_id", "keyword", "niche", "window",
    "views", "likes", "comments", "duration_s", "published_at", "age_hours",
    "subs", "ch_created_at", "ch_age_days", "ch_total_views", "ch_video_count",
    "uploads_playlist", "src", "snap_date",
    # V2: mặc định rỗng khi không có Data API
    "description", "tags", "live_broadcast_content", "default_language",
]


def _age_hours_from_iso(published_at: str) -> float | None:
    if not published_at:
        return None
    try:
        born = dt.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt.datetime.now(dt.timezone.utc) - born).total_seconds() / 3600


class Enricher:
    def __init__(self, api: YouTubeAPI | None, it: InnerTube, scrape_workers: int = 6):
        self.api, self.it, self.workers = api, it, scrape_workers
        self.stat = {"api_videos": 0, "api_channels": 0, "scrape_channels": 0, "api_off": 0}
        self._ch_cache: dict[str, dict] = {}

    # ---------- kênh ----------
    def _scrape_channels(self, ids: list[str]) -> dict[str, dict]:
        out: dict[str, dict] = {}

        def one(cid):
            try:
                return cid, self.it.channel_about(cid)
            except BotCheckError:
                raise
            except Exception:
                return cid, None

        with ThreadPoolExecutor(self.workers) as ex:
            for cid, info in ex.map(one, ids):
                if info:
                    out[cid] = info
                    self.stat["scrape_channels"] += 1
        return out

    def channels(self, channel_ids: list[str]) -> dict[str, dict]:
        todo = [c for c in channel_ids if c and c not in self._ch_cache]
        api_data: dict[str, dict] = {}
        if self.api and todo:
            try:
                api_data = self.api.channels_batch(todo)
                self.stat["api_channels"] += len(api_data)
            except QuotaExhausted:
                self.stat["api_off"] += 1
        missing = [c for c in todo if c not in api_data]
        scraped = self._scrape_channels(missing) if missing else {}
        for cid in todo:
            a, s = api_data.get(cid), scraped.get(cid)
            self._ch_cache[cid] = {
                "subs": (a or {}).get("subs") or (s or {}).get("subs_it", 0),
                "ch_created_at": (a or {}).get("ch_created_at") or (s or {}).get("ch_created_it", ""),
                "ch_age_days": (a or {}).get("ch_age_days")
                               if (a or {}).get("ch_age_days") is not None
                               else (s or {}).get("ch_age_days_it"),
                "ch_total_views": (a or {}).get("ch_total_views") or (s or {}).get("total_views_it", 0),
                "ch_video_count": (a or {}).get("ch_video_count", 0),
                "uploads_playlist": (a or {}).get("uploads_playlist") or f"UU{cid[2:]}",
                "_src": "api" if a else ("scrape" if s else "none"),
            }
        return {c: self._ch_cache[c] for c in channel_ids if c in self._ch_cache}

    # ---------- hợp nhất ----------
    def build_rows(self, found: list[dict], niche: str) -> list[dict]:
        by_id = {r["video_id"]: r for r in found}
        vid_api: dict[str, dict] = {}
        if self.api and by_id:
            try:
                vid_api = self.api.videos_batch(by_id)
                self.stat["api_videos"] += len(vid_api)
            except QuotaExhausted:
                self.stat["api_off"] += 1

        ch_ids = sorted({r["channel_id"] for r in found if r["channel_id"]})
        ch = self.channels(ch_ids)

        snap = dt.date.today().isoformat()
        rows = []
        for vid, base in by_id.items():
            v = vid_api.get(vid, {})
            c = ch.get(base["channel_id"], {})
            published = v.get("published_at", "")
            rows.append({
                "video_id": vid,
                "title": v.get("title_api") or base["title"],
                "channel": base["channel"],
                "channel_id": base["channel_id"],
                "keyword": base["keyword"],
                "niche": niche,
                "window": base["window"],
                "views": v.get("views") or base["views_it"],
                "likes": v.get("likes", 0),
                "comments": v.get("comments", 0),
                "duration_s": v.get("duration_s") or base.get("duration_s_it", 0),
                "published_at": published,
                "age_hours": round(_age_hours_from_iso(published) or base["age_hours_it"] or 0, 1),
                "subs": c.get("subs", 0),
                "ch_created_at": c.get("ch_created_at", ""),
                "ch_age_days": c.get("ch_age_days"),
                "ch_total_views": c.get("ch_total_views", 0),
                "ch_video_count": c.get("ch_video_count", 0),
                "uploads_playlist": c.get("uploads_playlist", ""),
                "src": f"v:{'api' if v else 'it'}/c:{c.get('_src', 'none')}",
                "snap_date": snap,
                "description": v.get("description", ""),
                "tags": v.get("tags", []) or [],
                "live_broadcast_content": v.get("live_broadcast_content", "none"),
                "default_language": v.get("default_language", ""),
            })
        return rows
