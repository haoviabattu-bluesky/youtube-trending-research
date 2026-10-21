# -*- coding: utf-8 -*-
"""Săn kênh NHỎ bứt phá, mọi ngách/ngôn ngữ (yêu cầu 2026-10-04).

Cổng cứng: sub < 30.000 · tổng video công khai < 20 · có >=1 video đăng trong 14 ngày gần nhất
đạt > 100.000 view. Faceless KHÔNG kiểm tự động được — bước xem thumbnail làm tay sau đó.
Loại kênh đã từng báo (UC… xuất hiện trong docs/ hoặc data/**/*.json).

    py -3.13 -X utf8 src/small_channel_outlier_hunt.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import statistics as st
import time
from pathlib import Path

from dotenv import load_dotenv

from innertube import InnerTube, BotCheckError, ProxyError
from proxy_pool import ProxyPool, load_proxies
from ytapi import YouTubeAPI

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "small_outlier_hunt"
SUB_MAX, VID_MAX, VIEWS_MIN, DAYS = 30_000, 20, 100_000, 14

# (hl, gl, keywords)
KEYWORDS = [
    ("ja", "JP", [
        # người già / hậu nghỉ hưu
        "老後 漫画", "定年 後悔", "シニア 感動 物語", "70代 人生", "年金 老後 現実", "老後 破産", "老後 孤独", "熟年離婚",
        "定年後 夫婦", "高齢者 実話", "おばあちゃん 感動", "おじいちゃん 感動", "老人ホーム 実話", "終活 物語", "孫 祖母 感動",
        "60代 後悔", "80代 人生訓", "人生の最期 物語", "年金 受給 現実", "介護 実話 漫画",
        # trinh thám / manga
        "探偵 漫画", "推理 漫画 アニメ", "ミステリー 漫画", "名探偵 物語", "密室 事件 推理", "殺人事件 推理 アニメ",
        "刑事 物語 漫画", "迷宮入り 事件", "未解決事件 解説", "犯罪 実話 アニメ", "怪事件 ゆっくり解説",
        # khác (faceless)
        "都市伝説", "スカッと 漫画", "嫁姑 漫画", "歴史 ミステリー", "怖い話 アニメ", "人生 逆転 物語", "感動 実話 漫画",
        "雑学 解説", "ナレーション ドキュメンタリー", "ゆっくり解説 歴史", "戦国 裏話", "昭和 実話", "実話 ナレーション 漫画",
        "不思議な話 朗読", "朗読 感動", "泣ける話 アニメ", "復讐 漫画 実話", "職場 漫画 実話", "お金 老後 解説 アニメ",
        "経済 衰退 解説", "日本 消滅 解説", "世にも奇妙 風 物語", "ホラー 実話 漫画", "ブラック企業 漫画",
    ]),
]


def discover(pool: ProxyPool) -> dict[str, dict]:
    seen: dict[str, dict] = {}
    for hl, gl, kws in KEYWORDS:
        it = InnerTube(hl=hl, gl=gl, proxy_url=pool.next())
        for kw in kws:
            for window in ("week", "month"):
                for _ in range(3):
                    try:
                        rows = it.search(kw, window=window, pages=3)
                        break
                    except (BotCheckError, ProxyError, RuntimeError) as e:
                        print(f"  [{kw}/{window}] {type(e).__name__}, đổi proxy")
                        it.set_proxy(pool.next())
                        time.sleep(3)
                else:
                    continue
                for r in rows:
                    seen.setdefault(r["video_id"], r)
                print(f"  [{hl}] {kw}/{window}: +{len(rows)} → {len(seen)}")
    return seen


def known_channels() -> set[str]:
    ids: set[str] = set()
    pat = re.compile(r"UC[\w-]{22}")
    for sub, glob in (("docs", "*.*"), ("data", "**/*.json"), ("lanes", "**/*.yaml")):
        for p in (ROOT / sub).glob(glob):
            if p.is_file() and p.stat().st_size < 30_000_000 and "small_outlier_hunt" not in str(p):
                try:
                    ids |= set(pat.findall(p.read_text(encoding="utf-8", errors="ignore")))
                except OSError:
                    pass
    return ids


def pdt(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    import sys
    if len(sys.argv) > 1:
        KEYWORDS[:] = [("ja", "JP", Path(sys.argv[1]).read_text(encoding="utf-8").split())] if False else [("ja", "JP", [l.strip() for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()])]
    load_dotenv(ROOT / "config" / ".env")
    api = YouTubeAPI(os.environ["YOUTUBE_API_KEY"])
    pool = ProxyPool(load_proxies(ROOT / "config" / "proxies.txt"))
    OUT.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)

    seen = discover(pool)
    print(f"\n{len(seen)} video duy nhất")
    vids = api.videos_batch(list(seen))
    hot = {v: m for v, m in vids.items()
           if m["views"] > VIEWS_MIN and (now - pdt(m["published_at"])).days <= DAYS and m["duration_s"] >= 180}
    print(f"{len(hot)} video >{VIEWS_MIN} view trong {DAYS} ngày")
    kana = re.compile(r"[぀-ヿ]")
    hot = {v: m for v, m in hot.items() if kana.search(m["title_api"])}
    print(f"{len(hot)} video có tiếng Nhật (kana)")
    chans = api.channels_batch(sorted({m["channel_id_api"] for m in hot.values()}))
    near = [{"channel_id": c, "title": d["channel_title"], "subs": d["subs"], "videos": d["ch_video_count"],
             "hot": [(m["title_api"], m["views"]) for m in hot.values() if m["channel_id_api"] == c]}
            for c, d in chans.items() if d["subs"] < 100_000]
    (OUT / f"near_{dt.datetime.now():%H%M%S}.json").write_text(json.dumps(near, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = {c: d for c, d in chans.items() if 0 < d["subs"] < SUB_MAX and d["ch_video_count"] < VID_MAX}
    old = known_channels()
    fresh = {c: d for c, d in ok.items() if c not in old}
    print(f"{len(chans)} kênh → {len(ok)} qua cổng sub/video → {len(fresh)} chưa từng báo")

    report = []
    for cid, d in fresh.items():
        allv = api.videos_batch(api.recent_uploads(d["uploads_playlist"], 50))
        rows = []
        for vid, m in allv.items():
            age = max((now - pdt(m["published_at"])).total_seconds() / 86400, 0.5)
            rows.append({"id": vid, "title": m["title_api"], "views": m["views"], "age": round(age, 1),
                         "dur": m["duration_s"], "vpd": round(m["views"] / age), "lang": m["default_language"]})
        rows.sort(key=lambda r: -r["views"])
        tot = sum(r["views"] for r in rows) or 1
        report.append({
            "channel_id": cid, "title": d["channel_title"], "subs": d["subs"], "videos": len(rows),
            "country": d["ch_country"], "ch_age_days": d["ch_age_days"],
            "total_views": tot, "median_views": st.median(r["views"] for r in rows),
            "top1_share": round(rows[0]["views"] / tot, 2), "hits_100k": sum(r["views"] > VIEWS_MIN for r in rows),
            "oldest_days": max(r["age"] for r in rows), "median_dur_s": st.median(r["dur"] for r in rows),
            "vsr_top": round(rows[0]["views"] / d["subs"], 1), "rows": rows,
        })
    report.sort(key=lambda c: -c["total_views"])
    out = OUT / f"hunt_{dt.datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {out}  (quota {api.used})")
    for c in report[:40]:
        print(f"subs={c['subs']:>6} n={c['videos']:>2} med={c['median_views']:>8.0f} top1={c['top1_share']:.0%} "
              f"hits={c['hits_100k']} old={c['oldest_days']:>5.0f}d {c['country']:>2} :: {c['title']} :: {c['rows'][0]['title'][:50]}")


if __name__ == "__main__":
    main()
