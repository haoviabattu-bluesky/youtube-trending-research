# -*- coding: utf-8 -*-
"""H10 — tab TRD_HUNT_AUDIT (guide §19, §31): full audit trail, CHỈ APPEND.

Không bao giờ update dòng đã có — cột HUMAN_DECISION/REJECT_REASON là của user gõ tay, ghi đè
là mất dữ liệu học. Chống trùng khi chạy lại trong ngày: đọc (DATE, LANE, VIDEO_ID) đã có, bỏ qua.
Cũng CHỈ ĐỌC tab này để lấy human feedback (feedback.py).
"""
from __future__ import annotations

from gapi import retry_api
from sheet_schema import HEADERS

TAB = "TRD_HUNT_AUDIT"
H = HEADERS[TAB]


def _cell(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return ", ".join(map(str, v))
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    return str(v)


def audit_row(c: dict, lane: str, snap: str, rank: int, old_sel: bool, v2_sel: bool,
              run_mode: str, run_id: str) -> list[str]:
    v, s, f = c.get("viral", {}), c.get("semantic", {}), c.get("format", {})
    op, qc = c.get("opportunity", {}), c.get("final_qc", {})
    conf = qc.get("independent_confidence") or s.get("semantic_confidence")
    qc_txt = qc.get("decision", "") if qc else ""
    if qc.get("fatal_issue"):
        qc_txt = f"REJECT:{qc['fatal_issue']}"
    row = {
        "DATE": snap, "LANE": lane, "RANK": rank, "VIDEO_URL": f"https://youtu.be/{c['video_id']}",
        "TITLE": c.get("title", ""), "CHANNEL": c.get("channel", ""),
        "PUBLISHED_AT": (c.get("published_at") or "")[:10], "AGE_DAYS": c.get("age_days"),
        "VIEWS": c.get("views"), "VPD": v.get("vpd", c.get("vpd")), "VPH": v.get("vph"),
        "BREAKOUT_RATIO": v.get("breakout_ratio"), "VIRAL_TYPE": v.get("viral_type"),
        "VIRAL_SCORE": v.get("viral_score"), "TOPIC_MATCH": s.get("topic_match"),
        "FORMAT_CLASS": f.get("format_class"), "OPPORTUNITY_SCORE": op.get("opportunity_score"),
        "FINAL_QC": qc_txt, "WHY_VIRAL": op.get("why_viral"), "WHY_USEFUL": op.get("reason"),
        "CONFIDENCE": conf, "HUMAN_DECISION": "", "REJECT_REASON": "",
        "OLD_SELECTED": old_sel, "V2_SELECTED": v2_sel, "RUN_MODE": run_mode, "RUN_ID": run_id,
        "FLAGS": c.get("flags", []), "VIDEO_ID": c["video_id"],
    }
    return [_cell(row.get(h)) for h in H]


def existing_keys(rep, snap: str) -> set[tuple[str, str, str]]:
    """(DATE, LANE, VIDEO_ID) đã có trong tab cho ngày snap — 1 request."""
    ws = rep.ensure_tab(TAB)
    vals = retry_api(ws.get_all_values)
    if not vals:
        return set()
    hdr = vals[0]
    try:
        i_d, i_l, i_v = hdr.index("DATE"), hdr.index("LANE"), hdr.index("VIDEO_ID")
    except ValueError:
        return set()
    out = set()
    for r in vals[1:]:
        if len(r) > max(i_d, i_l, i_v) and r[i_d] == snap:
            out.add((r[i_d], r[i_l], r[i_v]))
    return out


def write(rep, rows: list[list[str]], snap: str) -> int:
    """Append các dòng chưa có (theo DATE/LANE/VIDEO_ID). Trả số dòng ghi."""
    if not rows:
        return 0
    have = existing_keys(rep, snap)
    i_d, i_l, i_v = H.index("DATE"), H.index("LANE"), H.index("VIDEO_ID")
    fresh = [r for r in rows if (r[i_d], r[i_l], r[i_v]) not in have]
    return rep.append(TAB, fresh)


def read_human_feedback(rep) -> list[dict]:
    """CHỈ ĐỌC: mọi dòng có HUMAN_DECISION khác rỗng → [{video_id, lane, decision, reason, date, title}]."""
    ws = rep.ensure_tab(TAB)
    vals = retry_api(ws.get_all_values)
    if len(vals) < 2:
        return []
    hdr = vals[0]
    idx = {h: hdr.index(h) for h in ("DATE", "LANE", "VIDEO_ID", "HUMAN_DECISION", "REJECT_REASON",
                                     "TITLE") if h in hdr}
    out = []
    for r in vals[1:]:
        g = lambda k: r[idx[k]] if k in idx and len(r) > idx[k] else ""  # noqa: E731
        dec = g("HUMAN_DECISION").strip().upper()
        if dec:
            out.append({"video_id": g("VIDEO_ID"), "lane": g("LANE"), "decision": dec,
                        "reason": g("REJECT_REASON").strip().upper(), "date": g("DATE"),
                        "title": g("TITLE")})
    return out
