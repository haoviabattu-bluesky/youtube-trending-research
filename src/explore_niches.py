# -*- coding: utf-8 -*-
"""Khảo sát NGÁCH ứng viên — chấm điểm ngách, không chấm video.

Khác `run_daily.py`: ở đó câu hỏi là "hôm nay video nào đáng xem", ở đây là
"NGÁCH NÀO đáng nhảy vào". Chỉ số quyết định là **kênh mới có sống được không**,
chứ không phải ngách đó có bao nhiêu view (ngách to thường là ngách đã bị chiếm).

  py -3.13 -X utf8 src/explore_niches.py --out data/explore.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
import score as sc                                              # noqa: E402
from enrich import Enricher                                     # noqa: E402
from innertube import BotCheckError, InnerTube                  # noqa: E402
from ytapi import QuotaExhausted, YouTubeAPI                    # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")
LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731

# Ngưỡng "kênh mới sống được" — dùng chung cho mọi ngách để so sánh công bằng
NEW_DAYS = 180
MIN_SUBS = 300
HIT_VIEWS = 50_000
CONSISTENT = 3.0          # ch_mult >= 3 = kênh có công thức, không phải ăn may


def survey(name: str, niche: dict, api, windows, per_niche: int) -> dict:
    it = InnerTube(hl=niche.get("hl", "ja"), gl=niche.get("gl", "JP"))
    found: dict[str, dict] = {}
    for kw in niche["keywords"]:
        for w in windows:
            try:
                for r in it.search(kw, w):
                    found.setdefault(r["video_id"], r)
            except BotCheckError:
                raise
            except Exception as e:
                LOG(f"    ! {kw}[{w}]: {type(e).__name__}")
    enr = Enricher(api, it)
    rows = enr.build_rows(list(found.values()), name)

    # baseline cho các kênh ỨNG VIÊN: mới, đủ sub, có video kéo được view
    cand = {}
    for r in rows:
        if (r.get("subs") or 0) < MIN_SUBS or r["views"] < 20_000:
            continue
        age = r.get("ch_age_days")
        if age is None or age > NEW_DAYS:
            continue
        c = cand.get(r["channel_id"])
        if c is None or r["views"] > c["views"]:
            cand[r["channel_id"]] = r
    ranked = sorted(cand.values(), key=lambda r: r["views"], reverse=True)[:per_niche]

    base = {}
    if api:
        for r in ranked:
            try:
                vids = api.baseline_videos(r.get("uploads_playlist") or f"UU{r['channel_id'][2:]}",
                                           12, 7)
                if vids:
                    base[r["channel_id"]] = sc.channel_baseline_from_videos(vids, {"breakout_ratio": 3.0})
            except QuotaExhausted:
                LOG("    ! hết quota, dừng baseline")
                break
            except Exception:
                pass

    winners = []
    for r in ranked:
        b = base.get(r["channel_id"])
        if not b or not b["median_views"]:
            continue
        r["ch_mult"] = round(b["median_views"] / max(r.get("subs") or 1, MIN_SUBS), 2)
        r["ch_median"] = b["median_views"]
        winners.append(r)

    consistent = [r for r in winners if r["ch_mult"] >= CONSISTENT]
    consistent.sort(key=lambda r: r["ch_mult"], reverse=True)
    hits = [r for r in rows if r["views"] >= HIT_VIEWS
            and (r.get("ch_age_days") or 9999) <= NEW_DAYS
            and (r.get("subs") or 0) >= MIN_SUBS]
    fresh_views = [r["views"] for r in rows if (r.get("age_hours") or 9e9) <= 24 * 30]

    return {
        "niche": name,
        "label": niche.get("label", ""),
        "ai_fit": niche.get("ai_fit", ""),
        "videos_seen": len(rows),
        "channels_seen": len({r["channel_id"] for r in rows}),
        "new_ch_candidates": len(cand),
        "new_ch_with_hit": len({r["channel_id"] for r in hits}),
        "consistent_new_ch": len(consistent),
        "median_ch_mult": round(statistics.median([r["ch_mult"] for r in winners]), 2) if winners else 0,
        "top_ch_mult": round(max([r["ch_mult"] for r in winners], default=0), 1),
        "median_views_30d": int(statistics.median(fresh_views)) if fresh_views else 0,
        "p90_views_30d": int(sorted(fresh_views)[int(0.9 * len(fresh_views))]) if fresh_views else 0,
        "supply_30d": len(fresh_views),
        "best": max(consistent or winners or rows, key=lambda r: r.get("ch_mult", 0)
                    if (consistent or winners) else r["views"], default=None),
        "_winners": consistent,
    }


def entry_score(s: dict, allr: list[dict]) -> float:
    """Điểm DỄ VÀO: kênh mới sống được nhiều + kênh thắng đều đặn + cầu cao, phạt cung dày."""
    def z(key):
        vals = [x[key] for x in allr]
        mu = statistics.mean(vals)
        sd = statistics.pstdev(vals) or 1.0
        return (s[key] - mu) / sd
    return round(50 + 12 * (0.34 * z("consistent_new_ch") + 0.26 * z("new_ch_with_hit")
                            + 0.22 * z("median_ch_mult") + 0.18 * z("median_views_30d")), 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", default="")
    ap.add_argument("--out", default=str(ROOT / "data" / "explore.csv"))
    ap.add_argument("--detail", action="store_true",
                    help="in danh sách kênh MỚI + ĐỀU ĐẶN của từng ngách (để chọn kênh clone)")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(ROOT / "config" / "explore.yaml", encoding="utf-8"))
    key = os.getenv("YOUTUBE_API_KEY", "")
    api = YouTubeAPI(key) if key else None
    names = [n.strip() for n in args.niche.split(",") if n.strip()] or list(cfg["niches"])

    t0 = time.time()
    out = []
    for i, name in enumerate(names, 1):
        n = cfg["niches"][name]
        LOG(f"[{i}/{len(names)}] {name} — {n['label']}")
        try:
            s = survey(name, n, api, cfg["defaults"]["windows"],
                       cfg["defaults"]["baseline_per_niche"])
        except BotCheckError as e:
            LOG(f"!! BOT-CHECK: {e}")
            return 2
        out.append(s)
        LOG(f"    {s['videos_seen']} video · {s['new_ch_with_hit']} kênh mới có hit · "
            f"{s['consistent_new_ch']} kênh ĐỀU ĐẶN · median view 30d = {s['median_views_30d']:,}")

    for s in out:
        s["entry_score"] = entry_score(s, out)
    out.sort(key=lambda s: s["entry_score"], reverse=True)

    cols = ["entry_score", "niche", "label", "consistent_new_ch", "new_ch_with_hit",
            "median_ch_mult", "top_ch_mult", "median_views_30d", "p90_views_30d",
            "supply_30d", "videos_seen", "channels_seen", "ai_fit"]
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["best_channel", "best_ch_mult", "best_title"])
        w.writeheader()
        for s in out:
            b = s.get("best") or {}
            w.writerow({**{c: s[c] for c in cols},
                        "best_channel": b.get("channel", ""),
                        "best_ch_mult": b.get("ch_mult", ""),
                        "best_title": b.get("title", "")})

    print(f"\n{'ĐIỂM':>5} {'ĐỀU':>4} {'HIT':>4} {'chMult':>7} {'median30d':>10} {'cung':>5}  NGÁCH")
    for s in out:
        print(f"{s['entry_score']:5.1f} {s['consistent_new_ch']:4} {s['new_ch_with_hit']:4} "
              f"{s['median_ch_mult']:7.1f} {s['median_views_30d']:10,} {s['supply_30d']:5}  "
              f"{s['label'][:44]}")
        b = s.get("best") or {}
        if b:
            print(f"        ↳ {b.get('channel', '')[:26]} · {b.get('ch_age_days')}d · "
                  f"{(b.get('subs') or 0):,}sub · median {(b.get('ch_median') or 0):,}v "
                  f"· ch_mult {b.get('ch_mult')}")
    if args.detail:
        for s in out:
            print(f"\n### {s['label']}   (điểm vào ngách {s['entry_score']})")
            print(f"    {'TUỔI':>5} {'SUBS':>8} {'MEDIAN':>9} {'chMult':>7}  KÊNH MỚI + ĐỀU ĐẶN")
            for r in s["_winners"][:6]:
                print(f"    {r['ch_age_days']:5}d {(r.get('subs') or 0):8,} "
                      f"{r['ch_median']:9,} {r['ch_mult']:7.1f}  {r['channel'][:36]}")
                print(f"           ↳ {r['title'][:76]}")
    if api:
        LOG(f"\n[quota] {api.used} / 10000")
    LOG(f"[done] {time.time() - t0:.0f}s → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
