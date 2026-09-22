# -*- coding: utf-8 -*-
"""SQLite — nguồn chân lý. Google Sheet chỉ là lớp báo cáo.

Snapshot khoá theo (id, snap_date) nên chạy lại nhiều lần trong ngày là idempotent.
Delta 24h = snapshot hôm nay − snapshot gần nhất trước đó.
"""
from __future__ import annotations

import datetime as dt
import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS video(
  video_id TEXT PRIMARY KEY, channel_id TEXT, title TEXT, published_at TEXT,
  duration_s INT, niches TEXT, keywords TEXT, first_seen TEXT);
CREATE TABLE IF NOT EXISTS video_snapshot(
  video_id TEXT, snap_date TEXT, views INT, likes INT, comments INT,
  PRIMARY KEY(video_id, snap_date));
CREATE TABLE IF NOT EXISTS channel(
  channel_id TEXT PRIMARY KEY, title TEXT, created_at TEXT, ch_age_days INT,
  uploads_playlist TEXT, niches TEXT, first_seen TEXT, watchlist INT DEFAULT 0);
CREATE TABLE IF NOT EXISTS channel_snapshot(
  channel_id TEXT, snap_date TEXT, subs INT, total_views INT, video_count INT,
  PRIMARY KEY(channel_id, snap_date));
CREATE TABLE IF NOT EXISTS channel_baseline(
  channel_id TEXT PRIMARY KEY, median_views INT, p90_views INT, n_videos INT,
  hit_rate REAL, trend REAL, updated TEXT);
CREATE TABLE IF NOT EXISTS keyword_snapshot(
  keyword TEXT, niche TEXT, snap_date TEXT, n_new_7d INT, median_views_7d INT,
  p90_views_7d INT, n_new_channels INT, PRIMARY KEY(keyword, snap_date));
CREATE TABLE IF NOT EXISTS deepdive(
  video_id TEXT, snap_date TEXT, payload TEXT, PRIMARY KEY(video_id, snap_date));
CREATE TABLE IF NOT EXISTS hunt_pick(
  video_id TEXT, lane TEXT, pick_date TEXT, rank INT, title TEXT, channel TEXT,
  views INT, age_days REAL, vpd REAL, score REAL, reason TEXT,
  PRIMARY KEY(video_id, lane));
-- VIDEO HUNT V2 (2026-09-22) — bảng riêng, không đụng bảng cũ
CREATE TABLE IF NOT EXISTS hunt_baseline(
  channel_id TEXT PRIMARY KEY, median_views INT, median_vph REAL, n_videos INT,
  payload TEXT, updated TEXT);
CREATE TABLE IF NOT EXISTS hunt_v2_pick(
  video_id TEXT, lane TEXT, pick_date TEXT, rank INT, mode TEXT, final_score REAL,
  payload TEXT, PRIMARY KEY(video_id, lane));
CREATE TABLE IF NOT EXISTS human_feedback(
  video_id TEXT, lane TEXT, decision TEXT, reason TEXT, note TEXT, date TEXT,
  PRIMARY KEY(video_id, lane));
