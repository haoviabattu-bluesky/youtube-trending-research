# -*- coding: utf-8 -*-
"""Săn video manga NGHỀ NGHIỆP/CÔNG SỞ Nhật kiểu @iyaku_labo (漫画+口ぐせ/退職/パワハラ...).

Điều kiện lọc (user chốt 2026-09-24):
  - video đăng <10 ngày (age_days <= 10)
  - view >= 20.000
  - đúng thể loại manga công việc (khớp từ khoá 漫画 + có ít nhất 1 từ chủ đề công sở
    trong tiêu đề, loại phim/anime dài không liên quan)
  - bỏ Shorts/trailer (duration_s < 180s) — chỉ lấy video kể chuyện đầy đủ

Chạy 1 lượt quét toàn bộ từ khoá; CÓ kết quả khớp đủ điều kiện thì DỪNG NGAY và ghi
file + in bảng. CHƯA có thì tự ngủ `--interval` giây rồi quét lại vòng khác, lặp tới
khi tìm được (mặc định vô hạn — Ctrl+C để huỷ tay).

    py -3.13 -X utf8 src/find_workplace_manga.py --interval 1800
    py -3.13 -X utf8 src/find_workplace_manga.py --once          # chỉ 1 vòng, không lặp
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path

from dotenv import load_dotenv
import os

from innertube import InnerTube, BotCheckError, ProxyError
from proxy_pool import ProxyPool, load_proxies
from ytapi import YouTubeAPI

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "find_workplace_manga"

KEYWORDS = [
    "漫画 職場", "漫画 退職", "漫画 転職", "口ぐせ 漫画", "漫画 上司",
    "漫画 パワハラ", "漫画 仕事 辞める", "漫画 社会人", "漫画 ブラック企業",
    "漫画 同僚", "漫画 クビ", "漫画 薬剤師", "漫画 部下", "漫画 モラハラ 会社",
]
# ít nhất 1 cụm này phải xuất hiện trong tiêu đề mới tính là đúng ngách (tránh lẫn
# manga tình yêu/isekai chỉ trùng chữ 漫画 với từ khoá phụ)
TOPIC_WORDS = ("職場", "退職", "転職", "口ぐせ", "上司", "パワハラ", "仕事", "社会人",
               "ブラック企業", "同僚", "クビ", "薬剤師", "部下", "モラハラ", "会社")

MIN_VIEWS = 20_000
MAX_AGE_DAYS = 10
MIN_DURATION_S = 180


def scan_once(it: InnerTube, api: YouTubeAPI, pool: ProxyPool) -> list[dict]:
    seen_ids: dict[str, dict] = {}
    for kw in KEYWORDS:
        for window in ("today", "week"):
            for attempt in range(3):
                try:
                    rows = it.search(kw, window=window, pages=2)
                    break
                except (BotCheckError, ProxyError) as e:
                    print(f"  [{kw}/{window}] {type(e).__name__}, đổi proxy, thử lại...")
                    it.set_proxy(pool.next())
                    time.sleep(3)
            else:
                print(f"  [{kw}/{window}] bỏ qua sau 3 lần lỗi")
                continue
            for r in rows:
                seen_ids.setdefault(r["video_id"], r)
            print(f"  [{kw}/{window}] +{len(rows)} video (tổng {len(seen_ids)} id duy nhất)")

    if not seen_ids:
        return []

    stats = api.videos_batch(list(seen_ids.keys()))
    now = dt.datetime.now(dt.timezone.utc)
    hits = []
    for vid, meta in stats.items():
        try:
            born = dt.datetime.fromisoformat(meta["published_at"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            continue
        age_days = (now - born).total_seconds() / 86400
        title = meta.get("title_api", "")
        if (age_days <= MAX_AGE_DAYS
                and meta["views"] >= MIN_VIEWS
                and meta["duration_s"] >= MIN_DURATION_S
                and "漫画" in title
                and any(w in title for w in TOPIC_WORDS)):
            hits.append({
                "video_id": vid, "title": title, "channel_id": meta["channel_id_api"],
                "views": meta["views"], "age_days": round(age_days, 1),
                "published_at": meta["published_at"], "duration_s": meta["duration_s"],
                "keyword": seen_ids[vid]["keyword"], "url": f"https://www.youtube.com/watch?v={vid}",
                "channel_url": f"https://www.youtube.com/channel/{meta['channel_id_api']}",
            })
    hits.sort(key=lambda h: -h["views"])
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=1800, help="giây nghỉ giữa các vòng quét khi chưa có kết quả")
    ap.add_argument("--once", action="store_true", help="chỉ quét 1 vòng rồi thoát dù có hay không")
    ap.add_argument("--max-rounds", type=int, default=0, help="0 = vô hạn")
    args = ap.parse_args()

    load_dotenv(ROOT / "config" / ".env")
    api = YouTubeAPI(os.environ["YOUTUBE_API_KEY"])
    pool = ProxyPool(load_proxies(ROOT / "config" / "proxies.txt"))
    it = InnerTube(hl="ja", gl="JP", proxy_url=pool.next())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    round_no = 0
    while True:
        round_no += 1
        print(f"\n=== Vòng {round_no} — {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        hits = scan_once(it, api, pool)
        if hits:
            ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            out = OUT_DIR / f"found_{ts}.json"
            out.write_text(json.dumps(hits, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"\n★ TÌM ĐƯỢC {len(hits)} video khớp điều kiện (<{MAX_AGE_DAYS} ngày, >={MIN_VIEWS} view):")
            for h in hits:
                print(f"  {h['views']:>7} view · {h['age_days']:>4}d · {h['title']}")
                print(f"    {h['url']}  (kênh: {h['channel_url']})")
            print(f"\nĐã ghi: {out}")
            return
        print(f"  Chưa có video nào khớp đủ điều kiện.")
        if args.once or (args.max_rounds and round_no >= args.max_rounds):
            print("Dừng (--once/--max-rounds), chưa tìm được.")
            return
        print(f"  Ngủ {args.interval}s rồi quét lại...")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
