# -*- coding: utf-8 -*-
"""NEWS RADAR — CLI. Kế hoạch: plans/261017-1030-news-radar/plan.md

  py -3.13 -X utf8 src/run_news_radar.py --collect [--dry-run]       # thu 5 nguồn → data/news_radar.db
  py -3.13 -X utf8 src/run_news_radar.py --brief [--hooks] [--handoff] # gộp cụm → cung YouTube → chấm → tư liệu top 5 → brief ngày
  py -3.13 -X utf8 src/run_news_radar.py --loop 45                    # thu mỗi 45 phút; brief lúc 07/12/19h (JST = giờ máy)
Không ghi Google Sheet. Đầu ra: runs/news_radar/<ngày>/ + E:\\CLAUDE\\YOUTUBE\\MG_STUDIO\\lanes\\q\\NEWS_RADAR\\<ngày>.md"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / "config" / ".env")

from hunt_v2.llm_client import LlmClient           # noqa: E402
from innertube import InnerTube                     # noqa: E402
from lockfile import RunLock                        # noqa: E402
from news_radar import brief, cluster, collectors, evidence, heat, store, supply  # noqa: E402

BRIEF_HOURS = (7, 12, 19)


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


def load_cfg() -> dict:
    with open(ROOT / "config" / "news_radar.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_models() -> dict:
    with open(ROOT / "config" / "models.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def do_collect(cfg: dict, con, dry_run: bool) -> dict:
    log("THU 5 nguồn" + (" (dry-run)" if dry_run else ""))
    return collectors.collect_all(cfg, con, log, dry_run)


def do_brief(cfg: dict, con, snap_date: str, hooks: bool, handoff: bool, dry_run: bool) -> Path | None:
    since = int(time.time()) - cfg["cluster"]["lookback_hours"] * 3600
    sigs = store.recent_signals(con, since)
    if not sigs:
        log("Chưa có signal trong 24h — chạy --collect trước")
        return None
    rows = cluster.keyword_table(sigs, cfg["cluster"]["max_keywords"])
    log(f"GỘP {len(rows)} keyword (từ {len(sigs)} signal)")
    client = LlmClient(load_models(), con, ROOT / "logs")
    clusters = cluster.cluster_keywords(client, rows, snap_date, log)

    it = InnerTube(cfg["market"]["hl"], cfg["market"]["geo"])
    snap_ts = int(time.time())
    notes: list[str] = []
    for c in clusters:
        sup = {"videos": [], "n": 0, "views": 0, "blocked": False}
        if cfg["sources"].get("youtube_supply") and c["is_news"]:
            sup = supply.measure(it, c, log)
            if sup["blocked"] and "YouTube chặn" not in " ".join(notes):
                notes.append("YouTube chặn InnerTube giữa chừng — cột CUNG thiếu, gap có thể cao giả.")
        if not dry_run:
            store.replace_supply(con, c["cluster_id"], sup["videos"], snap_ts)
        sc = heat.score_cluster(c["by_source"], store.prev_cluster_heat(con, c["label_ja"], snap_date),
                                sup["n"], sup["views"], c["sensational"], c["is_news"], cfg["heat"])
        c.update(sc, supply_videos=sup["n"], supply_views=sup["views"])
    clusters.sort(key=lambda c: -c["final"])
    top = [c for c in clusters if c["final"] >= cfg["brief"]["min_final_score"]][: cfg["brief"]["top_n"]]
    log(f"CHẤM xong: {len(clusters)} cụm, lấy top {len(top)}")
    for i, c in enumerate(top, 1):
        log(f"  {i:2d}. {c['final']:6.2f} {c['category']} {c['label_ja'][:28]} | {'/'.join(c['sources'])} | cung {c['supply_videos']}v/{c['supply_views']:,}")
    if dry_run:
        return None

    run_dir = ROOT / cfg["output"]["runs_dir"] / snap_date
    import shutil
    shutil.rmtree(run_dir / "packs", ignore_errors=True)  # chạy lại trong ngày: cụm cũ đổi id → không để pack mồ côi
    packs: dict[str, dict] = {}
    for i, c in enumerate(top, 1):
        if i <= cfg["brief"]["evidence_top_n"]:
            evidence.gather(con, c, cfg, store, log)
            if hooks:
                evidence.gather_hooks(con, c, cfg, store, log)
        ev, sup_rows, hk = store.evidence_of(con, c["cluster_id"]), store.supply_of(con, c["cluster_id"]), store.hooks_of(con, c["cluster_id"])
        c["brief"] = brief.write_one(client, c, sup_rows, ev, log)
        packs[c["cluster_id"]] = {"evidence": ev, "supply": sup_rows, "hooks": hk}
        evidence.dump_pack(c, ev, sup_rows, hk, run_dir / "packs")
        store.upsert_cluster(con, c)
    for c in clusters[len(top):]:
        store.upsert_cluster(con, c)

    md = brief.render_markdown(snap_date, top, packs, notes)
    lane_dir = Path(cfg["output"]["lane_q_dir"]) if handoff else None
    files = brief.write_files(snap_date, md, top, run_dir, lane_dir)
    if handoff:
        import shutil
        shutil.copytree(run_dir / "packs", lane_dir / "packs" / snap_date, dirs_exist_ok=True)
        _append_handoff(Path(cfg["output"]["handoff_log"]), snap_date, top, lane_dir / f"{snap_date}.md")
    log(f"LLM: {client.stats}")
    for f in files:
        log(f"📝 {f}")
    return files[0]


def _append_handoff(logf: Path, snap_date: str, top: list[dict], md_path: Path) -> None:
    lam = [c for c in top if (c.get("brief") or {}).get("verdict") == "LÀM NGAY"]
    line = (f"\n## {dt.datetime.now():%Y-%m-%d %H:%M} · NEWS RADAR {snap_date}\n"
            f"- Brief {len(top)} đề tài, {len(lam)} `LÀM NGAY`: " + "; ".join(c["label_ja"] for c in lam[:5]) + "\n"
            f"- File: `{md_path}` · gói tư liệu `{md_path.parent / 'packs' / snap_date}`\n")
    old = logf.read_text(encoding="utf-8") if logf.exists() else ""
    pat = "\n## [^\n]* · NEWS RADAR " + re.escape(snap_date) + "\n(?:- [^\n]*\n)*"
    old = re.sub(pat, "", old)  # chạy lại trong ngày → thay khối cũ, không chồng dòng
    logf.write_text(old.rstrip("\n") + "\n" + line, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--loop", type=int, metavar="MIN", help="thu mỗi MIN phút, brief lúc 07/12/19h")
    ap.add_argument("--hooks", action="store_true", help="đọc hook 2 video đối thủ/cụm (chậm, ~20s/video)")
    ap.add_argument("--handoff", action="store_true", help="chép brief sang MG_STUDIO lane Q + ghi BAN_GIAO_TRENDING.md")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = load_cfg()
    con = store.connect(ROOT / cfg["output"]["db"])
    with RunLock(ROOT / "data" / "news_radar.lock", max_age_s=3 * 3600) as ok:
        if not ok:
            log("Lượt khác đang chạy (data/news_radar.lock) — thoát")
            return 2
        if a.loop:
            done_brief: set[tuple[str, int]] = set()
            while True:
                do_collect(cfg, con, False)
                now = dt.datetime.now()
                key = (now.date().isoformat(), max([h for h in BRIEF_HOURS if h <= now.hour] or [0]))
                if key[1] and key not in done_brief:
                    do_brief(cfg, con, key[0], a.hooks, True, False)
                    done_brief.add(key)
                time.sleep(a.loop * 60)
        if a.collect:
            do_collect(cfg, con, a.dry_run)
        if a.brief:
            do_brief(cfg, con, a.date, a.hooks, a.handoff, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
