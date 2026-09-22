---
phase: 4
title: "DEEPDIVE — transcript + comment top N → hook, title pattern, insight"
status: completed
priority: P2
effort: "1d"
dependencies: [3]
completed: 2026-09-09
smoke_test: "PASS — 5/5 video top lấy được transcript + comment, 0 lỗi. Ví dụ thật: hook 268 ký tự, transcript 7.785 ký tự, 356 ký tự/phút; title pattern trong ngày = 5つ×12, 5選×10, 1位×5, 【ゆっくり解説】×5; 12 comment top kèm số like; insight LLM (ramclouds gemini-3.5-flash-low) trả 4 mục tiếng Việt dùng được ngay."
---

# Phase 4 — DEEPDIVE

## Overview

Biến "video này đang bùng" thành "vì sao nó bùng và tôi nhân bản thế nào". Hai tầng tách bạch để tầng dưới không kéo tầng trên chết theo.

## Related Code Files

**Create** — `src/deepdive.py`

## Kiến trúc 2 tầng

**Tầng 1 — dữ kiện thô, không phụ thuộc dịch vụ ngoài** (luôn chạy):
- `hook` — 45 giây đầu của transcript, đây là thứ quyết định giữ chân người xem
- `wpm` — mật độ chữ/phút, đo nhịp kể
- `title_pattern` — thống kê khối `【】` và con số (`5つ`, `3選`, `1位`) trên **toàn bộ title top trong ngày**, không chỉ 1 video → thấy được công thức đặt title đang chạy trong ngách
- `top_comments` — 12 comment gốc nhiều like nhất

**Tầng 2 — LLM tóm tắt** (tuỳ chọn): đưa dữ kiện tầng 1 cho `gemini-3.5-flash-low` qua ramclouds → 4 mục: HOOK / CẤU TRÚC / INSIGHT KHÁN GIẢ / 3 ý tưởng title mới.

Không có key hoặc lỗi mạng → trả chuỗi rỗng, **pipeline vẫn chạy bình thường**. Tầng 1 đứng một mình đã đủ dùng.

## Bẫy đã xử lý

| Bẫy | Xử lý |
|---|---|
| `youtube-comment-downloader` trả `votes` là **CHUỖI viết tắt theo locale** (`"311 N"` = 311 nghìn) | `parse_votes()` tự quy đổi N/Tr/K/M/万/億; `int()` thẳng sẽ nổ |
| Video tắt comment / không phụ đề | Bắt exception, ghi vào `errors[]`, không retry, không làm hỏng lượt chạy |
| Reply lẫn vào comment gốc | Lọc `is_reply` trước khi xếp theo like |
| Transcript quá dài làm prompt phình | Cắt 12.000 ký tự khi lưu, 6.000 khi gửi LLM |

## Acceptance Criteria

- [x] 5 video top → 5 payload có hook + comment, lỗi lẻ tẻ không làm hỏng lượt chạy
- [x] `title_pattern` gom được công thức title của cả ngày, không chỉ 1 video
- [x] `votes` parse đúng từ chuỗi viết tắt
- [x] Không có LLM key vẫn chạy đủ tầng 1
