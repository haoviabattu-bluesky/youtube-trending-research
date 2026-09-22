---
phase: 5
title: "KEYWORD MOMENTUM + CONTENT GAP — thay Google Trends đã bị chặn"
status: completed
priority: P2
effort: "0.5d"
dependencies: [3]
completed: 2026-09-09
smoke_test: "PASS — sinh thống kê cho toàn bộ keyword đang bật, mỗi keyword có n_new_7d / median_views_7d / p90_views_7d / n_new_channels / content_gap / verdict. demand_delta_pct trống ở lượt đầu (chưa có snapshot 7 ngày trước) — đúng thiết kế, sẽ có giá trị từ ngày thứ 8."
---

# Phase 5 — Keyword momentum & content gap

## Overview

pytrends trả `429` ngay request đầu (verify 2026-09-09) nên Google Trends bị loại khỏi đường chính. Thay bằng thứ **tốt hơn**: tự tính momentum từ chính dữ liệu đã quét — đo được **cả cung lẫn cầu** ngay trên YouTube, điều Google Trends không làm được.

## Related Code Files

**Create** — `src/keywords.py`

## Chỉ số

| Chỉ số | Nghĩa | Vai trò |
|---|---|---|
| `n_new_7d` | Số video mới đăng trong 7 ngày khớp keyword | **CUNG** |
| `median_views_7d` / `p90_views_7d` | View điển hình / view top của lứa video mới đó | **CẦU** |
| `n_new_channels` | Số kênh <180 ngày tuổi mới xuất hiện ở keyword này | Có ai đang nhảy vào không |
| `demand_delta_pct` | `median_views_7d` so với snapshot 7 ngày trước | Keyword **đang tăng** hay đang nguội |
| `content_gap` | `z(cầu) − z(cung)` trong cùng ngách | **Cầu cao, cung thấp = ngách trống** |

`verdict` tự động: 🎯 CONTENT GAP · 📈 ĐANG TĂNG MẠNH · 🌱 NHIỀU KÊNH MỚI NHẢY VÀO · 🥵 BÃO HOÀ.

## Vì sao hơn Google Trends

Google Trends chỉ cho biết *người ta tìm nhiều hay ít* (một vế). Ở đây đo được **đối chiếu cung–cầu**: một keyword có 40 video mới/tuần với median 3.000 view là **bão hoà**, còn 4 video mới với median 80.000 view là **ngách trống** — Google Trends có thể hiển thị cả hai như nhau.

## Bug đã bắt được (2026-09-09)

**1 keyword bị xé thành 2 dòng số liệu khác nhau, rồi đè nhau trong DB.**
`ゆっくり解説 2ch` ra 2 dòng: một dòng `gap 6,9 / 3 video`, một dòng `gap 3,88 / 20 video`.
Nguyên nhân: gom theo `(niches.split("|")[0], keyword)` — video khớp keyword của cả 2 ngách
có `niches = "jp_senior|jp_satori"` nên rơi vào bucket ngách khác với ngách của chính keyword.
Hậu quả nặng hơn ở tầng lưu: khoá `keyword_snapshot` là `(keyword, snap_date)` nên **dòng sau
ĐÈ dòng trước, mất dữ liệu im lặng** và `content_gap` tính trên mẫu thiếu.

→ Sửa: gom theo **keyword**, ngách lấy từ map `kw_niche` của config. Sau khi sửa: 112 keyword,
**0 trùng lặp**; `ゆっくり解説 2ch` gộp lại đúng thành `gap 4,72 / 23 video / median 22.099`.

## Giới hạn đã biết

- `demand_delta_pct` chỉ có giá trị từ **ngày thứ 8** trở đi (cần snapshot 7 ngày trước để so). Lượt đầu để trống, không phải lỗi.
- `content_gap` là z-score **trong cùng ngách** — không so chéo giữa `jp_senior` và `jp_satori`.
- Chỉ đếm video mà tool **nhìn thấy** qua search, không phải toàn bộ YouTube. Đây là mẫu chứ không phải tổng thể; dùng để so keyword với nhau chứ đừng đọc như con số tuyệt đối.

## Acceptance Criteria

- [x] Mỗi keyword đang bật có đủ 6 chỉ số
- [x] `content_gap` chuẩn hoá trong cùng ngách
- [x] `demand_delta_pct` trống khi chưa đủ lịch sử, không nổ
- [x] Ghi vào `keyword_snapshot` khoá `(keyword, snap_date)` → chạy lại là idempotent
- [x] Mỗi keyword đúng **1 dòng** (verify: 112 keyword, 0 trùng lặp)
