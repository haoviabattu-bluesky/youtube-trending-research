# -*- coding: utf-8 -*-
"""Manga breakout channel hunt (nhiệm vụ 2026-09-25, xem pasted_content trong chat).

Quét seed keyword 漫画+職場/退職/薬剤師/... qua InnerTube (keyless, nhiều window/page),
enrich views/subs/uploads qua YouTube Data API, tính VSR/VPD/RVM, lọc kênh nhỏ
(100-5000 sub, watchlist 5k-10k) có tín hiệu breakout thật (không phải 1 video ăn may).

    py -3.13 -X utf8 src/manga_breakout_hunt.py --round 1
    py -3.13 -X utf8 src/manga_breakout_hunt.py --round 2 --extra-kw "漫画 薬剤師 理不尽,漫画 因果応報"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from innertube import InnerTube, BotCheckError, ProxyError
from proxy_pool import ProxyPool, load_proxies
from ytapi import YouTubeAPI

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "manga_breakout_hunt"

SEED_KEYWORDS = [
    "漫画 仕事", "漫画 職場", "漫画 薬剤師", "漫画 退職", "漫画 転職",
    "漫画 定年", "漫画 人間関係", "漫画 老後", "漫画 会社", "漫画 新人",
    "漫画 上司", "漫画 因果応報", "漫画 スカッと", "漫画 ざまぁ",
    "漫画 人生逆転", "漫画 感動",
]

TOPIC_WORDS = ("職場", "退職", "転職", "口ぐせ", "上司", "パワハラ", "仕事", "社会人",
               "ブラック企業", "同僚", "クビ", "薬剤師", "部下", "モラハラ", "会社",
               "定年", "老後", "因果応報", "スカッと", "ざまぁ", "人生逆転", "人間関係",
               "新人", "看護師", "介護", "嫁", "姑", "義母", "義実家")

MIN_DURATION_S = 180  # loại Shorts/trailer
SUB_MAIN_MAX = 5000
SUB_WATCH_MAX = 10000


def discover(it: InnerTube, pool: ProxyPool, keywords: list[str], pages: int) -> dict[str, dict]:
    seen: dict[str, dict] = {}
    for kw in keywords:
        for window in ("today", "week", "month"):
            for attempt in range(3):
                try:
                    rows = it.search(kw, window=window, pages=pages)
                    break
                except (BotCheckError, ProxyError) as e:
                    print(f"  [{kw}/{window}] {type(e).__name__}, đổi proxy...")
                    it.set_proxy(pool.next())
                    time.sleep(3)
            else:
                print(f"  [{kw}/{window}] bỏ qua sau 3 lần lỗi")
                continue
            for r in rows:
                seen.setdefault(r["video_id"], r)
            print(f"  [{kw}/{window}] +{len(rows)} → tổng {len(seen)} id duy nhất")
    return seen


def is_manga_topic(title: str) -> bool:
    return "漫画" in title and any(w in title for w in TOPIC_WORDS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--pages", type=int, default=4)
    ap.add_argument("--extra-kw", default="", help="comma-separated keyword bổ sung (round 2+)")
    ap.add_argument("--no-seeds", action="store_true", help="chỉ chạy --extra-kw, bỏ 16 seed cũ (đỡ trùng lặp)")
    ap.add_argument("--baseline-count", type=int, default=12)
    args = ap.parse_args()

    load_dotenv(ROOT / "config" / ".env")
    api = YouTubeAPI(os.environ["YOUTUBE_API_KEY"])
    pool = ProxyPool(load_proxies(ROOT / "config" / "proxies.txt"))
    it = InnerTube(hl="ja", gl="JP", proxy_url=pool.next())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    keywords = [] if args.no_seeds else list(SEED_KEYWORDS)
    if args.extra_kw:
        keywords += [k.strip() for k in args.extra_kw.split(",") if k.strip()]

    print(f"=== Round {args.round}: {len(keywords)} keyword ===")
    seen = discover(it, pool, keywords, args.pages)

    manga_rows = {vid: r for vid, r in seen.items() if is_manga_topic(r["title"])}
    print(f"\n{len(manga_rows)}/{len(seen)} video khớp chủ đề manga công sở/đời sống")

    stats = api.videos_batch(list(manga_rows.keys()))
    print(f"Data API videos.list: {api.used} quota dùng")

    now = dt.datetime.now(dt.timezone.utc)
    candidates = []
    for vid, meta in stats.items():
        if meta["duration_s"] < MIN_DURATION_S:
            continue
        try:
            born = dt.datetime.fromisoformat(meta["published_at"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            continue
        age_days = max((now - born).total_seconds() / 86400, 0.5)
        candidates.append({
            "video_id": vid, "title": meta["title_api"], "channel_id": meta["channel_id_api"],
            "views": meta["views"], "age_days": round(age_days, 1),
            "published_at": meta["published_at"], "duration_s": meta["duration_s"],
            "vpd": round(meta["views"] / age_days, 1),
            "keyword": manga_rows[vid]["keyword"],
        })

    chan_ids = sorted({c["channel_id"] for c in candidates})
    chans = api.channels_batch(chan_ids)
    print(f"Data API channels.list: {api.used} quota dùng, {len(chans)} kênh")

    for c in candidates:
        ch = chans.get(c["channel_id"], {})
        c["subs"] = ch.get("subs", 0)
        c["ch_video_count"] = ch.get("ch_video_count", 0)
        c["ch_age_days"] = ch.get("ch_age_days")
        c["channel_title"] = ch.get("channel_title", "")
        c["ch_country"] = ch.get("ch_country", "")
        c["uploads_playlist"] = ch.get("uploads_playlist", "")
        c["vsr"] = round(c["views"] / c["subs"], 2) if c["subs"] else None

    # giữ kênh trong khung sub (main <=5000, watchlist <=10000); loại kênh 0 sub bất thường lớn
    kept = [c for c in candidates if c["subs"] and c["subs"] <= SUB_WATCH_MAX]
    print(f"{len(kept)}/{len(candidates)} video thuộc kênh <= {SUB_WATCH_MAX} sub")

    by_channel: dict[str, list[dict]] = {}
    for c in kept:
        by_channel.setdefault(c["channel_id"], []).append(c)

    print(f"{len(by_channel)} kênh duy nhất — lấy baseline (12 video gần nhất, bỏ <7 ngày)...")
    channel_report = []
    for i, (cid, vids) in enumerate(by_channel.items(), 1):
        up = vids[0]["uploads_playlist"]
        median_views = None
        if up:
            try:
                base = api.baseline_videos(up, want=args.baseline_count, min_age_days=7, fetch=24)
                views_list = sorted(v["views"] for v in base)
                if views_list:
                    n = len(views_list)
                    median_views = (views_list[n // 2] if n % 2 else
                                     (views_list[n // 2 - 1] + views_list[n // 2]) / 2)
            except Exception as e:
                print(f"    [{cid}] baseline lỗi: {e}")
        subs = vids[0]["subs"]
        breakout_count = sum(1 for v in vids if subs and v["views"] >= 5 * subs)
        for v in vids:
            v["rvm"] = round(v["views"] / median_views, 2) if median_views else None
        channel_report.append({
            "channel_id": cid, "channel_title": vids[0]["channel_title"], "subs": subs,
            "ch_video_count": vids[0]["ch_video_count"], "ch_age_days": vids[0]["ch_age_days"],
            "ch_country": vids[0]["ch_country"],
            "recent_median_views": median_views,
            "videos_found": sorted(vids, key=lambda v: -v["views"]),
            "breakout_count_in_sample": breakout_count,
        })
        if i % 10 == 0:
            print(f"    ...{i}/{len(by_channel)} kênh")

    channel_report.sort(key=lambda c: -(c["videos_found"][0]["vsr"] or 0))

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = OUT_DIR / f"round{args.round}_{ts}.json"
    out.write_text(json.dumps(channel_report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nĐã ghi {len(channel_report)} kênh → {out}")
    print(f"Quota Data API dùng tổng: {api.used}")

    print("\n=== TOP 25 theo VSR video mạnh nhất ===")
    for c in channel_report[:25]:
        top = c["videos_found"][0]
        print(f"  subs={c['subs']:>5} vsr={top['vsr']:>6} vpd={top['vpd']:>7.0f} "
              f"age={top['age_days']:>5}d n_vid={len(c['videos_found'])} :: {c['channel_title']} :: {top['title'][:60]}")


if __name__ == "__main__":
    main()
