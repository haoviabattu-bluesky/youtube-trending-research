---
phase: 6
title: "DEPLOY — Task Scheduler máy nhà, rồi systemd timer trên VPS"
status: pending
priority: P2
effort: "0.5d"
dependencies: [4, 5]
smoke_test: ""
---

# Phase 6 — Deploy

## Overview

Chuyển từ "chạy tay" sang "tự chạy mỗi sáng". Máy nhà trước (IP đã verify sạch qua ~1.100 request), VPS sau khi user duyệt.

## Đã chuẩn bị sẵn

| File | Dùng cho |
|---|---|
| `deploy/run_daily.bat` | Task Scheduler gọi; ghi log kèm ngày vào `data/daily_YYYYMMDD.log` |
| `deploy/install_task.ps1` | Đăng ký task 07:00 hằng ngày, `-StartWhenAvailable` (chạy bù nếu máy tắt), `-MultipleInstances IgnoreNew` |
| `deploy/youtube-trend.service` / `.timer` | systemd cho VPS (chưa deploy) |
| `src/lockfile.py` | Khoá chống 2 lượt chạy chồng — chạy được cả Windows lẫn Linux (`fcntl.flock` chỉ có trên Linux) |

## Bước máy nhà

```powershell
powershell -ExecutionPolicy Bypass -File deploy\install_task.ps1
Start-ScheduledTask -TaskName YouTubeTrendHunter    # chạy thử ngay
```

## Bước VPS (CHỜ USER DUYỆT)

1. `timedatectl set-timezone Asia/Ho_Chi_Minh` — **bắt buộc trước**, nếu không `OnCalendar=07:00` là giờ UTC
2. Upload project (bỏ `data/`, `__pycache__`), `python -m venv venv && venv/bin/pip install -r requirements.txt`
3. Copy `config/.env` + `google-sheets-key.json`, `chmod 600`
4. **Chạy thử 1 lượt bằng tay TRƯỚC khi bật timer** — mục đích duy nhất là xem IP VPS có dính bot-check không
5. Bot-check → chạy `--no-api` fail luôn, khi đó: đổi sang proxy dân cư, hoặc giữ máy nhà

## Rủi ro

| Rủi ro | Xử lý |
|---|---|
| IP VPS dính "Sign in to confirm you're not a bot" | Bước 4 phát hiện ngay; `BotCheckError` làm tool thoát mã 2 chứ không chạy tiếp âm thầm |
| VPS timezone UTC → chạy sai giờ 7 tiếng | Bước 1, verify bằng `timedatectl` |
| Lượt trước treo, lượt sau vẫn nổ → 2 tiến trình cùng nện YouTube | `RunLock` (lock file có PID + hạn 2 giờ) |
| Máy nhà tắt lúc 07:00 | `-StartWhenAvailable` chạy bù |

## Acceptance Criteria

- [ ] Task chạy tự động 3 ngày liên tiếp trên máy nhà, log không lỗi
- [ ] `views_24h` có giá trị từ ngày thứ 2 (đây là bằng chứng delta hoạt động thật, không phải mô phỏng)
- [ ] `demand_delta_pct` có giá trị từ ngày thứ 8
- [ ] Chạy 2 lượt chồng nhau → lượt sau thoát sạch, log `[lock]`
- [ ] `GMAIL`/`NOTE` không đổi số dòng sau mỗi lượt
