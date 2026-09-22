# YouTube Trend & Outlier Hunter

Quét YouTube hằng ngày để tìm **video bứt phá** và **kênh mới nhiều view** trong ngách faceless, chấm điểm outlier rồi báo cáo lên Google Sheet.

Discovery bằng InnerTube (không cần API key, **0 quota**, quét 300+ keyword/ngày) — enrich bằng YouTube Data API v3 (1 quota / 50 video). SQLite giữ snapshot theo ngày để tính delta 24h.

## Cài đặt

```bash
py -3.13 -m pip install requests pyyaml python-dotenv gspread google-api-python-client \
                        youtube-transcript-api youtube-comment-downloader
cp config/.env.example config/.env      # điền YOUTUBE_API_KEY + SHEET_ID
```

`config/.env`:
```
YOUTUBE_API_KEY=<API key từ Google Cloud, bật "YouTube Data API v3">
SHEET_ID=<id Google Sheet>
SHEET_TAB_MAIN=TRENDING
GOOGLE_SHEETS_KEY=d:/CLAUDE/credentials/google-sheets-key.json
```
Service account trong file key phải được share **Editor** trên Sheet đích.

## Chạy

```bash
# Chạy đầy đủ + đẩy lên Google Sheet  (~10 phút, ~660 quota)
py -3.13 -X utf8 src/run_daily.py

# Thử nghiệm: không đụng Sheet, in top 15 ra màn hình
py -3.13 -X utf8 src/run_daily.py --niche jp_senior --limit-kw 8 --windows week --dry-run

# Bỏ bước đào sâu (nhanh hơn nhiều) / bỏ tầng LLM / ép chạy keyless
py -3.13 -X utf8 src/run_daily.py --no-deepdive
py -3.13 -X utf8 src/run_daily.py --no-llm
py -3.13 -X utf8 src/run_daily.py --no-api

# Chỉ quét ra CSV, không lưu DB, không đụng Sheet (công cụ Phase 1)
py -3.13 -X utf8 src/run_probe.py --niche jp_senior,jp_satori --limit-kw 60
```

## Chạy tự động hằng ngày

```powershell
powershell -ExecutionPolicy Bypass -File deploy\install_task.ps1   # 07:00 mỗi ngày
Start-ScheduledTask -TaskName YouTubeTrendHunter                   # chạy thử ngay
Unregister-ScheduledTask -TaskName YouTubeTrendHunter -Confirm:$false   # gỡ
```
Log ghi vào `data/daily_YYYYMMDD.log`. `src/lockfile.py` chặn 2 lượt chạy chồng nhau.

## Báo cáo là bản CHẮT LỌC, không phải bảng tra cứu

Tab `TRENDING` mỗi ngày chỉ có **10 video tinh hoa, 10 kênh khác nhau** — đủ ít để đọc hết
trong 5 phút và mỗi dòng đều đã được đào sâu (hook + comment + insight ở tab `TRD_DEEPDIVE`).

Để lọt vào 10 dòng đó, video phải qua **cổng cứng**:

| Điều kiện | Vì sao |
|---|---|
| Kênh phải có baseline | Không biết video *điển hình* của kênh bao nhiêu view thì không nói được video này có đặc biệt không |
| `ch_mult ≥ 3` | **Cổng quan trọng nhất** — loại kênh spam đăng mỗi ngày ăn may 1 video |
| `views ≥ 30.000` | Đủ lớn để đáng nghiên cứu |
| Nhãn ≠ WATCH/NOISE | Phải là 🔁 / 🌱 / 🚀 / 📈 |
| Mỗi kênh tối đa 1 video | 10 dòng = 10 cơ hội khác nhau |

Nếu chưa đủ 5 video qua cổng, tool tự **nới `ch_mult`** xuống 1.0 rồi 0 và **ghi rõ trong log**.

Dữ liệu thô đầy đủ (3.000+ video/ngày) vẫn nằm trong `data/trending.db` nếu cần đào lại.

## Đọc báo cáo thế nào

Cột quan trọng nhất **không phải `views`** mà là **`ch_mult`** = view của video *điển hình* chia số sub.

| `ch_mult` | Nghĩa | Nên làm gì |
|---|---|---|
| ≥ 3 | 🔁 Kênh **đều đặn** vượt quy mô — có công thức chạy được | **Nghiên cứu để nhân bản** |
| 1–3 | Khá đều | Theo dõi tiếp |
| < 1 | ⚡ **Ăn may 1 video** — mọi video khác gần như chết | Chỉ học riêng video đó, đừng clone kênh |

Ví dụ thật (2026-09-09): kênh có video 500.027 view nhưng 12 video gần nhất chỉ 57–521 view
(`ch_mult` 0,14) — **không** đáng học. Kênh khác median 100.863 (`ch_mult` 30,0) — đó mới là cỗ máy.

> **Bắt buộc `-X utf8`** trên Windows — title tiếng Nhật sẽ vỡ với codepage cp1252.

## Sửa keyword / ngưỡng

`config/niches.yaml` — mỗi ngách có `hl`/`gl` và danh sách keyword. Ngưỡng chung ở `defaults`:

| Tham số | Mặc định | Ý nghĩa |
|---|---:|---|
| `min_subs` | 300 | Sàn chống nhiễu (kênh 7 subs cho `view/sub` = 2618× là vô nghĩa) |
| `max_ch_age_days` | 1095 | Trần 3 năm — loại CM/kênh chính phủ không nhân bản được |
| `min_duration_s` | 180 | Chỉ long-form, bỏ Shorts |
| `breakout_ratio` | 3.0 | Ngưỡng bứt phá so với median của chính kênh |
| `new_channel_days` | 120 | Định nghĩa "kênh mới" |
| `new_channel_min_views` | 50000 | View tối thiểu để tính là "hit" |

Từ Phase 3, tool đọc ngược tab `TRD_CONFIG` trên Sheet — sửa trực tiếp trên Sheet, không cần đụng file.

## ⛔ Quy tắc Google Sheet

Tool **chỉ append/update**, **không bao giờ xoá** dòng/cột, và chỉ đụng tab `TRENDING` + tab prefix `TRD_`. Các tab khác trong Sheet (`GMAIL`, `NOTE`) không được chạm tới.


## Công cụ nghiên cứu ngách (ngoài báo cáo hằng ngày)

```bash
# Chấm điểm NGÁCH ứng viên (không chấm video) — sửa danh sách ở config/explore.yaml
py -3.13 -X utf8 src/explore_niches.py --detail

# Dò kho ĐỀ TÀI cho ngách bí ẩn/vũ trụ — đo cung/cầu từng đề tài
py -3.13 -X utf8 src/topic_gap.py --topics config/topics_cases.yaml

# Tải tư liệu hình an toàn bản quyền (NASA/Wikimedia public domain, có sổ giấy phép)
py -3.13 -X utf8 src/stockfetch.py --q "black hole galaxy" --n 6 --sources nasa,commons
```

Bản thiết kế sản xuất ngách bí ẩn: `docs/LANE_A_BLUEPRINT.md`.

## Tài liệu

- Kiến trúc & quyết định: `plans/260909-1611-youtube-trend-outlier-hunter/brainstorm-summary.md`
- Roadmap 7 phase: `plans/260909-1611-youtube-trend-outlier-hunter/plan.md`
- Module map: `docs/codebase-summary.md`