CREATE INDEX IF NOT EXISTS ix_vs_date ON video_snapshot(snap_date);
CREATE INDEX IF NOT EXISTS ix_v_channel ON video(channel_id);
CREATE INDEX IF NOT EXISTS ix_v_first_seen ON video(first_seen);
CREATE INDEX IF NOT EXISTS ix_hp_lane ON hunt_pick(lane);
"""


def today() -> str:
    return dt.date.today().isoformat()


def connect(db_path: str | Path) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def _merge_csv(old: str | None, new: str) -> str:
    """Gộp danh sách phân tách bằng '|' mà không nhân đôi."""
    seen = [x for x in (old or "").split("|") if x]
    for v in new.split("|"):
        if v and v not in seen:
            seen.append(v)
    return "|".join(seen)


def dedupe_rows(rows: list[dict]) -> list[dict]:
    """1 video xuất hiện ở nhiều keyword/ngách → 1 dòng, gộp keyword+niche."""
    out: dict[str, dict] = {}
    for r in rows:
        cur = out.get(r["video_id"])
        if cur is None:
            r = dict(r)
            r["niches"], r["keywords"] = r["niche"], r["keyword"]
            out[r["video_id"]] = r
        else:
            cur["niches"] = _merge_csv(cur["niches"], r["niche"])
            cur["keywords"] = _merge_csv(cur["keywords"], r["keyword"])
            if r["views"] > cur["views"]:
                cur["views"] = r["views"]
    return list(out.values())


def save_snapshot(con: sqlite3.Connection, rows: list[dict], snap: str | None = None) -> int:
    snap = snap or today()
    cur = con.cursor()
    for r in rows:
        cur.execute("""INSERT INTO video(video_id,channel_id,title,published_at,duration_s,
                       niches,keywords,first_seen) VALUES(?,?,?,?,?,?,?,?)
                       ON CONFLICT(video_id) DO UPDATE SET
                         title=excluded.title, duration_s=excluded.duration_s,
                         niches=excluded.niches, keywords=excluded.keywords""",
                    (r["video_id"], r["channel_id"], r["title"], r["published_at"],
                     r["duration_s"], r.get("niches", r["niche"]),
                     r.get("keywords", r["keyword"]), snap))
        cur.execute("""INSERT INTO video_snapshot(video_id,snap_date,views,likes,comments)
                       VALUES(?,?,?,?,?) ON CONFLICT(video_id,snap_date) DO UPDATE SET
                         views=excluded.views, likes=excluded.likes, comments=excluded.comments""",
                    (r["video_id"], snap, r["views"], r["likes"], r["comments"]))

    seen: set[str] = set()
    for r in rows:
        cid = r["channel_id"]
        if not cid or cid in seen:
            continue
        seen.add(cid)
        cur.execute("""INSERT INTO channel(channel_id,title,created_at,ch_age_days,
                       uploads_playlist,niches,first_seen) VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(channel_id) DO UPDATE SET
                         title=excluded.title, ch_age_days=excluded.ch_age_days,
                         uploads_playlist=excluded.uploads_playlist""",
                    (cid, r["channel"], r["ch_created_at"], r["ch_age_days"],
                     r["uploads_playlist"], r.get("niches", r["niche"]), snap))
        cur.execute("""INSERT INTO channel_snapshot(channel_id,snap_date,subs,total_views,video_count)
                       VALUES(?,?,?,?,?) ON CONFLICT(channel_id,snap_date) DO UPDATE SET
                         subs=excluded.subs, total_views=excluded.total_views,
                         video_count=excluded.video_count""",
                    (cid, snap, r["subs"], r["ch_total_views"], r["ch_video_count"]))
    con.commit()
    return len(rows)


def prev_video_stats(con: sqlite3.Connection, snap: str) -> dict[str, tuple[int, str]]:
    """Snapshot gần nhất TRƯỚC `snap` của mỗi video → {video_id: (views, snap_date)}."""
    q = """SELECT video_id, views, snap_date FROM video_snapshot vs
           WHERE snap_date < ? AND snap_date = (
             SELECT MAX(snap_date) FROM video_snapshot x
             WHERE x.video_id = vs.video_id AND x.snap_date < ?)"""
    return {r["video_id"]: (r["views"], r["snap_date"]) for r in con.execute(q, (snap, snap))}


def prev_channel_subs(con: sqlite3.Connection, snap: str, days: int = 7) -> dict[str, int]:
    cutoff = (dt.date.fromisoformat(snap) - dt.timedelta(days=days)).isoformat()
    q = """SELECT channel_id, subs FROM channel_snapshot cs
           WHERE snap_date <= ? AND snap_date = (
             SELECT MAX(snap_date) FROM channel_snapshot x
             WHERE x.channel_id = cs.channel_id AND x.snap_date <= ?)"""
    return {r["channel_id"]: r["subs"] for r in con.execute(q, (cutoff, cutoff))}


def save_baselines(con: sqlite3.Connection, baselines: dict[str, dict]) -> None:
    con.executemany("""INSERT INTO channel_baseline(channel_id,median_views,p90_views,
                       n_videos,hit_rate,trend,updated) VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(channel_id) DO UPDATE SET
                         median_views=excluded.median_views, p90_views=excluded.p90_views,
                         n_videos=excluded.n_videos, hit_rate=excluded.hit_rate,
                         trend=excluded.trend, updated=excluded.updated""",
                    [(c, b["median_views"], b["p90_views"], b["n_videos"],
                      b["hit_rate"], b.get("trend"), today()) for c, b in baselines.items()])
    con.commit()


def load_baselines(con: sqlite3.Connection) -> dict[str, dict]:
    return {r["channel_id"]: dict(r) for r in con.execute("SELECT * FROM channel_baseline")}


def save_deepdive(con: sqlite3.Connection, video_id: str, payload: dict, snap: str | None = None):
    con.execute("""INSERT INTO deepdive(video_id,snap_date,payload) VALUES(?,?,?)
                   ON CONFLICT(video_id,snap_date) DO UPDATE SET payload=excluded.payload""",
                (video_id, snap or today(), json.dumps(payload, ensure_ascii=False)))
    con.commit()


def save_keyword_snapshot(con: sqlite3.Connection, rows: list[dict], snap: str | None = None):
    con.executemany("""INSERT INTO keyword_snapshot(keyword,niche,snap_date,n_new_7d,
                       median_views_7d,p90_views_7d,n_new_channels) VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(keyword,snap_date) DO UPDATE SET
                         n_new_7d=excluded.n_new_7d, median_views_7d=excluded.median_views_7d,
                         p90_views_7d=excluded.p90_views_7d, n_new_channels=excluded.n_new_channels""",
                    [(r["keyword"], r["niche"], snap or today(), r["n_new_7d"],
                      r["median_views_7d"], r["p90_views_7d"], r["n_new_channels"]) for r in rows])
    con.commit()


def picked_video_ids(con: sqlite3.Connection, lane: str) -> set[str]:
    """Video ĐÃ được chọn cho lane này ở bất kỳ ngày nào trước đó — chặn chọn lại."""
    return {r["video_id"] for r in con.execute(
        "SELECT video_id FROM hunt_pick WHERE lane=?", (lane,))}


def save_hunt_picks(con: sqlite3.Connection, lane: str, picks: list[dict], pick_date: str) -> None:
    con.executemany("""INSERT INTO hunt_pick(video_id,lane,pick_date,rank,title,channel,
                       views,age_days,vpd,score,reason) VALUES(?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(video_id,lane) DO NOTHING""",
                    [(p["video_id"], lane, pick_date, i + 1, p["title"], p["channel"],
                      p["views"], p["age_days"], p["vpd"], p["score"], p["reason"])
                     for i, p in enumerate(picks)])
    con.commit()


def channel_first_seen(con: sqlite3.Connection) -> dict[str, str]:
    """Ngày phát hiện GỐC của mỗi kênh — dùng khi upsert Sheet để không ghi đè mất."""
    return {r["channel_id"]: r["first_seen"]
            for r in con.execute("SELECT channel_id, first_seen FROM channel")}

