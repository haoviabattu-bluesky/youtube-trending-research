# -*- coding: utf-8 -*-
"""H6 — viral engine, KHÔNG AI (guide §13, §14). Phân biệt "view lớn" với "viral thật".

Mọi sub-score 0–100, chuẩn hoá percentile TRONG pool của lane cùng lượt (pool nhỏ → log-scale).
viral_type: MARKET_TREND / CHANNEL_BREAKOUT / BOTH / NORMAL. Trọng số & ngưỡng ở hunt_rules.yaml.
"""
from __future__ import annotations

import math


def _pct_rank(values: list[float]) -> list[float]:
    """Percentile rank 0–100 (trung bình khi trùng)."""
    n = len(values)
    if n <= 1:
        return [50.0] * n
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2
        for k in range(i, j + 1):
            ranks[order[k]] = avg / (n - 1) * 100
        i = j + 1
    return ranks


def _log_scale(v: float, lo: float, hi: float) -> float:
    """log10 map [lo, hi] → 0–100, clamp. Dùng khi pool quá nhỏ để percentile."""
    if v <= 0:
        return 0.0
    x = (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
    return round(max(0.0, min(1.0, x)) * 100, 1)


def freshness(age_days: float, vr: dict) -> tuple[float, str]:
    fm = vr["freshness_mult"]
    if age_days <= 3:
        m, b = fm["d0_3"], "0-3"
    elif age_days <= 7:
        m, b = fm["d4_7"], "4-7"
    elif age_days <= 14:
        m, b = fm["d8_14"], "8-14"
    else:
        m, b = fm["d15_30"], "15-30"
    lo, hi = fm["d15_30"], fm["d0_3"]
    return round((m - lo) / (hi - lo) * 100, 1) if hi > lo else 50.0, b


def score(cands: list[dict], baselines: dict[str, dict | None], rules: dict) -> list[dict]:
    """Gắn cand["viral"] = {...} cho từng candidate. Trả cùng list (đã sửa tại chỗ)."""
    vr = rules["viral"]
    w = vr["weights"]
    n = len(cands)
    vph_list, vpd_list, abs_list, br_list = [], [], [], []
    for c in cands:
        age_h = max(float(c.get("age_hours") or 1), 1.0)
        age_d = max(age_h / 24, 0.25)
        c["_vph"] = c["views"] / age_h
        c["_vpd"] = c["views"] / age_d
        bl = baselines.get(c["channel_id"])
        if bl and bl.get("median_recent_vph"):
            c["_breakout"] = c["_vph"] / max(bl["median_recent_vph"], vr.get("min_baseline_vph", 1))
        else:
            c["_breakout"] = None
        vph_list.append(c["_vph"])
        vpd_list.append(c["_vpd"])
        abs_list.append(math.log10(max(c["views"], 1)))
        br_list.append(c["_breakout"] if c["_breakout"] is not None else 1.0)

    use_pct = n >= vr["min_pool_for_percentile"]
    vel_pct = _pct_rank(vph_list) if use_pct else [_log_scale(v, 10, 20000) for v in vph_list]
    abs_pct = _pct_rank(abs_list) if use_pct else [_log_scale(10 ** a, 5000, 2_000_000) for a in abs_list]
    br_pct = _pct_rank([math.log10(max(b, 0.01)) for b in br_list]) if use_pct \
        else [_log_scale(b, 0.5, vr["breakout_extreme"]) for b in br_list]

    for i, c in enumerate(cands):
        views = max(c["views"], 1)
        like_rate = (c.get("likes") or 0) / views
        cmt_rate = (c.get("comments") or 0) / views
        eng = 50 * min(like_rate / vr["engagement_cap_like_rate"], 1) + \
            50 * min(cmt_rate / vr["engagement_cap_comment_rate"], 1)
        fresh, bucket = freshness(c["age_days"], vr)
        br = c["_breakout"]
        if br is None:
            br_score = 50.0
            c.setdefault("flags", []).append("BASELINE_MISSING")
        else:
            # breakout ≥ good mới bắt đầu có điểm cao — kết hợp percentile pool với ngưỡng tuyệt đối
            br_score = max(br_pct[i], _log_scale(br, 1.0, vr["breakout_extreme"]) if br >= vr["breakout_good"] else 0)
        vs = (w["velocity"] * vel_pct[i] + w["breakout"] * br_score + w["absolute"] * abs_pct[i]
              + w["engagement"] * eng + w["freshness"] * fresh)
        market = vel_pct[i] >= vr["market_trend_velocity_pct"] and abs_pct[i] >= vr["market_trend_absolute_pct"]
        chan = br is not None and br >= vr["breakout_good"]
        vtype = "BOTH" if (market and chan) else "MARKET_TREND" if market else \
            "CHANNEL_BREAKOUT" if chan else "NORMAL"
        c["viral"] = {
            "vph": round(c["_vph"], 2), "vpd": round(c["_vpd"], 1),
            "breakout_ratio": round(br, 2) if br is not None else None,
            "velocity_score": round(vel_pct[i], 1), "breakout_score": round(br_score, 1),
            "absolute_view_score": round(abs_pct[i], 1), "engagement_score": round(eng, 1),
            "freshness_score": fresh, "freshness_bucket": bucket,
            "viral_score": round(vs, 1), "viral_type": vtype,
            "viral_pass": vs >= vr["min_score"],
        }
        for k in ("_vph", "_vpd", "_breakout"):
            c.pop(k, None)
    return cands
