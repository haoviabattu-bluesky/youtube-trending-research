# -*- coding: utf-8 -*-
"""Runner V2 — nối các gate theo thứ tự H1b→H2b→H3→H4/5→H6→H7→H8→H9, mỗi bước ghi runs/.

Được gọi từ run_video_hunt.py SAU khi đường cũ đã có pick. Nhận lại pool `found`/`rows`
của đường cũ nên không quét lại tag. Lỗi bất kỳ trong V2 KHÔNG được làm hỏng lượt cũ —
caller bọc try/except; ở đây mỗi gate cũng tự ghi ERROR thay vì ném.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from hunt_v2 import (baseline, discovery, final_qc, hard_filter, opportunity_gate, ranker,
                     semantic_format_gate, store_v2)
from hunt_v2.lane_profile import LaneProfile, load_lane
from hunt_v2.llm_client import LlmClient
from hunt_v2.run_store import RunStore


@dataclass
class V2Result:
    lane: str
    selected: list[dict] = field(default_factory=list)
    shadow_ranked: list[dict] = field(default_factory=list)
    counts: dict = field(default_factory=dict)
    run_id: str = ""
    error: str | None = None
    report_path: str = ""


def load_rules(root: Path) -> dict:
    with open(root / "config" / "hunt_rules.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_models(root: Path) -> dict:
    with open(root / "config" / "models.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _slim(c: dict) -> dict:
    """Bản ghi gọn để dump JSON (bỏ description dài)."""
    d = dict(c)
    if d.get("description"):
        d["description"] = d["description"][:200]
    return d


def run_lane_v2(root: Path, lane_id: str, flags: dict, ctx: dict, api, con, snap: str,
                log, discover_fn) -> V2Result:
    """ctx = {found, rows, kws, done_titles, it, pool, enricher, old_picks}."""
    res = V2Result(lane=lane_id)
    lane: LaneProfile | None = load_lane(root / flags.get("lanes_dir", "lanes"), lane_id)
    if lane is None:
        res.error = "không có lanes/<lane>/lane_profile.yaml — bỏ qua V2"
        return res
    rules, models = load_rules(root), load_models(root)
    rs = RunStore(root / flags.get("runs_dir", "runs"), snap, lane_id)
    res.run_id = rs.run_id
    client = LlmClient(models, con, root / "logs", lane_fingerprint=lane.fingerprint())
    found, rows = ctx["found"], list(ctx["rows"])

    # H1b discovery mở rộng → enrich phần mới
    if flags.get("discovery_expansion"):
        st = discovery.run(found, lane, ctx["kws"], ctx["it"], ctx["pool"], api, rules,
                           discover_fn, log)
        rs.note(f"discovery mở rộng: {st}")
        have = {r["video_id"] for r in rows}
        new_raw = [r for v, r in found.items() if v not in have
                   and (r.get("views_it") or 0) >= rules["hard_filter"]["min_views"]]
        if new_raw:
            rows += ctx["enricher"].build_rows(new_raw, lane_id)
        log(f"[{lane_id}][v2] discovery +{st['new_from_queries']} query, +{st['new_from_watch']} watch → enrich thêm {len(new_raw)}")
    for r in rows:
        r["discovery_sources"] = found.get(r["video_id"], {}).get("discovery_sources", ["A:tag"])
    rs.save(1, "discovery", [{"video_id": v, "title": r.get("title"), "sources": r.get("discovery_sources")}
                             for v, r in found.items()])
    rs.save(2, "enriched", [_slim(r) for r in rows])

    # H3
    already = store_v2.v2_picked_video_ids(con, lane_id, mode="PRODUCTION")
    kept, rejected = hard_filter.apply(rows, lane, rules, already, ctx["done_titles"], ctx["kws"])
    kept.sort(key=lambda r: r["vpd"], reverse=True)
    cap = rules["hard_filter"]["max_semantic_candidates_per_lane"]
    if len(kept) > cap:
        rejected += [{"video_id": r["video_id"], "title": r["title"], "reason": "CAP_SEMANTIC_POOL"}
                     for r in kept[cap:]]
        kept = kept[:cap]
    rej_counter = Counter(r["reason"] for r in rejected)
    rs.save(3, "hard_filter", {"kept": [_slim(r) for r in kept], "rejected": rejected})
    log(f"[{lane_id}][v2] hard filter: {len(kept)} giữ / {len(rejected)} loại {dict(rej_counter)}")

    # H4/H5
    semantic_format_gate.run(kept, lane, client, rules, flags)
    rs.save(4, "semantic", [{"video_id": c["video_id"], "title": c["title"], **c["semantic"]} for c in kept])
    rs.save(5, "format", [{"video_id": c["video_id"], **c["format"]} for c in kept])
    sem_pass = [c for c in kept if c["semantic_pass"] and c["format_pass"]]
    rs.count("semantic_format_pass", len(sem_pass))
    for c in kept:
        if not (c["semantic_pass"] and c["format_pass"]):
            rej_counter[f"GATE:{c['semantic'].get('decision')}/{c['format'].get('decision')}"] += 1
    log(f"[{lane_id}][v2] semantic+format: {len(sem_pass)}/{len(kept)} PASS")

    # H2b baseline (chỉ cho candidate còn sống) + H6 viral
    chans = {c["channel_id"]: c.get("uploads_playlist", "") for c in sem_pass}
    bstats: dict = {}
    baselines = baseline.channel_baselines(api, con, chans, rules, bstats)
    rs.note(f"baseline: {bstats}")
    from hunt_score import score_rows  # đường cũ — dùng khi viral_engine_v2 tắt
    if flags.get("viral_engine_v2", True):
        from hunt_v2 import viral_engine
        viral_engine.score(sem_pass, baselines, rules)
    else:
        for c, s in zip(sem_pass, score_rows(sem_pass, {"fresh_bonus_days": 14})):
            c["viral"] = {"viral_score": min(100, s["score"] / 100), "viral_pass": True,
                          "viral_type": "LEGACY", "vpd": s["vpd"]}
    rs.save(6, "viral", [{"video_id": c["video_id"], "title": c["title"], **c["viral"]} for c in sem_pass])
    viral_ok = [c for c in sem_pass if c["viral"]["viral_pass"]]
    rs.count("viral_pass", len(viral_ok))

    # H7 opportunity (shortlist) + H8 final QC (shortlist nhỏ hơn)
    viral_ok.sort(key=lambda c: c["viral"]["viral_score"], reverse=True)
    short = viral_ok[: rules["opportunity"]["shortlist_n"]]
    opportunity_gate.run(short, lane, client, rules, bool(flags.get("opportunity_gate")))
    rs.save(7, "opportunity", [{"video_id": c["video_id"], "title": c["title"], **c["opportunity"]} for c in short])
    opp_alive = [c for c in short if c["opportunity"].get("decision") in ("PASS", "UNCERTAIN")]
    rs.count("opportunity_pass", len([c for c in short if c.get("opportunity_pass")]))
    opp_alive.sort(key=lambda c: (c["opportunity"].get("opportunity_score") or 0,
                                  c["viral"]["viral_score"]), reverse=True)
    qc_short = opp_alive[: rules["final_qc"]["shortlist_n"]]
    final_qc.run(qc_short, lane, client, bool(flags.get("final_qc")))
    rs.save(8, "final_qc", [{"video_id": c["video_id"], "title": c["title"], **c["final_qc"]} for c in qc_short])
    rs.count("final_qc_pass", len([c for c in qc_short if c.get("final_qc_pass")]))

    # H9
    selected, shadow = ranker.rank(sem_pass, rules, lane_id)
    rs.save(9, "ranked", [_slim(c) for c in shadow])
    rs.count("selected", len(selected))
    res.selected, res.shadow_ranked, res.counts = selected, shadow, dict(rs.counts)
    old_ids = {p["video_id"] for p in ctx.get("old_picks", [])}
    compare = [{"video_id": c["video_id"], "old": c["video_id"] in old_ids,
                "v2": c in selected} for c in shadow[:10]]
    for p in ctx.get("old_picks", []):
        if p["video_id"] not in {x["video_id"] for x in compare}:
            compare.append({"video_id": p["video_id"], "old": True, "v2": False})
    res.report_path = str(rs.write_report(lane.profile.get("label", lane_id), shadow[:5],
                                          dict(rej_counter), client.stats, compare))
    mode = "PRODUCTION" if not flags.get("shadow_mode", True) else "SHADOW"
    if selected:
        store_v2.save_v2_picks(con, lane_id, [{**c.get("selected_record", {}), "title": c["title"]}
                                              for c in selected], snap, mode)
    log(f"[{lane_id}][v2] chọn {len(selected)} (mode {mode}); LLM {json.dumps(client.stats)}")
    return res
