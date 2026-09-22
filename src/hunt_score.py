# -*- coding: utf-8 -*-
"""Chấm điểm VIDEO cho Video Hunt — ưu tiên view/ngày, thưởng thêm cho video mới.

Khác score.py (chấm KÊNH cho luồng chính): ở đây không có baseline kênh, mỗi video
đứng độc lập — đúng yêu cầu "gom mọi video của mọi kênh", không chỉ kênh đã biết.
"""
from __future__ import annotations

import difflib
import re

_KANA_CHARS = re.compile(r"[぀-ヿ]")  # hiragana + katakana — CHỈ tiếng Nhật mới có


def is_japanese_title(title: str) -> bool:
    """Search sort-theo-view kéo theo video viral toàn cầu khớp lỏng lẻo từ khoá tiếng
    Nhật khi window rộng — đã dính thật 2 lần: (1) video tiếng Anh, (2) video tiếng
    TRUNG (phồn thể) lọt qua vì bản đầu chỉ kiểm dải Hán tự chung 一-鿿 — tiếng Trung
    dùng chung dải Hán tự này với tiếng Nhật nên không phân biệt được. Chữ Hán tự một
    mình KHÔNG đủ; tiếng Nhật viết thường xen kẽ hiragana/katakana (trợ từ ngữ pháp),
    tiếng Trung hầu như không có — ép phải CÓ kana mới coi là tiếng Nhật thật."""
    return bool(_KANA_CHARS.search(title or ""))


_LIVE_MARKERS = ("🔴", "ライブカメラ", "生配信", "LIVE配信", "配信中", "リアルタイム配信")


def is_live_stream(title: str) -> bool:
    """YouTube search vẫn trả video/live-cam nếu tag trùng chữ — view của live là số
    người xem TRỰC TIẾP cộng dồn, không so được với video thường. Đã dính thật (lane A
    ra 1 video ライブカメラ sân bay lọt top vì view tăng ảo nhanh)."""
    t = title or ""
    return any(m in t for m in _LIVE_MARKERS)


def title_matches_pool(title: str, kws: list[str], min_len: int = 4,
                       min_matches: int = 2) -> bool:
    """YouTube search khớp cả mô tả/tag video, không chỉ tiêu đề — 1 video có thể lọt
    vào kết quả dù chủ đề THẬT không liên quan (đã dính thật liên tiếp: video scandal
    thần tượng, video ẩm thực, 1 MV nhạc khớp NHẦM đúng 1 từ "サイエンス" — user chỉ ra
    "cả YouTube mà không tìm được video tiếng Nhật nào nói về khoa học vũ trụ" khi thấy
    MV đó đứng #1). Đo thật trên 5 video MẪU CHUẨN của chính lane A: video thật luôn có
    ≥2 từ khớp (do khối hashtag cuối tiêu đề kiểu 【都市伝説 ミステリー 怖い話】 tự lộ ra ≥2
    từ trong pool), còn 2 video nhiễu chỉ khớp ĐÚNG 1 từ. Ép `min_matches=2` — 1 từ
    khớp không đủ bằng chứng chủ đề, phải ≥2 mới tin.

    (1 lớp lọc yếu hơn min_len=4 vẫn giữ — bản đầu ép ≥2 ký tự để lại lọt vì cột F có
    tag ngắn quá chung như 暴露="phanh phui"/奇跡="phép màu")."""
    checkable = {p for kw in kws for p in kw.split() if len(p) >= min_len}
    if not checkable:
        return True  # không có tag đủ cụ thể để đối chiếu — không có gì để bác bỏ
    hits = sum(1 for p in checkable if p in title)
    return hits >= min_matches


def age_days_of(row: dict) -> float:
    return max((row.get("age_hours") or 0.1) / 24, 0.5)


def score_rows(rows: list[dict], cfg: dict) -> list[dict]:
    """Gắn `age_days`, `vpd` (view/ngày), `score` (vpd × hệ số ưu tiên độ mới)."""
    fresh_days = cfg.get("fresh_bonus_days", 14)
    out = []
    for r in rows:
        r = dict(r)
        age = age_days_of(r)
        vpd = r["views"] / age
        fresh_mult = 1 + max(0, (fresh_days - age) / fresh_days)
        r["age_days"] = round(age, 1)
        r["vpd"] = round(vpd, 1)
        r["score"] = round(vpd * fresh_mult, 1)
        out.append(r)
    return out


def _is_dup_topic(title: str, done_titles: list[str], threshold: float = 0.6) -> bool:
    for d in done_titles:
        if difflib.SequenceMatcher(None, title, d).ratio() >= threshold:
            return True
    return False


def filter_rows(rows: list[dict], cfg: dict, already_picked: set[str],
                done_titles: list[str], kws: list[str]) -> list[dict]:
    """Áp toàn bộ tiêu chí sàng lọc + chống trùng, KHÔNG sắp xếp."""
    out = []
    for r in rows:
        if r["video_id"] in already_picked:
            continue
        if not is_japanese_title(r["title"]):
            continue
        if is_live_stream(r["title"]):
            continue
        if not title_matches_pool(r["title"], kws):
            continue
        if r["views"] < cfg["min_views"]:
            continue
        if r.get("age_days", age_days_of(r)) > cfg["max_age_days"]:
            continue
        if (r.get("duration_s") or 0) < cfg["min_duration_s"]:
            continue
        if _is_dup_topic(r["title"], done_titles):
            continue
        out.append(r)
    return out


def reason_text(r: dict, matched_tags: list[str]) -> str:
    subs = r.get("subs") or 0
    mult = f"{r['views'] / max(subs, 300):.0f}× sub" if subs else "sub không rõ"
    tags = "、".join(matched_tags[:3]) if matched_tags else "-"
    return (f"{r['vpd']:,.0f} view/ngày · {r['age_days']:.0f} ngày tuổi · "
            f"{r['views']:,} view tổng · kênh {subs:,} sub ({mult}) · tag khớp: {tags}")


def pick_top(rows: list[dict], n: int, distinct_channels: bool = True) -> list[dict]:
    """Top N theo score, mặc định ép mỗi kênh chỉ góp tối đa 1 video trong N chọn."""
    ranked = sorted(rows, key=lambda r: r["score"], reverse=True)
    if not distinct_channels:
        return ranked[:n]
    picked, seen_ch = [], set()
    for r in ranked:
        if r["channel_id"] in seen_ch:
            continue
        picked.append(r)
        seen_ch.add(r["channel_id"])
        if len(picked) >= n:
            break
    return picked
