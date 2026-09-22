# -*- coding: utf-8 -*-
"""H4 + H5 — Gemini semantic gate + format gate, GỘP 1 call/lô (guide §11, §12, §25).

Decision cuối do CODE tính từ điểm theo threshold trong hunt_rules.yaml (model vẫn được yêu cầu
tự ghi decision — chỉ để đối chiếu; ghi lệch → cờ MODEL_DECISION_MISMATCH). UNCERTAIN → gọi lại
1 lần đơn lẻ. Model lỗi/parse lỗi → status ERROR, candidate KHÔNG PASS (guide §33).
"""
from __future__ import annotations

from pathlib import Path

from hunt_v2 import schemas
from hunt_v2.lane_profile import LaneProfile
from hunt_v2.llm_client import LlmClient

PROMPT = (Path(__file__).parent / "prompts" / "semantic_format_v1.txt").read_text(encoding="utf-8")
GATE = "semantic_format"


def _video_block(c: dict, n_desc: int) -> str:
    desc = (c.get("description") or "").replace("\n", " ")[:n_desc]
    tags = ", ".join((c.get("tags") or [])[:15])
    return (f"- video_id={c['video_id']}\n  title={c['title']}\n  channel={c.get('channel', '')}\n"
            f"  duration_min={round((c.get('duration_s') or 0) / 60)} views={c.get('views')} "
            f"age_days={c.get('age_days')} keyword_match_score={c.get('keyword_match_score', 0)}\n"
            f"  tags={tags}\n  description={desc}")


def build_prompt(cands: list[dict], lane: LaneProfile, rules: dict) -> str:
    s, f = rules["semantic"], rules["format"]
    return PROMPT.format(
        lane_profile=lane.prompt_block(), examples=lane.examples_block(s["examples_each"]),
        t_pass=s["pass"]["topic_match"], a_pass=s["pass"]["audience_match"],
        c_pass=s["pass"]["content_identity_match"], t_rej=s["reject"]["topic_match"],
        c_rej=s["reject"]["content_identity_match"], f_conf=f["min_confidence"],
        allowed_formats=", ".join(lane.allowed_formats) or ", ".join(f["allowed_default"]),
        excluded_formats=", ".join(lane.excluded_formats),
        videos="\n".join(_video_block(c, s["description_chars"]) for c in cands))


def code_decision_semantic(sem: dict, rules: dict) -> str:
    p, r = rules["semantic"]["pass"], rules["semantic"]["reject"]
    if sem["topic_match"] < r["topic_match"] or sem["content_identity_match"] < r["content_identity_match"]:
        return "REJECT"
    if (sem["topic_match"] >= p["topic_match"] and sem["audience_match"] >= p["audience_match"]
            and sem["content_identity_match"] >= p["content_identity_match"]):
        return "PASS"
    return "UNCERTAIN"


def code_decision_format(fmt: dict, lane: LaneProfile, rules: dict) -> str:
    allowed = set(lane.allowed_formats) or set(rules["format"]["allowed_default"])
    fc = fmt["format_class"]
    excluded_hard = {"NEWS", "INTERVIEW", "PODCAST", "VLOG_PERSON", "TALK_SHOW", "TV_CLIP",
                     "REACTION", "REUP"}
    if fc in excluded_hard or fmt.get("host_driven") or fmt.get("interview_style"):
        return "REJECT"
    # allowed_formats trong profile là tên kiểu "narration"/"manga_story" — map lỏng theo nhóm story
    story_like = {"NARRATED_STORY", "AI_STORY", "STOCK_STORY", "SLIDESHOW", "DOCUMENTARY"}
    if fc in story_like and fmt["format_confidence"] >= rules["format"]["min_confidence"]:
        return "PASS"
    if fc == "UNKNOWN" or fmt["format_confidence"] < rules["format"]["min_confidence"]:
        return "UNCERTAIN"
    return "PASS" if fc in allowed else "UNCERTAIN"


