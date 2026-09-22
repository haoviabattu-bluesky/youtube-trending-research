# -*- coding: utf-8 -*-
"""Trend keyword hunter — tìm kênh SIÊU NHỎ đang ăn theo trend (khác luồng ngách cố định).

Khác `run_probe.py`: từ khoá KHÔNG lấy từ niches.yaml mà sinh ĐỘNG mỗi lần chạy bằng
YouTube Suggest API (keyless, verify 2026-09-11: cần ie=utf-8&oe=utf-8 mới ra JSON
tiếng Nhật đúng, thiếu 2 tham số này trả về mojibake) từ các seed kana rộng khắp âm
đầu tiếng Nhật, sau đó search InnerTube như luồng chính.

Tiêu chí ("key trend hunter", khác NEW_CHANNEL_HIT của luồng ngách — thêm TRẦN sub và
ĐẾM số video kênh mà luồng chính chưa có):
  subs < --max-subs, tổng video kênh trong [--min-videos, --max-videos], có video
  views >= --min-views.

Chạy:
  py -3.13 -X utf8 src/trend_hunter.py --seeds 20 --out data/trend_hunt.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from innertube import BotCheckError, InnerTube      # noqa: E402
from reup_filter import classify as classify_reup   # noqa: E402
from ytapi import YouTubeAPI                        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"

# Gojuon rải rác — đủ phủ nhiều âm đầu, không cần soạn chủ đề tay (chốt 2026-09-11:
# tự động mở rộng bằng autocomplete, không soạn danh sách ngách tĩnh).
KANA_SEEDS = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ"
                   "まみむめもやゆよらりるれろわん")


def suggest(seed: str, hl: str = "ja", gl: str = "JP", tries: int = 2) -> list[str]:
    """Gọi YouTube Suggest (keyless) — trả cụm đang được gõ nhiều cho seed này."""
    params = {"client": "firefox", "ds": "yt", "hl": hl, "gl": gl,
              "ie": "utf-8", "oe": "utf-8", "q": seed}
    for i in range(tries):
        try:
            r = requests.get(SUGGEST_URL, params=params, timeout=15)
            if r.status_code == 200:
                data = r.json()
                return [s for s in data[1] if isinstance(s, str)]
        except Exception:
            pass
        time.sleep(1)
    return []


def build_keyword_pool(seeds: list[str], per_seed: int, hl: str, gl: str) -> list[str]:
    pool: dict[str, None] = {}
    for i, seed in enumerate(seeds, 1):
        for sug in suggest(seed, hl, gl)[:per_seed]:
            pool.setdefault(sug, None)
        time.sleep(0.3)
        if i % 10 == 0:
            print(f"  ...suggest {i}/{len(seeds)} seed, {len(pool)} từ khoá", file=sys.stderr)
    return list(pool)


def discover(it: InnerTube, keywords: list[str], windows: list[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for i, kw in enumerate(keywords, 1):
        for w in windows:
            try:
                for row in it.search(kw, w):
                    found.setdefault(row["video_id"], row)
            except BotCheckError:
                raise
            except Exception as e:
                print(f"  ! {kw} [{w}]: {type(e).__name__} {e}", file=sys.stderr)
        if i % 20 == 0:
            print(f"  ...search {i}/{len(keywords)} từ khoá, {len(found)} video", file=sys.stderr)
    return found


def main() -> int:
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=20, help="số seed kana dùng (tối đa 46)")
    ap.add_argument("--per-seed", type=int, default=6, help="số gợi ý lấy mỗi seed")
    ap.add_argument("--windows", default="today,week")
    ap.add_argument("--max-subs", type=int, default=1000)
    ap.add_argument("--min-videos", type=int, default=3)
    ap.add_argument("--max-videos", type=int, default=5)
    ap.add_argument("--min-views", type=int, default=50_000)
    ap.add_argument("--no-classify", action="store_true",
                    help="bỏ qua bước LLM phân loại ORIGINAL/REUP/VLOG_PERSON")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    key = os.getenv("YOUTUBE_API_KEY", "")
    if not key:
        print("[lỗi] thiếu YOUTUBE_API_KEY trong config/.env", file=sys.stderr)
        return 2
    api = YouTubeAPI(key)

    print("[1/4] sinh từ khoá từ YouTube Suggest...", file=sys.stderr)
    kws = build_keyword_pool(KANA_SEEDS[: args.seeds], args.per_seed, "ja", "JP")
    print(f"[1/4] {len(kws)} từ khoá duy nhất", file=sys.stderr)

    print("[2/4] search InnerTube...", file=sys.stderr)
    it = InnerTube(hl="ja", gl="JP")
    windows = args.windows.split(",")
    try:
        found = discover(it, kws, windows)
    except BotCheckError as e:
        print(f"!! BOT-CHECK: {e}", file=sys.stderr)
        return 2
    print(f"[2/4] {len(found)} video / {len({r['channel_id'] for r in found.values()})} kênh",
          file=sys.stderr)

    # sơ loại theo view keyless trước khi tốn quota Data API
    rough = [r for r in found.values() if r["views_it"] >= args.min_views]
    print(f"[3/4] {len(rough)} video >= {args.min_views:,} view (thô, chưa enrich)",
          file=sys.stderr)

    ch_ids = list({r["channel_id"] for r in rough})
    chans = api.channels_batch(ch_ids)
    vids = api.videos_batch([r["video_id"] for r in rough])
    print(f"[3/4] quota dùng: {api.used}", file=sys.stderr)

    gold = []
    for r in rough:
        ch = chans.get(r["channel_id"])
        vd = vids.get(r["video_id"])
        if not ch or not vd:
            continue
        if not (0 < ch["subs"] < args.max_subs):
            continue
        if not (args.min_videos <= ch["ch_video_count"] <= args.max_videos):
            continue
        if vd["views"] < args.min_views:
            continue
        gold.append({**r, **ch, **vd})

    gold.sort(key=lambda x: x["views"], reverse=True)
    print(f"[4/4] {len(gold)} kênh khớp: sub<{args.max_subs}, "
          f"{args.min_videos}-{args.max_videos} video, view>={args.min_views:,}", file=sys.stderr)

    if not args.no_classify:
        print("[5/5] phân loại ORIGINAL/REUP/VLOG_PERSON bằng LLM...", file=sys.stderr)
        tags = classify_reup(gold, os.getenv("LLM_BASE_URL", ""),
                             os.getenv("LLM_API_KEY", ""), os.getenv("LLM_MODEL", ""))
        for r in gold:
            t = tags.get(r["video_id"], {})
            r["content_type"] = t.get("type", "?")
            r["why"] = t.get("why", "")
        if not tags:
            print("  (bỏ qua — thiếu LLM_API_KEY hoặc lỗi gọi model)", file=sys.stderr)

    out_path = Path(args.out) if args.out else ROOT / "data" / f"trend_hunt_{time.strftime('%Y%m%d_%H%M')}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["keyword", "channel", "channel_id", "subs", "ch_video_count", "ch_age_days",
              "video_id", "title_api", "views", "published_at", "content_type", "why"]
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(gold)
    print(f"[out] {out_path}", file=sys.stderr)

    for r in gold[:30]:
        tag = f"[{r['content_type']}] " if r.get("content_type") else ""
        print(f"  {tag}{r['subs']:>5}sub {r['ch_video_count']:>2}vid {r['views']:>8,}v  "
              f"{r['title_api'][:40]:40s} | {r['channel']}", file=sys.stderr)
        if r.get("why"):
            print(f"    lý do: {r['why']}", file=sys.stderr)
        print(f"    https://youtube.com/watch?v={r['video_id']}  "
              f"https://youtube.com/channel/{r['channel_id']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
