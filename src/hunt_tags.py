# -*- coding: utf-8 -*-
"""Đọc pool từ khoá + đề tài đã làm của 1 lane từ tab lane trên Google Sheet.

CHỈ ĐỌC — không bao giờ ghi vào tab lane. Cột F = tag (phân tách dấu phẩy, có thể lẫn
dấu phẩy Nhật「、」), cột B = mô tả đề tài, cột E = title đã đăng (dùng để chống trùng
đề tài với video Video Hunt tìm được).
"""
from __future__ import annotations

import re

_SPLIT = re.compile(r"[,、]")


def _split_tags(cell: str) -> list[str]:
    return [t.strip() for t in _SPLIT.split(cell or "") if t.strip()]


def lane_keywords(rep, lane_cfg: dict, stop_tags: list[str]) -> list[str]:
    """Pool từ khoá = tag cột F (mọi dòng) ∪ seed_tags, trừ stop_tags (quá chung)."""
    stop = {t.strip() for t in stop_tags}
    seen: dict[str, None] = {}
    for s in lane_cfg.get("seed_tags", []):
        seen.setdefault(s, None)

    try:
        ws = rep.sh.worksheet(lane_cfg["tab"])
        col_f = ws.col_values(6)[1:]  # bỏ header dòng 1
    except Exception:
        col_f = []
    for cell in col_f:
        for tag in _split_tags(cell):
            if tag not in stop and len(tag) >= 2:
                seen.setdefault(tag, None)
    return list(seen)


def lane_done_titles(rep, lane_cfg: dict) -> list[str]:
    """Tiêu đề/mô tả đề tài lane ĐÃ LÀM — dùng để loại video trùng đề tài."""
    try:
        ws = rep.sh.worksheet(lane_cfg["tab"])
        col_b = ws.col_values(2)[1:]
        col_e = ws.col_values(5)[1:]
    except Exception:
        return []
    out = [c for c in col_b if c and len(c) > 5]
    out += [c for c in col_e if c and len(c) > 3]
    return out
