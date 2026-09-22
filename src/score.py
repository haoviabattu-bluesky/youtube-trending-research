# -*- coding: utf-8 -*-
"""Chấm điểm outlier.

Nguyên tắc rút ra từ probe 2026-09-09: `views/subs` một mình tạo rác nặng
(kênh 7 subs → 2618×). Chỉ số CHÍNH là `breakout` = views / median của chính kênh đó,
vì nó tự chuẩn hoá theo quy mô kênh. `mult` chỉ là phụ, và luôn có sàn `min_subs`.
"""
from __future__ import annotations

import datetime as dt
import math
import statistics

LABEL_ORDER = ["PROVEN_NICHE", "NEW_CHANNEL_HIT", "BREAKOUT", "RISING", "WATCH", "NOISE"]
LABEL_ICON = {"PROVEN_NICHE": "🔁", "NEW_CHANNEL_HIT": "🌱", "BREAKOUT": "🚀",
              "RISING": "📈", "WATCH": "👀", "NOISE": "⚠️"}


def _z(values: list[float]) -> list[float]:
    if len(values) < 2:
        return [0.0] * len(values)
    mu = statistics.mean(values)
    sd = statistics.pstdev(values) or 1.0
    return [(v - mu) / sd for v in values]


def compute_metrics(row: dict, prev: tuple[int, str] | None, baseline: dict | None,
                    cfg: dict, snap_today: str) -> dict:
    """Gắn thêm các chỉ số outlier vào 1 dòng. Không quyết định nhãn ở đây."""
    views = row["views"] or 0
    age_h = max(row.get("age_hours") or 0, 1.0)
    subs_floor = max(row.get("subs") or 0, cfg["min_subs"])

    m = {
        "vph": round(views / age_h, 1),
        "mult": round(views / subs_floor, 2),
        "engagement": round(((row.get("likes") or 0) + (row.get("comments") or 0))
                            / max(views, 1), 5),
        "views_24h": None,
        "vph_24h": None,
        "breakout": None,
        "ch_hit_rate": None,
        "ch_median_views": None,
        "ch_mult": None,
        "ch_n_videos": None,
    }

    if prev:
        prev_views, prev_date = prev
        # Snapshot trước KHÔNG chắc là hôm qua (tool có thể nghỉ vài ngày) → chia cho số
        # ngày thật, nếu không "views_24h" sẽ thổi phồng gấp mấy lần và nhãn RISING loạn.
        gap = max((dt.date.fromisoformat(snap_today) - dt.date.fromisoformat(prev_date)).days, 1)
        m["views_24h"] = round((views - prev_views) / gap)
        m["delta_gap_days"] = gap
        m["delta_share"] = round(m["views_24h"] / max(views, 1), 4)

    if baseline and baseline.get("median_views"):
        med = baseline["median_views"]
        m["ch_median_views"] = med
        m["breakout"] = round(views / max(med, 1), 2)
        m["ch_hit_rate"] = baseline.get("hit_rate")
        m["ch_n_videos"] = baseline.get("n_videos")
        # ĐỘ ỔN ĐỊNH: kênh ĐỀU ĐẶN kéo view vượt xa quy mô của mình.
        # Khác hẳn hit_rate (đo độ giật cục) — kênh mọi video đều 100k có hit_rate ~0.
        m["ch_mult"] = round(med / subs_floor, 2)
    return m


def label_row(row: dict, cfg: dict, rising: bool = False) -> str:
    subs = row.get("subs") or 0
    age_d = row.get("ch_age_days")
    views = row.get("views") or 0
    breakout = row.get("breakout")

    # --- loại nhiễu trước, đây là thứ probe cho thấy chiếm phần lớn top nếu không lọc ---
    if row.get("duration_s", 0) < cfg["min_duration_s"]:
        return "NOISE"
    if subs and subs < cfg["min_subs"]:
        return "NOISE"
    if age_d is not None and age_d > cfg["max_ch_age_days"]:
        return "NOISE"
    if views >= 10_000 and row.get("engagement", 0) < 0.0002:
        return "NOISE"          # view cao mà gần như không ai like/comment = quảng cáo/bơm

    # 🔁 Kênh có CÔNG THỨC chạy được: đều đặn kéo view vượt xa quy mô, đủ số video để
    #    loại trừ may mắn. Đây là nhãn đáng tiền nhất — "ngách đáng test", không phải
    #    "video may mắn". Dùng ch_mult (median/subs) chứ KHÔNG dùng hit_rate.
    if (row.get("ch_mult") is not None
            and row["ch_mult"] >= cfg.get("proven_ch_mult", 5.0)
            and (row.get("ch_n_videos") or 0) >= cfg.get("proven_min_videos", 5)
            and (row.get("ch_median_views") or 0) >= cfg.get("proven_min_median", 20_000)):
        return "PROVEN_NICHE"
    if (age_d is not None and age_d <= cfg["new_channel_days"]
            and views >= cfg["new_channel_min_views"] and subs >= cfg["min_subs"]):
        return "NEW_CHANNEL_HIT"
    if (breakout is not None and breakout >= cfg["breakout_ratio"]
            and (row.get("age_hours") or 9e9) <= 24 * 14 and views >= 30_000):
        return "BREAKOUT"
    # RISING phải là ĐANG LEO thật: vẫn ăn view mạnh so với tổng view của chính nó.
    # Ngưỡng "views_24h > 0" là vô nghĩa — gần như mọi video đều thoả.
    if (rising and (row.get("views_24h") or 0) >= cfg.get("rising_min_views_24h", 2000)
            and (row.get("delta_share") or 0) >= cfg.get("rising_min_share", 0.08)):
        return "RISING"
    return "WATCH"


