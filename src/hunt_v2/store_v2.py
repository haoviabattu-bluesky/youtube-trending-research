# -*- coding: utf-8 -*-
"""SQLite cho V2 — tách khỏi store.py để file đó không vượt 200 dòng. Bảng khai ở store.SCHEMA.

hunt_v2_pick.mode: SHADOW (chỉ ghi audit) | PRODUCTION (đã ghi RESEARCH). Chống chọn lại
chỉ tính PRODUCTION — pick shadow hôm nay vẫn được chọn lại khi bật production.
"""
from __future__ import annotations

import json
import sqlite3

from store import today
def v2_picked_video_ids(con: sqlite3.Connection, lane: str, mode: str | None = None) -> set[str]:
    """Video V2 đã chọn cho lane (mode='PRODUCTION' để chỉ tính pick thật, None = mọi mode)."""
    if mode:
        q = con.execute("SELECT video_id FROM hunt_v2_pick WHERE lane=? AND mode=?", (lane, mode))
    else:
        q = con.execute("SELECT video_id FROM hunt_v2_pick WHERE lane=?", (lane,))
    return {r["video_id"] for r in q}


def save_v2_picks(con: sqlite3.Connection, lane: str, picks: list[dict], pick_date: str,
                  mode: str) -> None:
    con.executemany("""INSERT INTO hunt_v2_pick(video_id,lane,pick_date,rank,mode,final_score,payload)
                       VALUES(?,?,?,?,?,?,?) ON CONFLICT(video_id,lane) DO UPDATE SET
                         mode=CASE WHEN excluded.mode='PRODUCTION' THEN 'PRODUCTION' ELSE hunt_v2_pick.mode END,
                         final_score=excluded.final_score, payload=excluded.payload""",
                    [(p["video_id"], lane, pick_date, i + 1, mode, p.get("final_score"),
                      json.dumps(p, ensure_ascii=False, default=str)) for i, p in enumerate(picks)])
    con.commit()


def load_hunt_baseline(con: sqlite3.Connection, channel_id: str) -> dict | None:
    r = con.execute("SELECT * FROM hunt_baseline WHERE channel_id=?", (channel_id,)).fetchone()
    return dict(r) if r else None


def save_hunt_baseline(con: sqlite3.Connection, channel_id: str, b: dict) -> None:
    con.execute("""INSERT INTO hunt_baseline(channel_id,median_views,median_vph,n_videos,payload,updated)
                   VALUES(?,?,?,?,?,?) ON CONFLICT(channel_id) DO UPDATE SET
                     median_views=excluded.median_views, median_vph=excluded.median_vph,
                     n_videos=excluded.n_videos, payload=excluded.payload, updated=excluded.updated""",
                (channel_id, b["median_recent_views"], b["median_recent_vph"], b["n_videos"],
                 json.dumps(b, ensure_ascii=False), today()))
    con.commit()


def upsert_human_feedback(con: sqlite3.Connection, rows: list[dict]) -> int:
    con.executemany("""INSERT INTO human_feedback(video_id,lane,decision,reason,note,date)
                       VALUES(?,?,?,?,?,?) ON CONFLICT(video_id,lane) DO UPDATE SET
                         decision=excluded.decision, reason=excluded.reason, note=excluded.note,
                         date=excluded.date""",
                    [(r["video_id"], r["lane"], r["decision"], r.get("reason", ""),
                      r.get("note", ""), r.get("date", today())) for r in rows])
    con.commit()
    return len(rows)
