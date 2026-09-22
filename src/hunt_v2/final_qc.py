# -*- coding: utf-8 -*-
"""H8 — GPT-5.6 Sol final audit, độc lập, shortlist nhỏ (guide §16, §33).

Prompt ép "tự đánh giá TRƯỚC rồi mới đọc assessment cũ". fatal_issue != null → final_qc_pass=False.
API lỗi → status ERROR (KHÔNG PASS). Không có fallback sang model khác — Sol phải là model khác hẳn
Gemini/Claude để "độc lập" có nghĩa; thiếu Sol thì hôm đó V2 không production-select.
"""
from __future__ import annotations

import json
from pathlib import Path

from hunt_v2.lane_profile import LaneProfile
from hunt_v2.llm_client import LlmClient
from hunt_v2.opportunity_gate import candidate_fields

PROMPT = (Path(__file__).parent / "prompts" / "finalqc_v1.txt").read_text(encoding="utf-8")
GATE = "final_qc"


def build_prompt(c: dict, lane: LaneProfile) -> str:
    f = candidate_fields(c)
    f["opportunity"] = json.dumps(c.get("opportunity", {}), ensure_ascii=False)
    return PROMPT.format(lane_profile=lane.prompt_block(), **f)


def run(cands: list[dict], lane: LaneProfile, client: LlmClient, enabled: bool) -> list[dict]:
    for c in cands:
        c.setdefault("flags", [])
        if not enabled:
            c["final_qc"] = {"decision": "SKIPPED", "status": "SKIPPED"}
            c["final_qc_pass"] = False
            continue
        res = client.call(GATE, build_prompt(c, lane), [c["video_id"]], schema_name="final_qc")
        if not res.ok or res.schema_errors:
            c["final_qc"] = {"decision": "ERROR", "status": "ERROR",
                             "errors": [res.error] if res.error else res.schema_errors[:5]}
            c["final_qc_pass"] = False
            c["flags"].append("FINAL_QC_ERROR")
            continue
        qc = res.parsed_response
        qc["status"] = "OK"
        qc["model"] = res.model
        if qc.get("fatal_issue"):
            qc["decision"] = "REJECT"
        c["final_qc"] = qc
        c["final_qc_pass"] = qc["decision"] == "PASS"
    return cands