def _attach(c: dict, item: dict, lane: LaneProfile, rules: dict) -> None:
    sem, fmt = item.get("semantic") or {}, item.get("format") or {}
    errs = schemas.validate("semantic", sem) + schemas.validate("format", fmt)
    if errs:
        c["semantic"] = {"decision": "ERROR", "errors": errs[:5]}
        c["format"] = {"decision": "ERROR"}
        c["flags"].append("GATE_SCHEMA_ERROR")
        return
    model_dec = sem.get("decision")
    sem["model_decision"] = model_dec
    sem["decision"] = code_decision_semantic(sem, rules)
    if model_dec != sem["decision"]:
        c["flags"].append("MODEL_DECISION_MISMATCH")
    fmt["model_decision"] = fmt.get("decision")
    fmt["decision"] = code_decision_format(fmt, lane, rules)
    c["semantic"], c["format"] = sem, fmt


def run(cands: list[dict], lane: LaneProfile, client: LlmClient, rules: dict,
        flags: dict) -> list[dict]:
    """Gắn c["semantic"], c["format"], c["semantic_pass"], c["format_pass"]. Gate tắt → SKIPPED."""
    if not (flags.get("semantic_gate") or flags.get("format_gate")):
        for c in cands:
            c["semantic"] = {"decision": "SKIPPED"}
            c["format"] = {"decision": "SKIPPED"}
            c["semantic_pass"] = c["format_pass"] = False
        return cands
    bs = rules["semantic"]["batch_size"]
    for i in range(0, len(cands), bs):
        _run_batch(cands[i:i + bs], lane, client, rules)

    # LẤP CHỖ THIẾU: model trả JSON hợp lệ nhưng BỎ BỚT video trong lô (đo thật 2026-09-22:
    # 39/200 video = 20% bị bỏ im lặng, không lỗi nào). Hỏi lại riêng những video bị bỏ, theo lô
    # nhỏ. Không làm bước này thì 1/5 pool bị loại oan mà chỉ hiện ra dưới dạng "ERROR".
    gb = max(1, rules["semantic"].get("gapfill_batch_size", 5))
    missing = [c for c in cands if c["semantic"].get("decision") == "ERROR"]
    for c in missing:
        c["flags"].append("GAPFILL_RETRIED")
    for i in range(0, len(missing), gb):
        _run_batch(missing[i:i + gb], lane, client, rules, use_cache=False)
    # UNCERTAIN → chấm lại 1 lần (guide §25), theo LÔ NHỎ chứ không từng video một: gọi đơn lẻ
    # 45 video × ~60s = 45 phút/lane, nhân 9 lane là không chạy nổi trong ngày. Lô 5 vẫn giúp model
    # tập trung hơn lô 15 mà chỉ tốn ~9 lượt gọi.
    rb = max(1, rules["semantic"].get("uncertain_batch_size", 5))
    retry = [c for c in cands if "UNCERTAIN" in (c["semantic"].get("decision"), c["format"].get("decision"))]
    retry = retry[: rules["semantic"].get("max_uncertain_retry", 40)]
    for c in retry:
        c["flags"].append("UNCERTAIN_RETRIED")
    for i in range(0, len(retry), rb):
        _run_batch(retry[i:i + rb], lane, client, rules, use_cache=False)
    for c in cands:
        c["semantic_pass"] = c["semantic"].get("decision") == "PASS"
        c["format_pass"] = c["format"].get("decision") == "PASS"
    return cands


def _run_batch(batch: list[dict], lane: LaneProfile, client: LlmClient, rules: dict,
               use_cache: bool = True) -> None:
    ids = [c["video_id"] for c in batch]
    res = client.call(GATE, build_prompt(batch, lane, rules), ids, schema_name=None,
                      expect_list=True, use_cache=use_cache)
    by_id = {}
    if res.ok and isinstance(res.parsed_response, list):
        by_id = {str(it.get("video_id")): it for it in res.parsed_response if isinstance(it, dict)}
    for c in batch:
        c.setdefault("flags", [])
        if res.fallback_used:
            c["flags"].append("FALLBACK_MODEL")
        item = by_id.get(c["video_id"])
        if not res.ok or item is None:
            c["semantic"] = {"decision": "ERROR", "errors": [res.error or "thiếu video trong output"]}
            c["format"] = {"decision": "ERROR"}
            c["flags"].append("GATE_ERROR")
            continue
        _attach(c, item, lane, rules)
        c["semantic"]["model"] = res.model
