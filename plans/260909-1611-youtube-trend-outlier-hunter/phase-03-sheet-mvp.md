---
phase: 3
title: "MVP + SHEET — 6 tab báo cáo, Sheet làm luôn bảng điều khiển (SHIP CHECKPOINT)"
status: completed
priority: P1
effort: "1d"
dependencies: [2]
completed: 2026-09-09
smoke_test: "PASS — ghi thật lên Sheet 1xu4iNud…: GMAIL 101→101, NOTE 1→1 (KHÔNG đổi 1 dòng nào). Tạo TRD_CONFIG 126 dòng (bootstrap 125 keyword), TRD_CHANNELS, TRD_NEW, TRD_KEYWORDS. Chạy LẠI cùng ngày: TRENDING giữ nguyên 41 dòng thay vì nhân đôi thành 81 → write_daily_block ghi đè tại chỗ hoạt động."
---

# Phase 3 — MVP + SHEET (ship checkpoint)

## Overview

Đẩy báo cáo lên Google Sheet và đọc ngược config từ chính Sheet đó, để đổi keyword/ngưỡng không cần đụng code. Sau phase này tool đã dùng được thật.

## Related Code Files

**Create** — `src/sheets.py` (lớp ghi, có guard), `src/report.py` (trình bày, tách khỏi lớp ghi để test offline)

## Cấu trúc tab

| Tab | Vai trò | Cách ghi |
|---|---|---|
| `TRENDING` | Báo cáo ngày: nhãn, score, thumbnail, mọi chỉ số, link | 1 khối/ngày, chạy lại thì ghi đè tại chỗ |
| `TRD_NEW` | Kênh mới có hit — bảng riêng vì đây là thứ đáng nghiên cứu nhất | 1 khối/ngày |
| `TRD_CHANNELS` | Sổ đăng ký kênh tích luỹ | upsert theo `channel_id` |
| `TRD_KEYWORDS` | Momentum + content gap | 1 khối/ngày |
| `TRD_DEEPDIVE` | Hook, title pattern, comment, insight LLM | 1 khối/ngày |
| `TRD_CONFIG` | **User sửa keyword/ngách ở đây** | bootstrap 1 lần, sau đó chỉ đọc |

## An toàn dữ liệu — điểm quan trọng nhất của phase

Sheet đích đang chứa dữ liệu thật của user ở tab `GMAIL` và `NOTE`.

1. `_assert_allowed(tab)` — chặn cứng, chỉ cho `TRENDING` + prefix `TRD_`. Mọi hàm ghi đều đi qua.
2. `sheets.py` **không import và không gọi** bất kỳ API xoá nào của gspread (`delete_rows`, `delete_columns`, `clear`, `batch_clear`, `delete_worksheet`).
3. `ensure_tab()` so header **exact-match**; header lệch thì **ném lỗi** chứ không ghi đè.
4. `guard_snapshot()` đếm số dòng MỌI tab trước và sau mỗi lượt chạy; `GMAIL`/`NOTE` đổi số dòng ⇒ orchestrator thoát với mã lỗi 3.

## Quyết định thiết kế phát sinh

**Chạy lại trong cùng ngày làm nhân đôi báo cáo.** Cách sửa thông thường là xoá khối cũ rồi ghi lại — nhưng quy tắc cấm xoá. → `write_daily_block()`: tìm các dòng có `snap_date` = hôm nay, **update tại chỗ**, phần dư mới thì append. Nếu lượt sau ít dòng hơn lượt trước, dòng cũ dư được **giữ nguyên** và hàm trả về số dòng dư để cảnh báo — không im lặng.

**`first_seen` của kênh lấy từ SQLite, không lấy `snap` hôm nay.** Nếu không, mỗi lần upsert `TRD_CHANNELS` sẽ ghi đè ngày phát hiện gốc và mất luôn thông tin "kênh này mình theo dõi từ bao giờ".

**Lượt chạy nhỏ đè mất báo cáo đầy đủ.** Đã dính thật: sau khi ghi xong 150 dòng của ngày, một lượt test 3 keyword ghi đè tại chỗ và **xoá mất top 28 dòng**. Sửa bằng `ShrinkGuard` — nếu lượt mới có ít hơn 70% số dòng của khối cùng ngày đã ghi thì **từ chối ghi** kèm thông báo rõ, phải `--force` mới đè. Đây là loại lỗi im lặng nguy hiểm nhất: chương trình báo thành công trong khi dữ liệu đã mất.

**Chặn 1 kênh chiếm hết bảng.** Kênh nào có 10 video lọt top sẽ ngập báo cáo → `max_rows_per_channel: 2`.

## Acceptance Criteria

- [x] `GMAIL` và `NOTE` không đổi 1 dòng nào (verify bằng `guard_snapshot` trước/sau)
- [x] Chạy lại cùng ngày không nhân đôi dòng
- [x] Sửa keyword trong `TRD_CONFIG` → lượt sau tool dùng keyword mới
- [x] Header lệch → từ chối ghi thay vì ghi đè
- [x] Thumbnail hiện được trong ô (`=IMAGE(...)`, `USER_ENTERED`)
- [x] Lượt chạy nhỏ KHÔNG đè được báo cáo đầy đủ cùng ngày (verify: 28 dòng bị chặn trước 150 dòng)
- [x] Thêm cột mới vào header của tab đã có dữ liệu → tự nâng cấp header, không mất dữ liệu cũ
