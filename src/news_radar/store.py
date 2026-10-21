# -*- coding: utf-8 -*-
"""SQLite cho NEWS RADAR: signal (thô từng nguồn) · cluster (cụm sự kiện/ngày) · supply (video YouTube 24h)
· evidence (bài gốc đã đọc). Khoá signal = (source, keyword, snap_ts) — mỗi lượt thu 1 snapshot."""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

DDL = """
CREATE TABLE IF NOT EXISTS signal (
  source TEXT NOT NULL, keyword TEXT NOT NULL, rank INTEGER, traffic INTEGER,
  url TEXT, extra TEXT, snap_ts INTEGER NOT NULL,
  PRIMARY KEY (source, keyword, snap_ts));
CREATE INDEX IF NOT EXISTS ix_signal_ts ON signal(snap_ts);
CREATE TABLE IF NOT EXISTS cluster (
  cluster_id TEXT PRIMARY KEY, snap_date TEXT NOT NULL, label_ja TEXT, label_vi TEXT,
  category TEXT, sensational INTEGER, is_news INTEGER, q_fit INTEGER, summary_vi TEXT,
  keywords TEXT, sources TEXT, heat REAL, velocity REAL, gap REAL, final REAL,
  supply_videos INTEGER, supply_views INTEGER, brief TEXT, updated_ts INTEGER);
CREATE INDEX IF NOT EXISTS ix_cluster_date ON cluster(snap_date);
CREATE TABLE IF NOT EXISTS supply (
  cluster_id TEXT NOT NULL, video_id TEXT NOT NULL, title TEXT, channel TEXT, channel_id TEXT,
  views INTEGER, age_hours REAL, duration_s INTEGER, keyword TEXT, snap_ts INTEGER,
  PRIMARY KEY (cluster_id, video_id));
CREATE TABLE IF NOT EXISTS evidence (
  cluster_id TEXT NOT NULL, url TEXT NOT NULL, title TEXT, source TEXT, excerpt TEXT,
  status TEXT, fetched_ts INTEGER, PRIMARY KEY (cluster_id, url));
CREATE TABLE IF NOT EXISTS hook (
  cluster_id TEXT NOT NULL, video_id TEXT NOT NULL, text TEXT, via TEXT, fetched_ts INTEGER,
  PRIMARY KEY (cluster_id, video_id));
"""


def connect(path: str | Path) -> sqlite3.Connection:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(p)
    con.row_factory = sqlite3.Row
    con.executescript(DDL)
    return con


def insert_signals(con: sqlite3.Connection, rows: list[dict], snap_ts: int) -> int:
    """rows: {source, keyword, rank, traffic, url, extra(dict)}. Trả số dòng ghi mới."""
    n = 0
    for r in rows:
        kw = (r.get("keyword") or "").strip()
        if not kw:
            continue
        cur = con.execute(
            "INSERT OR IGNORE INTO signal(source,keyword,rank,traffic,url,extra,snap_ts) VALUES(?,?,?,?,?,?,?)",
            (r["source"], kw, r.get("rank"), r.get("traffic"), r.get("url"),
             json.dumps(r.get("extra") or {}, ensure_ascii=False), snap_ts))
        n += cur.rowcount
    con.commit()
    return n


def recent_signals(con: sqlite3.Connection, since_ts: int) -> list[sqlite3.Row]:
    return con.execute("SELECT * FROM signal WHERE snap_ts >= ? ORDER BY snap_ts", (since_ts,)).fetchall()


def upsert_cluster(con: sqlite3.Connection, c: dict) -> None:
    cols = ["cluster_id", "snap_date", "label_ja", "label_vi", "category", "sensational", "is_news", "q_fit",
            "summary_vi", "keywords", "sources", "heat", "velocity", "gap", "final", "supply_videos",
            "supply_views", "brief"]
    vals = []
    for k in cols:
        v = c.get(k)
        if isinstance(v, (list, dict)):
            v = json.dumps(v, ensure_ascii=False)
        elif isinstance(v, bool):
            v = int(v)
        vals.append(v)
    con.execute(f"INSERT OR REPLACE INTO cluster({','.join(cols)},updated_ts) VALUES({','.join('?' * len(cols))},?)",
                (*vals, int(time.time())))
    con.commit()


def clusters_of_day(con: sqlite3.Connection, snap_date: str) -> list[dict]:
    out = []
    for r in con.execute("SELECT * FROM cluster WHERE snap_date=? ORDER BY final DESC NULLS LAST", (snap_date,)):
        d = dict(r)
        for k in ("keywords", "sources", "brief"):
            if d.get(k):
                try:
                    d[k] = json.loads(d[k])
                except ValueError:
                    pass
        out.append(d)
    return out


def prev_cluster_heat(con: sqlite3.Connection, label_ja: str, before_date: str) -> float | None:
    r = con.execute("SELECT heat FROM cluster WHERE label_ja=? AND snap_date<? ORDER BY snap_date DESC LIMIT 1",
                    (label_ja, before_date)).fetchone()
    return float(r["heat"]) if r and r["heat"] is not None else None


def replace_supply(con: sqlite3.Connection, cluster_id: str, videos: list[dict], snap_ts: int) -> None:
    con.execute("DELETE FROM supply WHERE cluster_id=?", (cluster_id,))
    con.executemany(
        "INSERT OR REPLACE INTO supply VALUES(?,?,?,?,?,?,?,?,?,?)",
        [(cluster_id, v["video_id"], v.get("title"), v.get("channel"), v.get("channel_id"),
          v.get("views_it"), v.get("age_hours_it"), v.get("duration_s_it"), v.get("keyword"), snap_ts)
         for v in videos])
    con.commit()


def supply_of(con: sqlite3.Connection, cluster_id: str) -> list[dict]:
    return [dict(r) for r in con.execute(
        "SELECT * FROM supply WHERE cluster_id=? ORDER BY views DESC", (cluster_id,))]


def put_evidence(con: sqlite3.Connection, cluster_id: str, url: str, title: str, source: str,
                 excerpt: str, status: str) -> None:
    con.execute("INSERT OR REPLACE INTO evidence VALUES(?,?,?,?,?,?,?)",
                (cluster_id, url, title, source, excerpt, status, int(time.time())))
    con.commit()


def evidence_of(con: sqlite3.Connection, cluster_id: str) -> list[dict]:
    return [dict(r) for r in con.execute(
        "SELECT * FROM evidence WHERE cluster_id=? ORDER BY fetched_ts", (cluster_id,))]


def put_hook(con: sqlite3.Connection, cluster_id: str, video_id: str, text: str, via: str) -> None:
    con.execute("INSERT OR REPLACE INTO hook VALUES(?,?,?,?,?)",
                (cluster_id, video_id, text, via, int(time.time())))
    con.commit()


def hooks_of(con: sqlite3.Connection, cluster_id: str) -> list[dict]:
    return [dict(r) for r in con.execute("SELECT * FROM hook WHERE cluster_id=?", (cluster_id,))]
