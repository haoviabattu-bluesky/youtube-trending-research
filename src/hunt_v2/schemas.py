# -*- coding: utf-8 -*-
"""Schema output của từng gate + hàm validate (guide §11/§12/§15/§16/§36).

Validator tự viết (không thêm dependency): kiểm tra key bắt buộc, kiểu, enum, dải 0–100.
Trả LIST lỗi (rỗng = hợp lệ) để caller ghi vào log thay vì ném — guide §24: không nuốt
lỗi parse im lặng, nhưng cũng không làm sập cả lô vì 1 video.
"""
from __future__ import annotations

DECISION3 = ("PASS", "REJECT", "UNCERTAIN")
DECISION2 = ("PASS", "REJECT")
FORMAT_CLASSES = ("NARRATED_STORY", "AI_STORY", "STOCK_STORY", "SLIDESHOW", "DOCUMENTARY",
                  "NEWS", "INTERVIEW", "PODCAST", "VLOG_PERSON", "TALK_SHOW", "TV_CLIP",
                  "REACTION", "REUP", "UNKNOWN")
VIRAL_TYPES = ("MARKET_TREND", "CHANNEL_BREAKOUT", "BOTH", "NORMAL")
FATAL_ISSUES = ("WRONG_NICHE", "WRONG_AUDIENCE", "INTERVIEW_DEPENDENCY", "CELEBRITY_DEPENDENCY",
                "NEWS_DEPENDENCY", "REAL_PERSON_FORMAT", "TV_CLIP", "REUP_RISK", "NOT_REPLICABLE",
                "MISLEADING_VIRAL_METRIC")
REJECT_REASONS = ("WRONG_TOPIC", "WRONG_AUDIENCE", "WRONG_FORMAT", "REAL_PERSON", "INTERVIEW",
                  "NEWS", "CELEBRITY", "TOO_GENERIC", "NOT_REPLICABLE", "BAD_CHANNEL",
                  "LOW_VALUE", "OTHER")
HUMAN_DECISIONS = ("ACCEPT", "REJECT", "SKIP")

# name -> {field: (type, extra)}; extra = enum tuple | "score" (0–100) | None
SCHEMAS: dict[str, dict[str, tuple]] = {
    "semantic": {
        "topic_match": (int, "score"), "audience_match": (int, "score"),
        "content_identity_match": (int, "score"), "market_language_match": (int, "score"),
        "semantic_confidence": (int, "score"), "decision": (str, DECISION3),
        "reasons": (list, None), "matched_topics": (list, None), "mismatch_flags": (list, None),
    },
    "format": {
        "format_class": (str, FORMAT_CLASSES), "real_person_present": (bool, None),
        "host_driven": (bool, None), "interview_style": (bool, None), "news_style": (bool, None),
        "format_confidence": (int, "score"), "decision": (str, DECISION3), "reason": (str, None),
    },
    "opportunity": {
        "why_viral": (list, None), "transferability": (int, "score"),
        "topic_reusability": (int, "score"), "hook_reusability": (int, "score"),
        "audience_compatibility": (int, "score"), "production_compatibility": (int, "score"),
        "channel_authority_dependency": (int, "score"), "external_event_dependency": (int, "score"),
        "celebrity_dependency": (int, "score"), "opportunity_score": (int, "score"),
        "decision": (str, DECISION3), "fatal_flags": (list, None), "reason": (str, None),
    },
    "final_qc": {
        "semantic_fit": (int, "score"), "format_fit": (int, "score"),
        "viral_validity": (int, "score"), "learning_value": (int, "score"),
        "independent_confidence": (int, "score"), "fatal_issue": (object, None),
        "disagreements": (list, None), "decision": (str, DECISION2), "reason": (str, None),
    },
}

# Field critical của record được chọn (guide §36) — thiếu 1 → DO NOT SELECT.
# `breakout_ratio` CỐ Ý không nằm đây dù guide có liệt kê: kênh chưa lấy được baseline (hết quota
# Data API / kênh mới) thì nó = None hợp lệ, mà viral_pass đã là cổng riêng cho tín hiệu viral.
# Để nó vào critical là chặn IM LẶNG mọi lượt chọn khi baseline trống (đã dính thật 2026-09-22:
# 5 ứng viên qua cả 4 cổng vẫn ra SELECTED rỗng). Thiếu baseline → gắn cờ BASELINE_MISSING ở audit.
SELECTED_CRITICAL = ("video_id", "url", "lane_id", "semantic_pass", "format_pass", "viral_pass",
                     "final_qc_pass", "viral_type", "viral_score", "topic_match",
                     "format_class", "opportunity_score", "learning_value", "why_viral",
                     "why_useful", "final_score")


def _coerce_int(v):
    """Model hay trả 87.0 hoặc "87" — chấp nhận, ép về int."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return int(round(v))
    if isinstance(v, str) and v.strip().lstrip("-").replace(".", "", 1).isdigit():
        return int(round(float(v)))
    return None


def validate(name: str, obj) -> list[str]:
    """Trả list lỗi; đồng thời ÉP KIỂU tại chỗ các số/enum để downstream dùng an toàn."""
    spec = SCHEMAS[name]
    if not isinstance(obj, dict):
        return [f"{name}: không phải object"]
    errs = []
    for field, (typ, extra) in spec.items():
        if field not in obj:
            errs.append(f"{name}.{field}: thiếu")
            continue
        v = obj[field]
        if typ is int:
            iv = _coerce_int(v)
            if iv is None:
                errs.append(f"{name}.{field}: không phải số ({v!r})")
                continue
            if extra == "score" and not 0 <= iv <= 100:
                errs.append(f"{name}.{field}: ngoài 0–100 ({iv})")
                continue
            obj[field] = iv
        elif typ is bool:
            if isinstance(v, str) and v.lower() in ("true", "false"):
                obj[field] = v.lower() == "true"
            elif not isinstance(v, bool):
                errs.append(f"{name}.{field}: không phải bool ({v!r})")
        elif typ is list:
            if v is None:
                obj[field] = []
            elif not isinstance(v, list):
                errs.append(f"{name}.{field}: không phải list")
        elif typ is str:
            if not isinstance(v, str):
                errs.append(f"{name}.{field}: không phải chuỗi")
                continue
            if isinstance(extra, tuple):
                up = v.strip().upper()
                if up not in extra:
                    errs.append(f"{name}.{field}: {v!r} không thuộc {extra}")
                    continue
                obj[field] = up
        elif typ is object:
            if isinstance(v, str) and v.strip().lower() in ("", "null", "none"):
                obj[field] = None
    if name == "final_qc" and obj.get("fatal_issue") not in (None,) + FATAL_ISSUES:
        errs.append(f"final_qc.fatal_issue: {obj.get('fatal_issue')!r} không thuộc enum")
    return errs


def missing_critical(record: dict) -> list[str]:
    return [k for k in SELECTED_CRITICAL if record.get(k) in (None, "", [])]
