# -*- coding: utf-8 -*-
"""Cột của từng tab + hàng rào an toàn.

Tách riêng để chỗ định nghĩa "được ghi vào đâu, cột nào" nằm một nơi dễ soi,
không lẫn với code gọi API.
"""
from __future__ import annotations

MAIN_TAB = "TRENDING"
TAB_PREFIX = "TRD_"
PROTECTED_HINT = "tab ngoài whitelist — có thể chứa dữ liệu khác của user"

HEADERS = {
    MAIN_TAB: ["snap_date", "rank", "label", "score", "thumb", "title", "channel",
               "niche", "views", "views_24h", "vph", "subs", "mult", "breakout",
               "ch_median", "ch_mult", "ch_age_d", "video_age_h", "dur_min",
               "engagement", "keyword", "video_url", "channel_url"],
    "TRD_NEW": ["first_seen", "channel", "ch_age_d", "subs", "ch_mult", "ch_median",
                "best_views", "best_title", "n_videos_seen", "niche", "channel_url",
                "verdict"],
    "TRD_CHANNELS": ["channel_id", "channel", "niche", "ch_age_d", "subs", "subs_7d",
                     "ch_median", "ch_mult", "hit_rate", "n_videos_seen", "best_views",
                     "uploads_per_week", "first_seen", "last_seen", "channel_url"],
    "TRD_KEYWORDS": ["snap_date", "niche", "keyword", "n_new_7d", "median_views_7d",
                     "p90_views_7d", "n_new_channels", "demand_delta_pct",
                     "content_gap", "verdict"],
    "TRD_DEEPDIVE": ["snap_date", "label", "title", "channel", "views", "video_url",
                     "hook_text", "title_pattern", "top_comments", "insight"],
    "TRD_CONFIG": ["niche", "enabled", "keyword", "hl", "gl", "note"],
    # RANK = 1..pick_per_lane — MỖI VIDEO 1 DÒNG (user chốt 2026-09-22), không nhét
    # nhiều video vào 1 ô bằng xuống dòng như bản đầu.
    "RESEARCH": ["DATE", "RANK", "shinya_shiryoshitsu", "Lopezzapa68", "irogatatarukioku",
                 "70dai-kenko", "teinengo-real", "teinengo-tanoshimi",
                 "kokoro-kazokugaku", "sengoku-uragawa", "teinengo-fuufu"],
    # VIDEO HUNT V2 (2026-09-22) — audit trail đầy đủ (guide §19): OLD pick + top V2 mỗi lane/ngày.
    # HUMAN_DECISION (ACCEPT/REJECT/SKIP) + REJECT_REASON là cột USER GÕ TAY — tool chỉ đọc.
    "TRD_HUNT_AUDIT": ["DATE", "LANE", "RANK", "VIDEO_URL", "TITLE", "CHANNEL", "PUBLISHED_AT",
                       "AGE_DAYS", "VIEWS", "VPD", "VPH", "BREAKOUT_RATIO", "VIRAL_TYPE",
                       "VIRAL_SCORE", "TOPIC_MATCH", "FORMAT_CLASS", "OPPORTUNITY_SCORE",
                       "FINAL_QC", "WHY_VIRAL", "WHY_USEFUL", "CONFIDENCE", "HUMAN_DECISION",
                       "REJECT_REASON", "OLD_SELECTED", "V2_SELECTED", "RUN_MODE", "RUN_ID",
                       "FLAGS", "VIDEO_ID"],
}
# Tab riêng, KHÔNG có prefix TRD_ — chốt bởi user 2026-09-21, khai cứng ở _EXTRA_ALLOWED
# vì _assert_allowed() chỉ cho phép MAIN_TAB hoặc prefix TRD_.
_EXTRA_ALLOWED = {"RESEARCH"}


class SheetGuardError(RuntimeError):
    """Chặn thao tác lên tab không thuộc whitelist."""


class ShrinkGuard(RuntimeError):
    """Lượt chạy này ít dòng hơn hẳn khối cùng ngày đã ghi — từ chối để khỏi mất báo cáo."""

    def __init__(self, new_n: int, old_n: int, tab: str):
        self.new_n, self.old_n, self.tab = new_n, old_n, tab
        super().__init__(
            f"'{tab}': lượt này chỉ có {new_n} dòng trong khi khối hôm nay đã có {old_n}. "
            f"Từ chối ghi để không mất báo cáo đầy đủ — thêm --force nếu thật sự muốn đè.")


def _assert_allowed(tab: str) -> None:
    if tab != MAIN_TAB and not tab.startswith(TAB_PREFIX) and tab not in _EXTRA_ALLOWED:
        raise SheetGuardError(f"TỪ CHỐI ghi vào '{tab}' — {PROTECTED_HINT}. "
                              f"Chỉ cho phép '{MAIN_TAB}', prefix '{TAB_PREFIX}', hoặc {_EXTRA_ALLOWED}.")


