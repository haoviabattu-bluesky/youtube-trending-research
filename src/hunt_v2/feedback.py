# -*- coding: utf-8 -*-
"""H11 — human feedback loop (guide §20, §21): đọc HUMAN_DECISION/REJECT_REASON từ TRD_HUNT_AUDIT
(CHỈ ĐỌC), lưu SQLite, tính metric, và khi lane đủ ≥20 quyết định → nhờ Claude soạn PROPOSAL
cập nhật positive/negative examples + query_expansion. KHÔNG tự sửa lane_profile.yaml.

  py -3.13 -X utf8 src/hunt_v2/feedback.py --sync              # kéo feedback về DB + in metric
  py -3.13 -X utf8 src/hunt_v2/feedback.py --propose --lane X  # sinh lanes/X/feedback_proposal_<ngày>.md
  py -3.13 -X utf8 src/hunt_v2/feedback.py --apply --lane X    # áp proposal JSON (sau khi user đọc)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / "config" / ".env")
import yaml  # noqa: E402

import store  # noqa: E402
from hunt_v2 import audit_writer, schemas, store_v2  # noqa: E402
from hunt_v2.lane_profile import load_lane  # noqa: E402
from hunt_v2.llm_client import LlmClient  # noqa: E402
from sheets import SheetReporter  # noqa: E402

MIN_DECISIONS = 20


def sync(rep, con) -> list[dict]:
    fb = audit_writer.read_human_feedback(rep)
    good = [f for f in fb if f["decision"] in schemas.HUMAN_DECISIONS]
    bad = [f for f in fb if f["decision"] not in schemas.HUMAN_DECISIONS]
    for b in bad:
        print(f"  ! bỏ qua {b['video_id']}: HUMAN_DECISION={b['decision']!r} không thuộc {schemas.HUMAN_DECISIONS}")
    store_v2.upsert_human_feedback(con, good)
    return good


def metrics(fb: list[dict]) -> dict:
    """Guide §32 — tính trên các dòng có quyết định."""
    by_lane: dict[str, Counter] = {}
    for f in fb:
        by_lane.setdefault(f["lane"], Counter())[f["decision"]] += 1
    out = {}
    for lane, c in by_lane.items():
        n = sum(c.values())
        out[lane] = {"n": n, "accept_rate": round(c["ACCEPT"] / n, 2) if n else None,
                     "reject": c["REJECT"], "skip": c["SKIP"]}
    reasons = Counter(f["reason"] for f in fb if f["decision"] == "REJECT")
    out["_reject_reasons"] = dict(reasons)
    return out


def propose(lane_id: str, fb: list[dict], con) -> Path | None:
    mine = [f for f in fb if f["lane"] == lane_id]
    if len(mine) < MIN_DECISIONS:
        print(f"[{lane_id}] mới {len(mine)}/{MIN_DECISIONS} quyết định — chưa đủ để đề xuất")
        return None
    lane = load_lane(ROOT / "lanes", lane_id)
    with open(ROOT / "config" / "models.yaml", encoding="utf-8") as f:
        models = yaml.safe_load(f)
    client = LlmClient(models, con, ROOT / "logs", lane.fingerprint())
    acc = [f for f in mine if f["decision"] == "ACCEPT"]
    rej = [f for f in mine if f["decision"] == "REJECT"]
    prompt = (
        "You maintain the lane profile of a YouTube research pipeline. Based on human decisions, propose "
        "updates. Do NOT rewrite the lane profile itself. Return ONLY JSON:\n"
        '{"positive_examples":[{"title":"","why":""}],"negative_patterns":[{"pattern":"","reason":"","count":1}],'
        '"query_expansion_add":{"concept_queries":[],"format_queries":[],"story_queries":[]},'
        '"query_expansion_remove":[],"notes":""}\n\n'
        f"LANE_PROFILE:\n{lane.prompt_block()}\n\nCURRENT EXPANSION:\n{json.dumps(lane.expansion, ensure_ascii=False)}\n\n"
        f"ACCEPTED ({len(acc)}):\n" + "\n".join(f"- {a['title']}" for a in acc) +
        f"\n\nREJECTED ({len(rej)}):\n" + "\n".join(f"- [{r['reason']}] {r['title']}" for r in rej))
    res = client.call("feedback", prompt, [f["video_id"] for f in mine], schema_name=None, use_cache=False)
    if not res.ok:
        print(f"[{lane_id}] LLM lỗi: {res.error}")
        return None
    stamp = dt.date.today().isoformat()
    d = ROOT / "lanes" / lane_id
    (d / f"feedback_proposal_{stamp}.json").write_text(
        json.dumps(res.parsed_response, ensure_ascii=False, indent=2), encoding="utf-8")
    md = d / f"feedback_proposal_{stamp}.md"
    md.write_text(f"# Đề xuất cập nhật lane {lane_id} ({stamp})\n\nDựa trên {len(mine)} quyết định "
                  f"(ACCEPT {len(acc)} / REJECT {len(rej)}). Model: {res.model}.\n\n```json\n"
                  f"{json.dumps(res.parsed_response, ensure_ascii=False, indent=2)}\n```\n\n"
                  f"Áp dụng: `py -3.13 -X utf8 {ROOT / 'src' / 'hunt_v2' / 'feedback.py'} --apply --lane {lane_id}`\n",
                  encoding="utf-8")
    print(f"[{lane_id}] đề xuất → {md}")
    return md


def apply(lane_id: str) -> None:
    d = ROOT / "lanes" / lane_id
    props = sorted(d.glob("feedback_proposal_*.json"))
    if not props:
        print(f"[{lane_id}] không có proposal để áp")
        return
    p = json.loads(props[-1].read_text(encoding="utf-8"))
    for fname, key in (("positive_examples.json", "positive_examples"), ("negative_examples.json", "negative_patterns")):
        cur = json.loads((d / fname).read_text(encoding="utf-8"))
        cur.setdefault(key, []).extend(p.get(key, []))
        (d / fname).write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
    qe = json.loads((d / "query_expansion.json").read_text(encoding="utf-8"))
    for grp, qs in (p.get("query_expansion_add") or {}).items():
        qe.setdefault(grp, [])
        qe[grp] += [q for q in qs if q not in qe[grp]]
    rm = set(p.get("query_expansion_remove") or [])
    for grp in qe:
        qe[grp] = [q for q in qe[grp] if q not in rm]
    (d / "query_expansion.json").write_text(json.dumps(qe, ensure_ascii=False, indent=2), encoding="utf-8")
    props[-1].rename(props[-1].with_suffix(".applied.json"))
    print(f"[{lane_id}] đã áp {props[-1].name} (lane_profile.yaml KHÔNG đổi)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--propose", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--lane", default="")
    a = ap.parse_args()
    con = store.connect(ROOT / "data" / "trending.db")
    if a.apply:
        apply(a.lane)
        return 0
    with open(ROOT / "config" / "video_hunt.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    rep = SheetReporter(cfg["defaults"]["sheet_id"], os.getenv("GOOGLE_SHEETS_KEY"))
    fb = sync(rep, con)
    print(json.dumps(metrics(fb), ensure_ascii=False, indent=1))
    if a.propose:
        for lane_id in ([a.lane] if a.lane else cfg["lanes"]):
            propose(lane_id, fb, con)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