def score_within_niche(rows: list[dict], cfg: dict) -> None:
    """Gắn `score` 0–100, chuẩn hoá z-score TRONG cùng ngách (không so chéo ngách)."""
    by_niche: dict[str, list[dict]] = {}
    for r in rows:
        by_niche.setdefault((r.get("niches") or r.get("niche", "")).split("|")[0], []).append(r)

    for group in by_niche.values():
        lg = lambda v: math.log10(max(v or 0, 1))  # noqa: E731
        zb = _z([lg(r.get("breakout") or 1) for r in group])
        zv = _z([lg(r.get("vph")) for r in group])
        zm = _z([lg(min(r.get("mult") or 0, 500)) for r in group])
        zd = _z([lg(max(r.get("views_24h") or 0, 0)) for r in group])
        ze = _z([r.get("engagement") or 0 for r in group])
        # ch_mult = kênh ĐỀU ĐẶN vượt quy mô. Không có nó, kênh spam đăng mỗi ngày
        # ăn may 1 video sẽ luôn đứng đầu bảng nhờ breakout khổng lồ (500k/306 = 1634x).
        zc = _z([lg(min(r.get("ch_mult") or 0, 100)) for r in group])
        for i, r in enumerate(group):
            age_d = r.get("ch_age_days")
            new_bonus = 0.0
            if age_d is not None:
                if age_d <= 60:
                    new_bonus = 2.0
                elif age_d <= cfg["new_channel_days"]:
                    new_bonus = 1.2
                elif age_d <= 365:
                    new_bonus = 0.5
            raw = (0.22 * zb[i] + 0.18 * zv[i] + 0.13 * zm[i] + 0.12 * zd[i]
                   + 0.08 * ze[i] + 0.17 * zc[i] + 0.10 * new_bonus)
            r["score"] = round(max(0.0, min(100.0, 50 + 16 * raw)), 1)


def channel_baseline_from_videos(videos: list[dict], cfg: dict) -> dict:
    """Baseline của 1 kênh: median, p90, tỉ lệ bứt phá, VÀ xu hướng đang lên hay đang tụt.

    `trend` là chốt chặn KHÔNG THỂ THIẾU — đã dính thật 2026-09-09: kênh 極秘接触 chấm
    `ch_mult` 37,9 (hạng nhất ngách vũ trụ) nhưng 4 video mới nhất chỉ 177–930 view.
    Baseline chỉ nhìn video >=7 ngày nên KHÔNG THẤY kênh vừa bắt đầu tụt — suýt chọn
    nhầm một kênh đang chết làm hình mẫu để nhân bản.
    """
    vids = [v for v in videos if v.get("views") is not None]
    if not vids:
        return {"median_views": 0, "p90_views": 0, "n_videos": 0, "hit_rate": 0.0,
                "trend": None}
    vals = sorted(v["views"] for v in vids)
    med = int(statistics.median(vals))
    p90 = vals[min(len(vals) - 1, int(0.9 * len(vals)))]
    hits = sum(1 for v in vals if med and v >= cfg["breakout_ratio"] * med)

    trend = None
    dated = [v for v in vids if v.get("published_at")]
    if len(dated) >= 6:
        dated.sort(key=lambda v: v["published_at"], reverse=True)
        half = max(3, len(dated) // 2)
        recent = statistics.median([v["views"] for v in dated[:half]])
        older = statistics.median([v["views"] for v in dated[half:]])
        trend = round(recent / older, 2) if older else None

    return {"median_views": med, "p90_views": int(p90), "n_videos": len(vals),
            "hit_rate": round(hits / len(vals), 3), "trend": trend}
