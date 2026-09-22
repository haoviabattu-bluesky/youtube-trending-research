# -*- coding: utf-8 -*-
"""Hàng rào Sheet: tab audit trong whitelist, writer chỉ append, feedback chỉ đọc."""
import re
from pathlib import Path

import pytest

from hunt_v2 import audit_writer, shadow_report
from sheet_schema import HEADERS, SheetGuardError, _assert_allowed
from conftest import ROOT


def test_audit_tab_allowed_but_unprefixed_not():
    _assert_allowed("TRD_HUNT_AUDIT")
    with pytest.raises(SheetGuardError):
        _assert_allowed("HUNT_AUDIT")


def test_audit_row_matches_header():
    c = {"video_id": "abc", "title": "t", "channel": "ch", "views": 10, "age_days": 2.0,
         "viral": {"vpd": 5, "vph": 0.2, "viral_type": "BOTH", "viral_score": 80.5, "breakout_ratio": 3.1},
         "semantic": {"topic_match": 90, "semantic_confidence": 80}, "format": {"format_class": "AI_STORY"},
         "opportunity": {"opportunity_score": 85, "why_viral": ["A", "B"], "reason": "why"},
         "final_qc": {"decision": "REJECT", "fatal_issue": "TV_CLIP", "independent_confidence": 70},
         "flags": ["X"]}
    row = audit_writer.audit_row(c, "L", "2026-09-22", 1, True, False, "SHADOW", "run1")
    h = HEADERS["TRD_HUNT_AUDIT"]
    assert len(row) == len(h)
    d = dict(zip(h, row))
    assert d["VIDEO_URL"] == "https://youtu.be/abc" and d["FINAL_QC"] == "REJECT:TV_CLIP"
    assert d["HUMAN_DECISION"] == "" and d["REJECT_REASON"] == ""
    assert d["OLD_SELECTED"] == "TRUE" and d["WHY_VIRAL"] == "A, B"


def test_v2_code_never_calls_delete_or_clear():
    """grep cứng: gói hunt_v2 không được gọi API xoá/clear của gspread hay update dòng audit."""
    banned = re.compile(r"\b(delete_rows|delete_dimension|batch_clear|\.clear\(|delete_columns|clear_basic_filter)\b")
    for p in (ROOT / "src" / "hunt_v2").glob("*.py"):
        assert not banned.search(p.read_text(encoding="utf-8")), p.name
    aw = (ROOT / "src" / "hunt_v2" / "audit_writer.py").read_text(encoding="utf-8")
    assert "batch_update" not in aw and ".update(" not in aw


class _Rep:
    def __init__(self):
        self.appended = []
        self.vals = [HEADERS["TRD_HUNT_AUDIT"]]

    def ensure_tab(self, tab):
        assert tab == "TRD_HUNT_AUDIT"
        rep = self

        class WS:
            def get_all_values(self_inner):
                return rep.vals
        return WS()

    def append(self, tab, rows):
        self.appended += rows
        self.vals += rows
        return len(rows)


def test_audit_write_is_idempotent_within_day():
    rep = _Rep()
    c = {"video_id": "v1", "title": "t", "flags": []}
    row = audit_writer.audit_row(c, "L", "2026-09-22", 1, False, False, "SHADOW", "r")
    assert audit_writer.write(rep, [row], "2026-09-22") == 1
    assert audit_writer.write(rep, [row], "2026-09-22") == 0


def test_read_human_feedback_only_filled_rows():
    rep = _Rep()
    h = HEADERS["TRD_HUNT_AUDIT"]
    r1 = [""] * len(h)
    r1[h.index("VIDEO_ID")], r1[h.index("LANE")], r1[h.index("HUMAN_DECISION")] = "v1", "L", "accept"
    r2 = [""] * len(h)
    r2[h.index("VIDEO_ID")] = "v2"
    rep.vals += [r1, r2]
    fb = audit_writer.read_human_feedback(rep)
    assert fb == [{"video_id": "v1", "lane": "L", "decision": "ACCEPT", "reason": "", "date": "", "title": ""}]


def test_shadow_rows_old_fallback_mode():
    class R2:
        selected, shadow_ranked, run_id, error, counts = [], [], "rid", None, {}
    rows = shadow_report._rows_for_lane("L", [{"video_id": "o1", "title": "t", "vpd": 1}], R2(), "2026-09-22", shadow=False)
    d = dict(zip(HEADERS["TRD_HUNT_AUDIT"], rows[0]))
    assert d["RUN_MODE"] == "OLD_FALLBACK" and d["OLD_SELECTED"] == "TRUE" and d["RANK"] == "101"
