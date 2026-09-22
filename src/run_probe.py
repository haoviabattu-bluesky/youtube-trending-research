# -*- coding: utf-8 -*-
"""Phase 1 — PROBE: quét keyword → enrich → CSV. Sync, đơn luồng, không đụng Sheet.

Chạy:
  py -3.13 -X utf8 src/run_probe.py --niche jp_senior,jp_satori --limit-kw 60
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
from enrich import ROW_FIELDS, Enricher                       # noqa: E402
from innertube import BotCheckError, InnerTube                # noqa: E402
from ytapi import YouTubeAPI                                  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")


def load_niches() -> dict:
    with open(ROOT / "config" / "niches.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


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
        if i % 10 == 0:
            print(f"  ...{i}/{len(keywords)} keyword, {len(found)} video", file=sys.stderr)
    return found


def main() -> int:
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", default="jp_senior", help="danh sách ngăn cách bằng dấu phẩy")
    ap.add_argument("--limit-kw", type=int, default=0, help="0 = tất cả")
    ap.add_argument("--windows", default="", help="ghi đè lát thời gian, vd: today,week")
    ap.add_argument("--out", default="")
    ap.add_argument("--no-api", action="store_true", help="ép chạy keyless để test fallback")
    args = ap.parse_args()

    cfg = load_niches()
    defaults = cfg["defaults"]
    key = os.getenv("YOUTUBE_API_KEY", "")
    api = None if (args.no_api or not key) else YouTubeAPI(key)
    if api is None:
        print("[api] TẮT — chạy hoàn toàn keyless", file=sys.stderr)

    windows = args.windows.split(",") if args.windows else defaults["windows"]
    out_path = Path(args.out) if args.out else ROOT / "data" / f"probe_{time.strftime('%Y%m%d_%H%M')}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    t0 = time.time()
    for name in args.niche.split(","):
        name = name.strip()
        niche = cfg["niches"][name]
        kws = niche["keywords"][: args.limit_kw] if args.limit_kw else niche["keywords"]
        print(f"\n[{name}] {len(kws)} keyword × {len(windows)} lát — {niche['label']}", file=sys.stderr)
        it = InnerTube(hl=niche.get("hl", "ja"), gl=niche.get("gl", "JP"))
        try:
            found = discover(it, kws, windows)
        except BotCheckError as e:
            print(f"\n!! BOT-CHECK: {e}\n   → IP đang bị chặn, xem phase-01 §'Nếu Phase 1 FAIL'",
                  file=sys.stderr)
            return 2
        print(f"[discovery] {len(found)} video / "
              f"{len({r['channel_id'] for r in found.values()})} kênh", file=sys.stderr)
        tot = it.parse_ok + it.parse_fail
        print(f"[parse] ok={it.parse_ok} fail={it.parse_fail} "
              f"({100 * it.parse_ok / max(tot, 1):.1f}%)", file=sys.stderr)

        enr = Enricher(api, it)
        rows = enr.build_rows(list(found.values()), name)
        print(f"[enrich] {enr.stat}", file=sys.stderr)
        all_rows.extend(rows)

    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ROW_FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    if api:
        print(f"[quota] used={api.used} / 10000", file=sys.stderr)
    print(f"[out] {out_path} — {len(all_rows)} dòng, {time.time() - t0:.0f}s", file=sys.stderr)

    d = defaults
    gold = [r for r in all_rows
            if r["subs"] >= d["min_subs"]
            and (r["ch_age_days"] or 9999) <= d["new_channel_days"]
            and r["views"] >= d["new_channel_min_views"]
            and r["duration_s"] >= d["min_duration_s"]]
    print(f"[gold] {len(gold)} video thoả NEW_CHANNEL_HIT "
          f"(subs>={d['min_subs']}, kênh<={d['new_channel_days']}d, "
          f"views>={d['new_channel_min_views']:,})", file=sys.stderr)
    for r in sorted(gold, key=lambda x: x["views"], reverse=True)[:15]:
        print(f"   {r['ch_age_days']:>4}d {r['subs']:>7,}sub {r['views']:>9,}v  "
              f"{r['title'][:44]} | {r['channel'][:18]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
