# -*- coding: utf-8 -*-
"""Momentum + content gap theo keyword — thay thế Google Trends (pytrends đã chết 429).

Ưu điểm so với Google Trends: đo được CẢ hai vế ngay trên YouTube —
  cầu = median/p90 view của video mới trong ngách
  cung = số video mới xuất hiện
Content gap = cầu cao mà cung thấp.
"""
from __future__ import annotations

import datetime as dt
import sqlite3
import statistics


def _z(vals: list[float]) -> list[float]:
    if len(vals) < 2:
        return [0.0] * len(vals)
    mu = statistics.mean(vals)
    sd = statistics.pstdev(vals) or 1.0
    return [(v - mu) / sd for v in vals]


def compute(con: sqlite3.Connection, snap: str, kw_niche: dict[str, str],
            days: int = 7) -> list[dict]:
    """Thống kê mỗi keyword trên các video ĐĂNG trong `days` ngày gần đây.

    Gom theo KEYWORD, ngách lấy từ `kw_niche` (config) chứ KHÔNG lấy ngách đầu tiên của
    video. Video khớp keyword của cả 2 ngách sẽ có `niches='jp_senior|jp_satori'`, lấy
    phần tử [0] làm khoá thì 1 keyword bị xé thành 2 dòng số liệu khác nhau — mà khoá
    SQLite là (keyword, snap_date) nên dòng sau ĐÈ dòng trước, mất dữ liệu im lặng.
    """
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()
    q = """SELECT v.video_id, v.keywords, v.niches, v.published_at, v.first_seen,
                  v.channel_id, s.views
           FROM video v JOIN video_snapshot s
             ON s.video_id = v.video_id AND s.snap_date = ?
           WHERE v.published_at >= ?"""
    buckets: dict[str, dict] = {}
    for r in con.execute(q, (snap, cutoff)):
        for kw in (r["keywords"] or "").split("|"):
            if not kw:
                continue
            b = buckets.setdefault(kw, {"views": [], "channels": set()})
            b["views"].append(r["views"] or 0)
            b["channels"].add(r["channel_id"])

    new_ch = _new_channels_by_keyword(con, snap, days)
    rows = []
    for kw, b in buckets.items():
        vals = sorted(b["views"])
        rows.append({
            "keyword": kw, "niche": kw_niche.get(kw, "?"),
            "n_new_7d": len(vals),
            "median_views_7d": int(statistics.median(vals)) if vals else 0,
            "p90_views_7d": int(vals[min(len(vals) - 1, int(0.9 * len(vals)))]) if vals else 0,
            "n_new_channels": new_ch.get(kw, 0),
        })
    return rows


def _new_channels_by_keyword(con, snap: str, days: int) -> dict[str, int]:
    cutoff = (dt.date.fromisoformat(snap) - dt.timedelta(days=days)).isoformat()
    q = """SELECT v.keywords, v.niches, c.channel_id FROM channel c
           JOIN video v ON v.channel_id = c.channel_id
           WHERE c.ch_age_days IS NOT NULL AND c.ch_age_days <= 180 AND c.first_seen >= ?"""
    out: dict[str, set] = {}
    for r in con.execute(q, (cutoff,)):
        for kw in (r["keywords"] or "").split("|"):
            if kw:
                out.setdefault(kw, set()).add(r["channel_id"])
    return {k: len(v) for k, v in out.items()}


def enrich_with_history(con: sqlite3.Connection, rows: list[dict], snap: str,
                        lookback: int = 7) -> list[dict]:
    """Thêm demand_delta_pct (so với `lookback` ngày trước) + content_gap + verdict."""
    prev_date = (dt.date.fromisoformat(snap) - dt.timedelta(days=lookback)).isoformat()
    prev = {r["keyword"]: r["median_views_7d"] for r in con.execute(
        "SELECT keyword, median_views_7d FROM keyword_snapshot WHERE snap_date = ?",
        (prev_date,))}

    by_niche: dict[str, list[dict]] = {}
    for r in rows:
        by_niche.setdefault(r["niche"], []).append(r)

    for group in by_niche.values():
        zd = _z([float(r["median_views_7d"]) for r in group])   # cầu
        zs = _z([float(r["n_new_7d"]) for r in group])          # cung
        for i, r in enumerate(group):
            p = prev.get(r["keyword"])
            r["demand_delta_pct"] = (round(100 * (r["median_views_7d"] - p) / p, 1)
                                     if p else None)
            r["content_gap"] = round(zd[i] - zs[i], 2)
            r["verdict"] = _verdict(r)
    return rows


def _verdict(r: dict) -> str:
    gap, delta, n = r["content_gap"], r.get("demand_delta_pct"), r["n_new_7d"]
    if gap >= 1.0 and n >= 3:
        return "🎯 CONTENT GAP — cầu cao, ít người làm"
    if delta is not None and delta >= 50:
        return "📈 ĐANG TĂNG MẠNH"
    if r["n_new_channels"] >= 3:
        return "🌱 NHIỀU KÊNH MỚI NHẢY VÀO"
    if gap <= -1.0:
        return "🥵 BÃO HOÀ — nhiều video, view thấp"
    return "—"
