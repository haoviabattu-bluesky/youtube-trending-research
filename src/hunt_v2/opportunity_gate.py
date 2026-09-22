# -*- coding: utf-8 -*-
"""H7 — Claude opportunity analysis trên shortlist sau viral engine (guide §15).

Chạy qua `claude -p --model sonnet` (gói Claude Code, không tốn API key) — xem models.yaml.
REJECT chỉ theo fatal rules trong hunt_rules.yaml (dependency quá cao / production thấp);
UNCERTAIN được giữ khi viral_score cực cao (guide §25). Lỗi → ERROR, không PASS.
"""
from __future__ import annotations

import json
from pathlib import Path

from hunt_v2 import schemas
from hunt_v2.lane_profile import LaneProfile
from hunt_v2.llm_client import LlmClient

PROMPT = (Path(__file__).parent / "prompts" / "opportunity_v1.txt").read_text(encoding="utf-8")
GATE = "opportunity"


def candidate_fields(c: dict, n_desc: int = 800) -> dict:
    """Field chung cho prompt opportunity + final_qc."""
    return {
        "video_id": c["video_id"], "title": c["title"], "channel": c.get("channel", ""),
        "subs": c.get("subs", 0), "ch_age_days": c.get("ch_age_days"),
        "published_at": c.get("published_at", ""), "age_days": c.get("age_days"),
        "duration_min": round((c.get("duration_s") or 0) / 60), "views": c.get("views"),
        "likes": c.get("likes"), "comments": c.get("comments"),
        "tags": ", ".join((c.get("tags") or [])[:20]),
        "description": (c.get("description") or "").replace("\n", " ")[:n_desc],
        "viral": json.dumps(c.get("viral", {}), ensure_ascii=False),
        "semantic": json.dumps(c.get("semantic", {}), ensure_ascii=False),
        "format": json.dumps(c.get("format", {}), ensure_ascii=False),
    }


def build_prompt(c: dict, lane: LaneProfile, rules: dict) -> str:
    negs = "\n".join(f"- {n.get('pattern') or n.get('title', '')} — {n.get('reason', '')}"
                     for n in lane.negatives[: rules["semantic"]["examples_each"] * 2]) or "- (none)"
    return PROMPT.format(lane_profile=lane.prompt_block(), negatives=negs, **candidate_fields(c))


def code_decision(op: dict, viral_score: float, rules: dict) -> str:
    r = rules["opportunity"]["reject_if"]
    fatal = []
    if op["celebrity_dependency"] >= r["celebrity_dependency"]:
        fatal.append("CELEBRITY_DEPENDENCY")
    if op["external_event_dependency"] >= r["external_event_dependency"]:
        fatal.append("NEWS_DEPENDENCY")
    if op["production_compatibility"] < r["production_compatibility_below"]:
        fatal.append("NOT_REPLICABLE")
    op["fatal_flags"] = sorted(set(op.get("fatal_flags") or []) | set(fatal))
    if fatal or op["model_decision"] == "REJECT":
        return "REJECT"
    if op["model_decision"] == "UNCERTAIN":
        return "UNCERTAIN" if viral_score < rules["opportunity"]["keep_uncertain_if_viral_score"] \
            else "PASS"
    return "PASS"


def run(cands: list[dict], lane: LaneProfile, client: LlmClient, rules: dict, enabled: bool) -> list[dict]:
    """cands = shortlist (đã cắt shortlist_n ở runner). Gắn c["opportunity"], c["opportunity_pass"]."""
    for c in cands:
        c.setdefault("flags", [])
        if not enabled:
            c["opportunity"] = {"decision": "SKIPPED"}
            c["opportunity_pass"] = False
            continue
        res = client.call(GATE, build_prompt(c, lane, rules), [c["video_id"]], schema_name="opportunity")
        if res.fallback_used:
            c["flags"].append("FALLBACK_MODEL")
        if not res.ok or res.schema_errors:
            c["opportunity"] = {"decision": "ERROR",
                                "errors": [res.error] if res.error else res.schema_errors[:5]}
            c["opportunity_pass"] = False
            c["flags"].append("OPPORTUNITY_ERROR")
            continue
        op = res.parsed_response
        op["model_decision"] = op["decision"]
        op["decision"] = code_decision(op, c.get("viral", {}).get("viral_score", 0), rules)
        op["model"] = res.model
        c["opportunity"] = op
        c["opportunity_pass"] = op["decision"] == "PASS"
        if op["decision"] == "UNCERTAIN":
            c["flags"].append("OPPORTUNITY_UNCERTAIN")
    return cands
