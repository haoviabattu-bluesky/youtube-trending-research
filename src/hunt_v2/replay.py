# -*- coding: utf-8 -*-
"""Chạy lại CÁC GATE từ `runs/<ngày>/<lane>/02_enriched.json` — KHÔNG quét lại YouTube.

Discovery + enrich mất ~20 phút/lane; hiệu chỉnh threshold mà phải quét lại mỗi lần là không
làm nổi. Cache LLM theo (video_id + lane_fingerprint + prompt_version + model) nên chạy lại với
threshold khác gần như miễn phí — chỉ phần đổi prompt/lane profile mới tốn tiền.

  py -3.13 -X utf8 src/hunt_v2/replay.py --lane Lopezzapa68
  py -3.13 -X utf8 src/hunt_v2/replay.py --lane Lopezzapa68 --date 2026-09-22 --no-llm
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / "config" / ".env")

import store  # noqa: E402
from hunt_v2 import (final_qc, hard_filter, opportunity_gate, ranker,  # noqa: E402
                     semantic_format_gate, viral_engine)
from hunt_v2.lane_profile import load_lane  # noqa: E402
from hunt_v2.llm_client import LlmClient  # noqa: E402
from hunt_v2.run_store import RunStore  # noqa: E402
from hunt_v2.runner import load_models, load_rules  # noqa: E402

LOG = lambda *a: print(*a, file=sys.stderr, flush=True)  # noqa: E731


def latest_run_dir(runs_root: Path, lane: str, date: str | None) -> Path:
    if date:
        return runs_root / date / lane
    days = sorted(d for d in runs_root.iterdir() if (d / lane / "02_enriched.json").exists())
    if not days:
        raise SystemExit(f"không có runs/*/{lane}/02_enriched.json — chạy run_video_hunt.py trước")
    return days[-1] / lane


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--date", default="")
    ap.add_argument("--no-llm", action="store_true", help="chỉ hard filter + viral (không gọi model)")
    a = ap.parse_args()

    rules, models = load_rules(ROOT), load_models(ROOT)
    lane = load_lane(ROOT / "lanes", a.lane)
    if lane is None:
        raise SystemExit(f"không có lanes/{a.lane}/lane_profile.yaml")
    d = latest_run_dir(ROOT / "runs", a.lane, a.date or None)
    rows = json.loads((d / "02_enriched.json").read_text(encoding="utf-8"))
    LOG(f"[replay] {d} — {len(rows)} video")

    con = store.connect(ROOT / "data" / "trending.db")
    client = LlmClient(models, con, ROOT / "logs", lane.fingerprint())
    rs = RunStore(ROOT / "runs", d.parent.name, a.lane)
    flags = {"semantic_gate": not a.no_llm, "format_gate": not a.no_llm}

    kept, rejected = hard_filter.apply(rows, lane, rules, set(), [], lane.all_queries["core_tags"])
    kept.sort(key=lambda r: r["vpd"], reverse=True)
    kept = kept[: rules["hard_filter"]["max_semantic_candidates_per_lane"]]
    rej = Counter(r["reason"] for r in rejected)
    LOG(f"[replay] hard filter: {len(kept)} giữ / {len(rejected)} loại {dict(rej)}")

    semantic_format_gate.run(kept, lane, client, rules, flags)
    rs.save(4, "semantic", [{"video_id": c["video_id"], "title": c["title"], **c["semantic"]} for c in kept])
    rs.save(5, "format", [{"video_id": c["video_id"], **c["format"]} for c in kept])
    alive = [c for c in kept if c["semantic_pass"] and c["format_pass"]]
    LOG(f"[replay] semantic+format: {len(alive)}/{len(kept)} PASS  (LLM {client.stats})")

    # baseline: đọc cache SQLite, không gọi Data API trong replay
    from hunt_v2 import store_v2
    bl = {}
    for c in alive:
        row = store_v2.load_hunt_baseline(con, c["channel_id"])
        bl[c["channel_id"]] = json.loads(row["payload"]) if row else None
    viral_engine.score(alive, bl, rules)
    rs.save(6, "viral", [{"video_id": c["video_id"], "title": c["title"], **c["viral"]} for c in alive])
    viral_ok = sorted([c for c in alive if c["viral"]["viral_pass"]],
                      key=lambda c: c["viral"]["viral_score"], reverse=True)
    LOG(f"[replay] viral: {len(viral_ok)}/{len(alive)} PASS")

    if not a.no_llm:
        short = viral_ok[: rules["opportunity"]["shortlist_n"]]
        opportunity_gate.run(short, lane, client, rules, True)
        qc_short = [c for c in short if c["opportunity"].get("decision") in ("PASS", "UNCERTAIN")]
        qc_short = qc_short[: rules["final_qc"]["shortlist_n"]]
        final_qc.run(qc_short, lane, client, True)
        rs.save(7, "opportunity", [{"video_id": c["video_id"], **c["opportunity"]} for c in short])
        rs.save(8, "final_qc", [{"video_id": c["video_id"], **c["final_qc"]} for c in qc_short])
        LOG(f"[replay] opportunity {len([c for c in short if c.get('opportunity_pass')])}/{len(short)}"
            f" · final QC {len([c for c in qc_short if c.get('final_qc_pass')])}/{len(qc_short)}")

    selected, shadow = ranker.rank(alive, rules, a.lane)
    for i, c in enumerate(shadow[:8], 1):
        v = c["viral"]
        LOG(f"  {i}. {c['final_score']:6.1f} https://youtu.be/{c['video_id']} "
            f"viral={v['viral_score']} {v['viral_type']} br={v['breakout_ratio']} "
            f"topic={c['semantic'].get('topic_match')} {c['format'].get('format_class')} "
            f"qc={c.get('final_qc', {}).get('decision')} | {c['title'][:50]}")
    LOG(f"[replay] SELECTED: {[c['video_id'] for c in selected]}")
    rs.count("replay_kept", len(kept))
    rs.count("replay_alive", len(alive))
    rs.count("replay_selected", len(selected))
    rs.save(9, "ranked_replay", [{k: v for k, v in c.items() if k != "description"} for c in shadow])
    rs.write_report(lane.profile.get("label", a.lane) + " (replay)", shadow[:5], dict(rej), client.stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
