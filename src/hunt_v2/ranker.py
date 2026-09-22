# -*- coding: utf-8 -*-
"""H9 — ranking tất định (guide §17, §18, §36). AI không quyết top 1/2.

final_score = Σ weight × sub-score (0–100); sub-score thiếu (gate tắt/lỗi) → bỏ khỏi mẫu số và
gắn cờ. `selected` chỉ gồm candidate đủ 4 cờ PASS + đủ field critical; `shadow_ranked` là
toàn bộ candidate còn sống xếp theo final_score để ghi audit khi shadow.
"""
from __future__ import annotations

from hunt_score import _is_dup_topic
from hunt_v2 import schemas

REQUIRED_FLAGS = ("semantic_pass", "format_pass", "viral_pass", "final_qc_pass")  # guide §2


def _components(c: dict) -> dict[str, float | None]:
    v, s, o = c.get("viral", {}), c.get("semantic", {}), c.get("opportunity", {})
    sem = None
    if isinstance(s.get("topic_match"), int):
        sem = (s["topic_match"] + s.get("audience_match", 0) + s.get("content_identity_match", 0)) / 3
    return {
        "viral": v.get("viral_score"),
        "semantic": sem,
        "opportunity": o.get("opportunity_score") if isinstance(o.get("opportunity_score"), int) else None,
        "freshness": v.get("freshness_score"),
    }


def final_score(c: dict, rules: dict, diversity: float = 100.0) -> float:
    w = rules["ranking"]["weights"]
    comps = _components(c)
    comps["diversity"] = diversity
    num = den = 0.0
    for k, val in comps.items():
        if val is None:
            continue
        num += w[k] * val
        den += w[k]
    c["score_components"] = {k: (round(v, 1) if v is not None else None) for k, v in comps.items()}
    return round(num / den, 2) if den else 0.0


def selected_record(c: dict, lane_id: str) -> dict:
    op, qc = c.get("opportunity", {}), c.get("final_qc", {})
    return {
        "video_id": c["video_id"], "url": f"https://youtu.be/{c['video_id']}", "lane_id": lane_id,
        "semantic_pass": c.get("semantic_pass"), "format_pass": c.get("format_pass"),
        "viral_pass": c.get("viral", {}).get("viral_pass"), "final_qc_pass": c.get("final_qc_pass"),
        "viral_type": c.get("viral", {}).get("viral_type"),
        "viral_score": c.get("viral", {}).get("viral_score"),
        "breakout_ratio": c.get("viral", {}).get("breakout_ratio"),
        "topic_match": c.get("semantic", {}).get("topic_match"),
        "format_class": c.get("format", {}).get("format_class"),
        "opportunity_score": op.get("opportunity_score"), "learning_value": qc.get("learning_value"),
        "why_viral": op.get("why_viral"), "why_useful": op.get("reason"),
        "final_score": c.get("final_score"),
    }


def rank(cands: list[dict], rules: dict, lane_id: str) -> tuple[list[dict], list[dict]]:
    """Trả (selected, shadow_ranked). Diversity: cùng kênh/cùng đề tài với video xếp trên bị phạt."""
    rk = rules["ranking"]
    alive = [c for c in cands if c.get("viral", {}).get("viral_pass") and c.get("semantic_pass")
             and c.get("format_pass")]
    for c in alive:
        c["final_score"] = final_score(c, rules)
    alive.sort(key=lambda c: c["final_score"], reverse=True)
    # phạt diversity theo thứ tự đã xếp (tham lam)
    placed: list[dict] = []
    for c in alive:
        pen = 0.0
        for p in placed:
            if p["channel_id"] == c["channel_id"]:
                pen += rk["diversity_penalty_same_channel"]
            elif _is_dup_topic(c["title"], [p["title"]], rk["same_topic_ratio"]):
                pen += rk["diversity_penalty_same_topic"]
        c["diversity_penalty"] = pen
        c["final_score"] = final_score(c, rules, diversity=max(0.0, 100.0 - pen))
        placed.append(c)
    alive.sort(key=lambda c: c["final_score"], reverse=True)

    selected, seen_ch = [], set()
    for c in alive:
        # alive đã đủ semantic/format/viral; còn lại: opportunity không REJECT + final QC PASS
        if c.get("opportunity", {}).get("decision") == "REJECT" or not c.get("final_qc_pass"):
            continue
        rec = selected_record(c, lane_id)
        missing = schemas.missing_critical(rec)
        if missing:
            c["flags"].append(f"MISSING_CRITICAL:{','.join(missing)}")
            continue
        if c["channel_id"] in seen_ch:
            continue  # ≤1 video/kênh/ngày (guide §18)
        seen_ch.add(c["channel_id"])
        c["selected_record"] = rec
        selected.append(c)
        if len(selected) >= rk["pick_per_lane"]:
            break
    for i, c in enumerate(alive, 1):
        c["shadow_rank"] = i
    return selected, alive
