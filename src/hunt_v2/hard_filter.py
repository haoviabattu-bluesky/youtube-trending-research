# -*- coding: utf-8 -*-
"""H3 — hard filter CODE-ONLY (guide §10). Tái dùng hàm đã trả giá thật trong hunt_score.py.

KHÁC bản cũ: "title phải khớp ≥2 tag" KHÔNG còn là hard reject — chỉ thành feature
`keyword_match_score` 0–1 để đưa vào prompt semantic gate. Mọi loại đều ghi lý do.
"""
from __future__ import annotations

from hunt_score import _is_dup_topic, age_days_of, is_japanese_title, is_live_stream
from hunt_v2.lane_profile import LaneProfile


def keyword_match_score(title: str, kws: list[str], rules: dict) -> tuple[float, list[str]]:
    """Số tag (token ≥ min_token_len) xuất hiện trong tiêu đề / full_score_hits, clamp 0–1.
    Trả kèm danh sách token khớp để trace (guide §28)."""
    km = rules["keyword_match"]
    checkable = {p for kw in kws for p in kw.split() if len(p) >= km["min_token_len"]}
    if not checkable:
        return 0.0, []
    hits = sorted(p for p in checkable if p in (title or ""))
    return round(min(len(hits) / km["full_score_hits"], 1.0), 3), hits


def apply(rows: list[dict], lane: LaneProfile, rules: dict, already_picked: set[str],
          done_titles: list[str], kws: list[str]) -> tuple[list[dict], list[dict]]:
    """Trả (kept, rejected). kept có thêm age_days/vpd/keyword_match_score/matched_tags.
    Không sắp xếp; không cắt — runner cắt max_semantic_candidates_per_lane sau khi sort vpd."""
    hf = rules["hard_filter"]
    black = lane.blacklist_channels
    kept, rejected = [], []
    for r in rows:
        r = dict(r)
        age = age_days_of(r)
        r["age_days"] = round(age, 1)
        r["vpd"] = round(r["views"] / age, 1)
        reason = None
        lbc = (r.get("live_broadcast_content") or "none").lower()
        if r["video_id"] in already_picked:
            reason = "ALREADY_SELECTED"
        elif r["channel_id"] in black:
            reason = "CHANNEL_BLACKLIST"
        elif lbc != "none" or is_live_stream(r["title"]):
            reason = "LIVE_OR_PREMIERE"
        elif age > hf["max_age_days"]:
            reason = "AGE_GT_MAX"
        elif r["views"] < hf["min_views"]:
            reason = "VIEWS_LT_MIN"
        elif (r.get("duration_s") or 0) < max(hf["min_duration_s"], lane.duration_min_s):
            reason = "DURATION_TOO_SHORT"
        elif (r.get("duration_s") or 0) > min(hf["max_duration_s"], lane.duration_max_s):
            reason = "DURATION_TOO_LONG"
        elif hf.get("require_kana") and not is_japanese_title(r["title"]):
            reason = "NON_TARGET_LANGUAGE"
        elif _is_dup_topic(r["title"], done_titles):
            reason = "DUP_TOPIC_ALREADY_MADE"
        if reason:
            rejected.append({"video_id": r["video_id"], "title": r["title"], "reason": reason})
            continue
        r["keyword_match_score"], r["matched_tags"] = keyword_match_score(r["title"], kws, rules)
        r["flags"] = []
        kept.append(r)
    return kept, rejected
