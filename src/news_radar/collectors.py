# -*- coding: utf-8 -*-
"""Tải 5 nguồn trend (keyless) → parsers → ghi bảng signal. Một lượt = một snap_ts.
Lỗi 1 nguồn KHÔNG làm hỏng lượt: ghi vào `errors` và đi tiếp (đã dính: NHK 301, Reddit 403)."""
from __future__ import annotations

import time

import requests

from . import parsers as P
from . import store

URLS = {
    "google_trends": "https://trends.google.com/trending/rss?geo={geo}",
    "google_news": "https://news.google.com/rss?hl={hl}&gl={geo}&ceid={geo}:{hl}",
    "yahoo_ranking": "https://news.yahoo.co.jp/ranking/access/news",
    "yahoo_ranking_domestic": "https://news.yahoo.co.jp/ranking/access/news/domestic",
    "x_trends24": "https://trends24.in/japan/",
    "x_getdaytrends": "https://getdaytrends.com/japan/",
}


def _get(url: str, cfg: dict) -> str:
    h = cfg["http"]
    r = requests.get(url, headers={"User-Agent": h["user_agent"], "Accept-Language": "ja,en;q=0.5"},
                     timeout=h["timeout_s"])
    r.raise_for_status()
    r.encoding = r.encoding or "utf-8"
    return r.text


def collect_all(cfg: dict, con, log=print, dry_run: bool = False) -> dict:
    """Trả {source: n_signal} + 'errors'. dry_run = chỉ parse, không ghi DB."""
    m, src = cfg["market"], cfg["sources"]
    snap_ts = int(time.time())
    result: dict = {"snap_ts": snap_ts, "errors": {}}
    jobs = []
    if src.get("google_trends"):
        jobs.append(("google_trends", URLS["google_trends"].format(**m), P.parse_google_trends))
    if src.get("google_news"):
        jobs.append(("google_news", URLS["google_news"].format(**m), P.parse_google_news))
    if src.get("yahoo_ranking"):
        jobs.append(("yahoo_ranking", URLS["yahoo_ranking"], lambda t: P.parse_yahoo_ranking(t, "news")))
        jobs.append(("yahoo_ranking", URLS["yahoo_ranking_domestic"], lambda t: P.parse_yahoo_ranking(t, "domestic")))
    if src.get("x_trends24"):
        jobs.append(("x_trends24", URLS["x_trends24"], P.parse_trends24))
    if src.get("x_getdaytrends"):
        jobs.append(("x_getdaytrends", URLS["x_getdaytrends"], P.parse_getdaytrends))

    for name, url, parse in jobs:
        try:
            rows = parse(_get(url, cfg))
        except Exception as e:  # noqa: BLE001 — 1 nguồn hỏng không được giết cả lượt
            result["errors"][name] = f"{type(e).__name__}: {str(e)[:120]}"
            log(f"  ✗ {name}: {result['errors'][name]}")
            continue
        if name == "yahoo_ranking":  # 2 trang Yahoo: trang tổng ghi trước, trang domestic không đè hạng
            # trang domestic: giữ top 20, hạng +10 để không ngang hàng với hạng tổng (1 domestic ≠ 1 tổng)
            rows = [dict(r, rank=r["rank"] + 10) if r["extra"].get("category") == "domestic" else r
                    for r in rows if not (r["extra"].get("category") == "domestic" and r["rank"] > 20)]
        n = len(rows) if dry_run else store.insert_signals(con, rows, snap_ts)
        result[name] = result.get(name, 0) + n
        log(f"  ✓ {name}: {len(rows)} keyword" + ("" if dry_run else f" (ghi mới {n})"))
        time.sleep(0.8)
    return result
