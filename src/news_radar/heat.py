# -*- coding: utf-8 -*-
"""Chấm điểm THUẦN cho 1 cụm sự kiện (không mạng, không DB — test được bằng số giả).

heat     = Σ_source weight × điểm nguồn, × thưởng khi xuất hiện ở ≥2 nguồn
velocity = heat hôm nay / heat lần trước (cùng label); chưa từng thấy → 1.5 (sự kiện MỚI)
gap      = clamp(1.5 − 0.2·ln(1 + view_24h/đơn_vị + số_video), 0.5, 1.5) — chưa ai làm 1.5, bão hoà 0.5
final    = heat × min(velocity, cap) × gap × (floor + 0.1×giật_gân) × (0.5 nếu không phải tin)

Điểm nguồn (mỗi nguồn cho 1 cụm, lấy tín hiệu TỐT NHẤT của các keyword trong cụm):
- google_trends : 1 + log10(max(traffic,100)/100)   100+→1 · 1k+→2 · 10k+→3 · 100k+→4
- google_news   : 0.4 × số tiêu đề (trần 5)
- yahoo_ranking : max(0.2, 1.4 − 0.03×hạng tốt nhất) + 0.3 × số bài (trần 3)
- x_trends24    : max(0.2, 1.2 − 0.04×hạng tốt nhất) + hours/of   (bền nhiều giờ = +1 tối đa)
- x_getdaytrends: max(0.2, 1.2 − 0.05×hạng tốt nhất)"""
from __future__ import annotations

import math


def source_score(source: str, sigs: list[dict]) -> float:
    """sigs = signal của cụm thuộc `source`: {rank, traffic, extra}."""
    if not sigs:
        return 0.0
    best_rank = min(int(s.get("rank") or 999) for s in sigs)
    if source == "google_trends":
        tr = max(int(s.get("traffic") or 0) for s in sigs)
        return 1.0 + math.log10(max(tr, 100) / 100)
    if source == "google_news":
        return 0.4 * min(len(sigs), 5)
    if source == "yahoo_ranking":
        return max(0.2, 1.4 - 0.03 * best_rank) + 0.3 * min(len(sigs), 3)
    if source == "x_trends24":
        hours = max(float((s.get("extra") or {}).get("hours") or 0) for s in sigs)
        of = max(float((s.get("extra") or {}).get("of") or 1) for s in sigs)
        return max(0.2, 1.2 - 0.04 * best_rank) + min(1.0, hours / max(of, 1))
    if source == "x_getdaytrends":
        return max(0.2, 1.2 - 0.05 * best_rank)
    return 0.0


def heat_of(by_source: dict[str, list[dict]], cfg: dict) -> tuple[float, list[str]]:
    """by_source = {source: [signal...]}. Trả (heat, danh sách nguồn có mặt)."""
    w = cfg["source_weight"]
    present = [s for s, sigs in by_source.items() if sigs]
    total = sum(w.get(s, 0.5) * source_score(s, by_source[s]) for s in present)
    bonus = 1.0
    for k, v in sorted(cfg["multi_source_bonus"].items()):
        if len(present) >= int(k):
            bonus = float(v)
    return round(total * bonus, 3), present


def velocity_of(heat: float, prev_heat: float | None, cap: float) -> float:
    if prev_heat is None:
        return 1.5
    if prev_heat <= 0:
        return cap
    return round(min(cap, heat / prev_heat), 3)


def gap_of(supply_videos: int, supply_views: int, unit: int) -> float:
    """1.5 khi chưa ai làm → 0.5 khi bão hoà (≈ >150 đơn vị cung). Đo 17/10: công thức 1/ln cũ cho 片山さつき
    (28 video, 1,9M view — tin lớn nhất ngày) gap 0,18 → tụt xuống #8 dưới tin đời sống Yahoo; bão hoà chỉ là
    rủi ro đến muộn, không được giết hẳn tin lớn — brief sẽ bắt đổi góc."""
    x = supply_views / max(unit, 1) + supply_videos
    return round(max(0.5, min(1.5, 1.5 - 0.2 * math.log1p(x))), 3)


def final_of(heat: float, velocity: float, gap: float, sensational: int, is_news: bool, cfg: dict) -> float:
    sens = cfg["sensational_floor"] + 0.1 * max(1, min(5, int(sensational or 3)))
    return round(heat * min(velocity, cfg["velocity_cap"]) * gap * sens * (1.0 if is_news else 0.5), 3)


def score_cluster(by_source: dict[str, list[dict]], prev_heat: float | None, supply_videos: int,
                  supply_views: int, sensational: int, is_news: bool, cfg: dict) -> dict:
    heat, present = heat_of(by_source, cfg)
    vel = velocity_of(heat, prev_heat, cfg["velocity_cap"])
    gap = gap_of(supply_videos, supply_views, cfg["supply_view_unit"])
    return {"heat": heat, "sources": present, "velocity": vel, "gap": gap,
            "final": final_of(heat, vel, gap, sensational, is_news, cfg)}
