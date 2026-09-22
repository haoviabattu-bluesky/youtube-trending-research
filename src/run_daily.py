# -*- coding: utf-8 -*-
"""Orchestrator chạy hằng ngày: discover → enrich → store → score → deepdive → Sheet.

  py -3.13 -X utf8 src/run_daily.py                      # chạy đủ, đẩy lên Sheet
  py -3.13 -X utf8 src/run_daily.py --dry-run            # không đụng Sheet
  py -3.13 -X utf8 src/run_daily.py --limit-kw 10 --no-deepdive
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
import keywords as kwmod                                            # noqa: E402
import score as sc                                                  # noqa: E402
import store                                                        # noqa: E402
from deepdive import analyze, llm_insight                           # noqa: E402
from enrich import Enricher                                         # noqa: E402
from innertube import BotCheckError, InnerTube                      # noqa: E402
from lockfile import RunLock                                        # noqa: E402
import publish                                                      # noqa: E402
from pipeline import compute_baselines, discover_niche              # noqa: E402
from sheets import SheetReporter                                    # noqa: E402
from ytapi import YouTubeAPI                                        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")
LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731


def load_yaml_niches() -> dict:
    with open(ROOT / "config" / "niches.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--niche", default="", help="mặc định: tất cả ngách bật trong config")
    ap.add_argument("--limit-kw", type=int, default=0)
    ap.add_argument("--windows", default="")
    ap.add_argument("--dry-run", action="store_true", help="không ghi Google Sheet")
    ap.add_argument("--no-deepdive", action="store_true")
    ap.add_argument("--no-api", action="store_true")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="cho phép đè khối cùng ngày kể cả khi lượt này ít dòng hơn")
    args = ap.parse_args()

    t0 = time.time()
    ycfg = load_yaml_niches()
    cfg = ycfg["defaults"]
    key = os.getenv("YOUTUBE_API_KEY", "")
    api = None if (args.no_api or not key) else YouTubeAPI(key)
    snap = store.today()
    con = store.connect(ROOT / "data" / "trending.db")

    rep = None
    if not args.dry_run:
        rep = SheetReporter(os.getenv("SHEET_ID"), os.getenv("GOOGLE_SHEETS_KEY"))
        before = rep.guard_snapshot()
        LOG(f"[guard] số dòng trước khi ghi: {before}")
        rep.bootstrap_config(ycfg["niches"])
        sheet_cfg = rep.read_config()
        if sheet_cfg:
            for name, d in sheet_cfg.items():
                if name in ycfg["niches"]:
                    ycfg["niches"][name]["keywords"] = d["keywords"]
                else:
                    ycfg["niches"][name] = {"label": name, **d}
            LOG(f"[config] đọc từ TRD_CONFIG: "
                f"{ {k: len(v['keywords']) for k, v in sheet_cfg.items()} }")

    names = [n.strip() for n in args.niche.split(",") if n.strip()] or list(ycfg["niches"])
    windows = args.windows.split(",") if args.windows else cfg["windows"]

    all_rows: list[dict] = []
    for name in names:
        n = ycfg["niches"][name]
        kws = n["keywords"][: args.limit_kw] if args.limit_kw else n["keywords"]
        LOG(f"\n[{name}] {len(kws)} kw × {len(windows)} lát")
        it = InnerTube(hl=n.get("hl", "ja"), gl=n.get("gl", "JP"))
        try:
            found = discover_niche(it, kws, windows, name)
        except BotCheckError as e:
            LOG(f"!! BOT-CHECK: {e}")
            return 2
        tot = it.parse_ok + it.parse_fail
        LOG(f"[{name}] {len(found)} video, parse {100 * it.parse_ok / max(tot, 1):.1f}%")
        enr = Enricher(api, it)
        all_rows.extend(enr.build_rows(list(found.values()), name))
        LOG(f"[{name}] enrich {enr.stat}")

    rows = store.dedupe_rows(all_rows)
    LOG(f"\n[dedupe] {len(all_rows)} → {len(rows)} video duy nhất")
    store.save_snapshot(con, rows, snap)

    prev = store.prev_video_stats(con, snap)
    subs_prev = store.prev_channel_subs(con, snap)
    baselines = compute_baselines(api, rows, cfg, con)
    LOG(f"[delta] {len(prev)} video có snapshot cũ để so; baseline {len(baselines)} kênh")

    for r in rows:
        r.update(sc.compute_metrics(r, prev.get(r["video_id"]),
                                    baselines.get(r["channel_id"]), cfg, snap))
        r["subs_7d"] = (r.get("subs") or 0) - subs_prev.get(r["channel_id"], r.get("subs") or 0)
        r["label"] = sc.label_row(r, cfg, rising=(r.get("views_24h") or 0) > 0)
    sc.score_within_niche(rows, cfg)

    keep = [r for r in rows if r["label"] != "NOISE"]
    keep.sort(key=lambda r: r["score"], reverse=True)
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    LOG(f"[label] {counts}")

    top = sc.pick_elite(keep, cfg, LOG)
    LOG(f"[elite] chọn {len(top)} video tinh hoa / {len(keep)} video qua vòng loại "
        f"({len({r['channel_id'] for r in top})} kênh khác nhau)")

    deep: dict[str, dict] = {}
    if not args.no_deepdive and top:
        langs = [ycfg["niches"][names[0]].get("hl", "ja"), "en"]
        titles = [r["title"] for r in top[:60]]
        base = os.getenv("LLM_BASE_URL", "")
        lkey = "" if args.no_llm else os.getenv("LLM_API_KEY", "")
        # Ngân sách thời gian: đào sâu là bước KHÔNG đoán được độ dài (video comment lớn,
        # transcript thiếu, LLM chậm). Đo thật: 10 video mất 861s, đẩy tổng lượt chạy lên
        # 23 phút. Có trần thì lượt chạy hằng ngày luôn kết thúc đúng hẹn, mất vài bản
        # đào sâu vẫn còn nguyên bảng xếp hạng.
        budget = cfg.get("deepdive_budget_s", 420)
        t_dd = time.time()
        for r in top[: cfg["deepdive_top_n"]]:
            if time.time() - t_dd > budget:
                LOG(f"[deepdive] HẾT ngân sách {budget}s sau {len(deep)} video — dừng")
                break
            LOG(f"[deepdive] {r['title'][:40]}")
            p = analyze(r, langs, titles, cfg.get("deepdive_comments", 50))
            p["insight"] = llm_insight(p, r, base, lkey, os.getenv("LLM_MODEL", ""))
            store.save_deepdive(con, r["video_id"], p, snap)
            deep[r["video_id"]] = p
        LOG(f"[deepdive] xong {len(deep)} video trong {time.time() - t_dd:.0f}s")

    kw_niche = {kw: nm for nm in names for kw in ycfg["niches"][nm]["keywords"]}
    kw_rows = kwmod.enrich_with_history(con, kwmod.compute(con, snap, kw_niche), snap)
    store.save_keyword_snapshot(con, kw_rows, snap)
    LOG(f"[keywords] {len(kw_rows)} keyword có thống kê")

    if args.dry_run:
        LOG("\n[dry-run] KHÔNG ghi Sheet. Top 15:")
        for i, r in enumerate(top[:15], 1):
            LOG(f" {i:2}. {r['score']:5.1f} {sc.LABEL_ICON[r['label']]}{r['label']:<16} "
                f"{r['views']:>8,}v {r.get('subs') or 0:>7,}sub "
                f"{str(r.get('ch_age_days')):>5}d  {r['title'][:44]}")
    else:
        publish.push(rep, con, store, top, keep, kw_rows, deep, baselines,
                     snap, cfg, args.force, LOG)
        if not publish.verify_untouched(rep, before, LOG):
            return 3

    if api:
        LOG(f"[quota] {api.used} / 10000")
    LOG(f"[done] {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    with RunLock(ROOT / "data" / "run.lock") as acquired:
        if not acquired:
            LOG("[lock] đã có lượt chạy khác — thoát, KHÔNG chạy chồng")
            raise SystemExit(0)
        raise SystemExit(main())
