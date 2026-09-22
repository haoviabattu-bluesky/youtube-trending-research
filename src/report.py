# -*- coding: utf-8 -*-
"""Chuyển dòng đã chấm điểm thành ma trận giá trị đúng thứ tự cột của từng tab Sheet.

Tách khỏi sheets.py để phần "ghi lên Sheet" không dính logic trình bày,
và để test được các hàm này mà không cần mạng.
"""
from __future__ import annotations

from score import LABEL_ICON

YT = "https://www.youtube.com"


def _thumb(video_id: str) -> str:
    return f'=IMAGE("https://i.ytimg.com/vi/{video_id}/mqdefault.jpg")'


def build_daily_rows(top: list[dict], snap: str) -> list[list]:
    out = []
    for rank, r in enumerate(top, 1):
        out.append([
            snap, rank, f"{LABEL_ICON.get(r['label'], '')} {r['label']}", r["score"],
            _thumb(r["video_id"]), r["title"], r["channel"],
            (r.get("niches") or "").split("|")[0],
            r["views"], r.get("views_24h"), r.get("vph"), r.get("subs"),
            r.get("mult"), r.get("breakout"), r.get("ch_median_views"), r.get("ch_mult"),
            r.get("ch_age_days"), round(r.get("age_hours") or 0),
            round((r.get("duration_s") or 0) / 60, 1), r.get("engagement"),
            (r.get("keywords") or "").split("|")[0],
            f"https://youtu.be/{r['video_id']}", f"{YT}/channel/{r['channel_id']}",
        ])
    return out


def build_new_rows(rows: list[dict], cfg: dict, snap: str) -> list[list]:
    """Kênh MỚI có hit — bảng riêng vì đây là thứ đáng nghiên cứu nhất."""
    best: dict[str, dict] = {}
    for r in rows:
        age = r.get("ch_age_days")
        if age is None or age > cfg["new_channel_days"]:
            continue
        if (r.get("subs") or 0) < cfg["min_subs"]:
            continue
        if r["views"] < cfg["new_channel_min_views"]:
            continue
        cur = best.get(r["channel_id"])
        if cur is None or r["views"] > cur["views"]:
            best[r["channel_id"]] = r
    seen_count: dict[str, int] = {}
    for r in rows:
        seen_count[r["channel_id"]] = seen_count.get(r["channel_id"], 0) + 1
    # Sắp theo ch_mult chứ KHÔNG theo best_views: kênh spam đăng mỗi ngày ăn may 1 video
    # 500k sẽ luôn đứng đầu nếu xếp theo view, trong khi kênh đáng học là kênh ĐỀU ĐẶN.
    return [[snap, r["channel"], r.get("ch_age_days"), r.get("subs"), r.get("ch_mult"),
             r.get("ch_median_views"), r["views"], r["title"],
             seen_count.get(r["channel_id"], 1), (r.get("niches") or "").split("|")[0],
             f"{YT}/channel/{r['channel_id']}", consistency_verdict(r)]
            for r in sorted(best.values(),
                            key=lambda x: (x.get("ch_mult") or 0, x["views"]),
                            reverse=True)[: cfg.get("new_rows_limit", 15)]]


def consistency_verdict(r: dict) -> str:
    """Phân biệt kênh CÓ CÔNG THỨC với kênh ăn may — khác biệt quan trọng nhất khi chọn
    ngách để nhân bản. Đo thật 2026-09-09: シニア健康日和 có video 500k view nhưng 12 video
    gần nhất chỉ 57–521 view (ch_mult 0,14) — không đáng học. Còn 他人の人生【タニジン】
    median 100.863 (ch_mult 18,8) — đó mới là cỗ máy."""
    cm = r.get("ch_mult")
    if cm is None:
        return "❔ chưa có baseline"
    if cm >= 3:
        return f"🔁 ĐỀU ĐẶN — video điển hình = {cm:.1f}× số sub"
    if cm >= 1:
        return f"➖ khá đều ({cm:.1f}×)"
    return f"⚡ ĂN MAY 1 VIDEO — video điển hình chỉ {cm:.2f}× số sub"


def build_channel_rows(rows: list[dict], baselines: dict, snap: str,
                       first_seen: dict[str, str] | None = None) -> list[list]:
    """Sổ đăng ký kênh tích luỹ — upsert theo channel_id, không bao giờ xoá dòng cũ.

    `first_seen` lấy từ DB chứ KHÔNG dùng snap hôm nay, nếu không mỗi ngày upsert
    sẽ ghi đè ngày phát hiện gốc và mất luôn thông tin kênh này có từ bao giờ.
    """
    first_seen = first_seen or {}
    agg: dict[str, dict] = {}
    for r in rows:
        cid = r["channel_id"]
        a = agg.setdefault(cid, {"row": r, "n": 0, "best": 0})
        a["n"] += 1
        if r["views"] > a["best"]:
            a["best"] = r["views"]
            a["row"] = r
    out = []
    for cid, a in agg.items():
        r, b = a["row"], baselines.get(cid, {})
        age = r.get("ch_age_days")
        vc = r.get("ch_video_count") or 0
        upw = round(vc / max((age or 0) / 7, 1), 2) if age else None
        out.append([cid, r["channel"], (r.get("niches") or "").split("|")[0], age,
                    r.get("subs"), r.get("subs_7d"), b.get("median_views"),
                    r.get("ch_mult"), b.get("hit_rate"), a["n"], a["best"], upw,
                    first_seen.get(cid, snap), snap, f"{YT}/channel/{cid}"])
    return out
