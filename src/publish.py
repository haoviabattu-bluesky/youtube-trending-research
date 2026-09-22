# -*- coding: utf-8 -*-
"""Đẩy kết quả lên Google Sheet + kiểm tra toàn vẹn dữ liệu trước/sau.

Tách khỏi `run_daily.py` để phần điều phối không lẫn với phần ghi, và để chỗ duy nhất
đụng tới Sheet nằm gọn trong 2 file (`sheets.py` ghi, file này quyết định ghi cái gì).
"""
from __future__ import annotations

from report import build_channel_rows, build_daily_rows, build_new_rows
from sheet_schema import ShrinkGuard

HOT_LABELS = ("PROVEN_NICHE", "NEW_CHANNEL_HIT", "BREAKOUT", "RISING")


def _safe_block(rep, tab, rows, snap, force, log, expect=None) -> tuple[int, int]:
    try:
        added, stale = rep.write_daily_block(tab, rows, snap, force, expect)
        log(f"[sheet] {tab}: {len(rows) - added} dòng cập nhật tại chỗ, {added} thêm mới"
            + (f", {stale} dòng cũ được đánh dấu ⏹cũ" if stale else ""))
        return added, stale
    except ShrinkGuard as e:
        log(f"[sheet] BỎ QUA — {e}")
        return 0, 0


def push(rep, con, store, top, keep, kw_rows, deep, baselines, snap, cfg,
         force: bool, log) -> None:
    n1, stale1 = _safe_block(rep, "TRENDING", build_daily_rows(top, snap), snap,
                             force, log, cfg["daily_report_rows"])

    # Sổ đăng ký kênh chỉ nhận kênh ĐÁNG THEO DÕI. Ghi mọi kênh quét được thì tab phình
    # ~800 dòng/ngày toàn mức WATCH, và không xoá bớt được.
    hot = {r["channel_id"] for r in keep if r["label"] in HOT_LABELS}
    watched = [r for r in keep if r["channel_id"] in hot]
    u2, a2 = rep.upsert_by_key("TRD_CHANNELS", build_channel_rows(
        watched, baselines, snap, store.channel_first_seen(con)))
    log(f"[channels] {len(hot)} kênh đáng theo dõi / "
        f"{len({r['channel_id'] for r in keep})} kênh quét được")

    n3, stale3 = _safe_block(rep, "TRD_NEW", build_new_rows(keep, cfg, snap), snap,
                             force, log, cfg.get("new_rows_limit", 15))
    n4, _ = _safe_block(rep, "TRD_KEYWORDS", [
        [snap, r["niche"], r["keyword"], r["n_new_7d"], r["median_views_7d"],
         r["p90_views_7d"], r["n_new_channels"], r["demand_delta_pct"],
         r["content_gap"], r["verdict"]] for r in kw_rows], snap, force, log)
    n5, _ = _safe_block(rep, "TRD_DEEPDIVE", [
        [snap, r["label"], r["title"], r["channel"], r["views"],
         f"https://youtu.be/{r['video_id']}", deep[r["video_id"]]["hook"][:900],
         deep[r["video_id"]]["title_pattern"][:900],
         deep[r["video_id"]]["top_comments"][:2000],
         deep[r["video_id"]].get("insight", "")[:3000]]
        for r in top if r["video_id"] in deep], snap, force, log)

    log(f"[sheet] TRD_CHANNELS: {u2} cập nhật, {a2} thêm mới")
    _ = (n1, n3, n4, n5)
    _ = (stale1, stale3)


def verify_untouched(rep, before: dict, log, tabs=("GMAIL", "NOTE")) -> bool:
    """Chứng minh không tab nào của user bị đụng. False ⇒ caller phải thoát với mã lỗi."""
    after = rep.guard_snapshot()
    log(f"[guard] số dòng sau khi ghi: {after}")
    ok = True
    for tab in tabs:
        if tab in before and before[tab] != after.get(tab):
            log(f"!! CẢNH BÁO: tab {tab} đổi {before[tab]} → {after.get(tab)}")
            ok = False
    return ok
