---
phase: 2
title: "FOUNDATION — SQLite snapshot + delta 24h + chấm điểm outlier"
status: completed
priority: P1
effort: "1d"
dependencies: [1]
completed: 2026-09-09
smoke_test: "PASS — backdate snapshot 2026-09-08 = 88% view hôm nay rồi chạy lại: 114/114 video tính ra views_24h. Nhãn sau khi hiệu chỉnh: NOISE 39 · WATCH 49 · RISING 9 · BREAKOUT 8 · PROVEN_NICHE 7 · NEW_CHANNEL_HIT 3 (trên 117 video). Lượt 2 chỉ tốn 5 quota + 8s nhờ cache baseline."
---

# Phase 2 — FOUNDATION: lưu trữ, delta, chấm điểm

## Overview

Biến tool từ "chụp ảnh một lần" thành "theo dõi hằng ngày": SQLite giữ snapshot khoá theo `(id, snap_date)`, từ đó tính được delta view — tín hiệu thật của việc video *đang* được thuật toán đẩy, khác hẳn view tích luỹ.

## Related Code Files

**Create** — `src/store.py`, `src/score.py`, `src/run_daily.py` (khung orchestrator)

## Quyết định thiết kế phát sinh khi làm

### 1. `hit_rate` KHÔNG dùng để nhận diện "ngách đáng test"

Thiết kế ban đầu định nghĩa `hit_rate` = tỉ lệ video ≥3× median của chính kênh. Khi cài xong mới thấy nó **đo ngược điều mình cần**: kênh nào *mọi* video đều đạt 100k view sẽ có median cao, nên không video nào đạt 3× median → `hit_rate ≈ 0`. Đúng kênh đáng học lại bị chấm 0 điểm.

→ Thay bằng **`ch_mult` = median_views / max(subs, min_subs)** — đo **độ ỔN ĐỊNH của việc vượt quy mô**, tức video *điển hình* (không phải video may mắn nhất) kéo được bao nhiêu lần số sub. `hit_rate` giữ lại làm số liệu tham khảo (đo độ giật cục), không dùng để gán nhãn.

### 2. Ngưỡng phải hiệu chỉnh trên phân phối thật, không đặt bằng cảm giác

Ngưỡng đầu tiên (`ch_mult ≥ 5`, `median ≥ 20.000`, `≥5 video`) chỉ **2/50 kênh** đạt — nhãn gần như không bao giờ bật. Đo phân phối thật: median-của-median = **3.104**.
→ Chốt `ch_mult ≥ 3.0`, `≥8 video`, `median ≥ 5.000` → khoảng 8% số kênh, đúng tầm "top tier".

### 3. `RISING` với ngưỡng `views_24h > 0` là vô nghĩa

Bật cho **58/117 video** ngay lượt đầu. → Đổi thành *đang leo thật*: `views_24h ≥ 2.000` **và** `≥8% tổng view của chính video đó đến trong 1 ngày`. Còn 9/117.

### 4. Delta phải chia cho số ngày THẬT giữa 2 snapshot

Snapshot trước không chắc là hôm qua (tool có thể nghỉ vài ngày, VPS tắt). Lấy hiệu thô rồi gọi là "views_24h" sẽ thổi phồng gấp mấy lần và làm nhãn `RISING` loạn. → `views_24h = (views − prev_views) / số_ngày_cách_nhau`, có lưu `delta_gap_days`.

### 5. Baseline chỉ tính cho kênh ứng viên

Mỗi kênh tốn 2 quota (`playlistItems` + `videos`). Tính cho toàn bộ ~2.000 kênh quét được là lãng phí. → Lọc `subs ≥ min_subs`, `ch_age ≤ max_ch_age_days`, **`views ≥ 10.000`** rồi xếp hạng theo `views/subs`, lấy tối đa 400 kênh/lượt, **cache vĩnh viễn** trong `channel_baseline`. Lượt 2 trở đi gần như không tốn quota.

## Acceptance Criteria

- [x] Chạy lại nhiều lần trong ngày là idempotent (khoá `(id, snap_date)`)
- [x] `views_24h` tính đúng khi có snapshot cũ — verify bằng backdate
- [x] Phân bố nhãn hợp lý, không nhãn nào nuốt >50% dữ liệu
- [x] 1 video khớp nhiều keyword/ngách → 1 dòng, gộp danh sách (104 ca trùng ở Phase 1)
- [x] Baseline cache lại, lượt sau không tính lại
