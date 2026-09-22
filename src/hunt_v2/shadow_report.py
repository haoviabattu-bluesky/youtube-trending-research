# -*- coding: utf-8 -*-
"""Shadow mode (guide §31): in bảng OLD vs V2 ra log + ghi tab TRD_HUNT_AUDIT.

Mỗi lane/ngày ghi: pick OLD (RANK old-1..2) + top `shadow_top_n` V2 (RANK v2-1..5); video vừa
OLD vừa V2 chỉ 1 dòng (OLD_SELECTED & V2_SELECTED đều TRUE). RUN_MODE: SHADOW | PRODUCTION |
OLD_FALLBACK (production nhưng V2 không chọn được → RESEARCH giữ pick cũ).
"""
from __future__ import annotations

from hunt_v2 import audit_writer

SHADOW_TOP_N = 5


def _rows_for_lane(name: str, old_picks: list[dict], r2, snap: str, shadow: bool) -> list[list[str]]:
    old_ids = {p["video_id"] for p in old_picks}
    v2_sel_ids = {c["video_id"] for c in (r2.selected if r2 else [])}
    if shadow:
        mode = "SHADOW"
    else:
        mode = "PRODUCTION" if v2_sel_ids else "OLD_FALLBACK"
    run_id = r2.run_id if r2 else "old-only"
    rows, seen = [], set()
    top = (r2.shadow_ranked if r2 else [])[:SHADOW_TOP_N]
    for i, c in enumerate(top, 1):
        seen.add(c["video_id"])
        rows.append(audit_writer.audit_row(c, name, snap, i, c["video_id"] in old_ids,
                                           c["video_id"] in v2_sel_ids, mode, run_id))
    for i, p in enumerate(old_picks, 1):
        if p["video_id"] in seen:
            continue
        # pick cũ không nằm trong top V2 — vẫn ghi để so; số liệu V2 (nếu có) lấy từ shadow_ranked
        c = next((x for x in (r2.shadow_ranked if r2 else []) if x["video_id"] == p["video_id"]), None)
        c = c or {**p, "viral": {"vpd": p.get("vpd")}, "flags": ["OLD_ONLY:not_in_v2_pool"]}
        rows.append(audit_writer.audit_row(c, name, snap, 100 + i, True,
                                           p["video_id"] in v2_sel_ids, mode, run_id))
    return rows


def print_compare(names: list[str], all_picks: dict, v2_results: dict, shadow: bool, log) -> None:
    log("\n[v2] so sánh OLD vs V2 — mode " + ("SHADOW (RESEARCH = OLD)" if shadow else "PRODUCTION"))
    log(f"{'lane':22} | {'OLD top':<26} | {'V2 top':<26} | trùng")
    for name in names:
        old = [p["video_id"] for p in all_picks.get(name, [])]
        r2 = v2_results.get(name)
        v2 = [c["video_id"] for c in (r2.selected if r2 else [])]
        v2s = [c["video_id"] for c in (r2.shadow_ranked if r2 else [])[:2]]
        shown = v2 or [f"({v})" for v in v2s]  # ngoặc = shadow rank, chưa đủ 4 cờ
        overlap = len(set(old) & set(v2 or v2s))
        err = f"  !! {r2.error}" if (r2 and r2.error) else ("  (v2 lỗi)" if r2 is None else "")
        log(f"{name:22} | {' '.join(old):<26} | {' '.join(shown):<26} | {overlap}{err}")
        if r2 and r2.counts:
            log(f"{'':22}   phễu: {r2.counts}")


def write_audit(rep, names: list[str], all_picks: dict, v2_results: dict, snap: str,
                shadow: bool) -> int:
    rows: list[list[str]] = []
    for name in names:
        rows += _rows_for_lane(name, all_picks.get(name, []), v2_results.get(name), snap, shadow)
    return audit_writer.write(rep, rows, snap)
