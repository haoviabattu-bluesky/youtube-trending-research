---
phase: 1
title: "PROBE — discovery keyless + enrich Data API ra CSV"
status: completed
priority: P1
effort: "0.5d"
dependencies: []
completed: 2026-09-09
smoke_test: "PASS — 2 ngách × 60 kw × 3 lát = 360 request, 282s, KHÔNG bot-check. 3.239 dòng / 3.135 video / 1.988 kênh. parse ok=4297 fail=74 (98,3%). ch_age_days 100%, published_at 100%, subs>0 95,6%. quota Data API = 106/10.000. gold NEW_CHANNEL_HIT = 69 video; kênh <180 ngày & >=300 subs = 292. Top: 他人の人生【タニジン】 32 ngày / 5.360 sub / 500.848 view"
---

# Phase 1 — PROBE: discovery + enrich

## Overview

Validate giả thuyết rủi ro nhất trước khi xây gì thêm: **InnerTube có quét được ≥150 keyword liên tục mà không bị bot-check không, và Data API có enrich đủ số liệu để chấm outlier không.** Đầu ra là 1 file CSV có đủ cột để chấm điểm bằng tay — chưa cần SQLite, chưa cần Sheet, chưa cần đa luồng.

## Context Links

- [brainstorm-summary.md §5](brainstorm-summary.md) — kiến trúc, §5.2 bộ chỉ số
- [plan.md](plan.md) — bảng phase
- Skill `youtube_research_ext.md` §0 (đường không-extension), §7 (cơ chế InnerTube)

## Requirements

**Functional**
1. `src/innertube.py` — search keyless theo keyword × 3 lát thời gian (`today` / `this week` / `this month`), sort theo view count; trả `video_id, title, channel, channel_id, views, age_text, age_hours`
2. `src/innertube.py` — `channel_about(channel_id)` fallback: `subs`, `total_views`, `joined_date`
3. `src/ytapi.py` — `videos_batch(ids)` (50/lượt) và `channels_batch(ids)` (50/lượt), có **bộ đếm quota** in ra cuối lượt chạy
4. `src/enrich.py` — hợp nhất: ưu tiên Data API, thiếu field nào mới rơi xuống scrape; đánh dấu `src` mỗi dòng
5. `config/niches.yaml` — 2 ngách JP với ≥60 keyword/ngách (bootstrap, sau chuyển sang tab `TRD_CONFIG`)
6. `src/run_probe.py` — CLI: `--niche`, `--limit-kw`, `--out out.csv`; sync, đơn luồng cho discovery, thread nhỏ (≤6) cho scrape fallback

**Non-Functional**
- Mỗi file ≤ 200 dòng
- Parser phòng thủ: walk cây tìm `videoRenderer`, mọi field bọc try/except, **đếm và in tỉ lệ parse thất bại**
- Throttle ≥0.4s giữa 2 request InnerTube
- `PYTHONIOENCODING=utf-8` / `-X utf8` cho tiếng Nhật trên Windows
- Không ghi gì lên Google Sheet ở phase này

## Architecture

```
config/niches.yaml
src/
  innertube.py     # search() + channel_about() + parse helpers (jnum, jage_hours)
  ytapi.py         # videos_batch() + channels_batch() + QuotaCounter
  enrich.py        # merge 2 nguồn + fallback chain
  run_probe.py     # CLI orchestrator → CSV
data/probe_YYYYMMDD.csv
```

## Related Code Files

**Create**
- `config/niches.yaml`
- `config/.env` (`YOUTUBE_API_KEY`, `SHEET_ID`, `GOOGLE_SHEETS_KEY`) + `.env.example`
- `src/innertube.py`
- `src/ytapi.py`
- `src/enrich.py`
- `src/run_probe.py`
- `.gitignore`

**Modify** — không có (project mới)

**Tái dùng** — logic `jnum()` / `jage_hours()` / walk `videoRenderer` đã verify trong prototype `proto_hunt.py` (scratchpad phiên 2026-09-09)

## Acceptance Criteria

- [ ] Chạy 2 ngách × ≥60 keyword không dính bot-check, không exception thoát giữa chừng
- [ ] CSV có đủ cột: `video_id, title, channel, channel_id, views, age_hours, published_at, likes, comments, duration_s, subs, ch_created_at, ch_age_days, total_views, keyword, niche, src`
- [ ] Tỉ lệ parse InnerTube thành công ≥ 95% (in ra số cụ thể)
- [ ] `ch_age_days` có giá trị cho ≥ 90% kênh
- [ ] Bộ đếm quota in ra tổng quota tiêu thụ, phải ≤ 500 cho lượt chạy này
- [ ] Chạy lại lần 2 không lỗi (không state gì phải dọn)

## Smoke Test

**Input**
```bash
py -3.13 -X utf8 src/run_probe.py --niche jp_senior,jp_satori --limit-kw 60 --out data/probe_20260909.csv
```

**Output mong đợi** (ghi số THẬT vào frontmatter `smoke_test:` sau khi chạy)
```
[discovery] N unique videos / M channels from K keywords in Ts
[parse] ok=X fail=Y (Z%)
[enrich] api_videos=A api_channels=B scrape_fallback=C
[quota] used=Q / 10000
[out] data/probe_20260909.csv — R rows
```

Kiểm bằng mắt: mở CSV, lọc `subs >= 300 AND ch_age_days <= 120 AND views >= 50000` → phải ra **≥10 dòng** (prototype ngày 2026-09-09 chỉ với 10 keyword đã ra 12 kênh thoả điều kiện này).

## Nếu Phase 1 FAIL

| Triệu chứng | Kết luận | Hành động |
|---|---|---|
| InnerTube trả HTML "Sign in to confirm you're not a bot" | IP bị chặn | Chuyển discovery sang `search.list` Data API, giảm còn ~80 keyword/ngày, cân nhắc thêm key |
| Parse thành công < 95% | YouTube đổi schema | Dump 1 response ra file, sửa parser, thêm test cố định |
| `ch_age_days` thiếu > 10% | `channels.list` không trả `publishedAt` cho kênh brand | Fallback scrape `/about`, đã verify lấy được `joinedDateText` |

## Kết quả thực tế (2026-09-09)

| Tiêu chí | Ngưỡng | Đo được | |
|---|---|---|---|
| Không bot-check trên 360 request | bắt buộc | không dính lần nào | ✅ |
| Parse InnerTube thành công | ≥95% | **98,3%** (4297/4371) | ✅ |
| `ch_age_days` có giá trị | ≥90% | **100%** | ✅ |
| Quota Data API | ≤500 | **106** / 10.000 | ✅ |
| Gold NEW_CHANNEL_HIT | ≥10 | **69** video | ✅ |
| Thời gian chạy | ≤15 phút | **4 phút 42** | ✅ |

Enrich chạy 100% qua Data API (`v:api/c:api`), nhánh scrape fallback **chưa được kích hoạt lần nào**
→ cần test riêng bằng `--no-api` trước khi tin nó hoạt động.

## Phát hiện cần xử lý ở Phase 2

1. **Trùng video giữa 2 ngách** — 104 video khớp keyword của cả `jp_senior` lẫn `jp_satori` → hiện ra 2 dòng.
   Phase 2 phải dedupe theo `video_id`, gộp `keyword`/`niche` thành danh sách thay vì nhân dòng.
2. **4,4% dòng có `subs = 0`** — kênh ẩn số subscriber. Xử lý như `subs = min_subs` khi tính `mult`,
   và không loại thẳng vì `breakout` (so median chính kênh) vẫn tính được.
3. **2% là video < 3 phút** — lọc ở bước score bằng `min_duration_s`, không lọc ở discovery
   (giữ lại để đo momentum keyword ở Phase 5).
4. ~~Nhánh `channel_about()` scrape chưa chạy thật~~ → **đã test `--no-api`: 49/49 dòng lấy đủ**
   `subs` + `ch_created_at` + `ch_age_days` từ scrape (`src=v:it/c:scrape`).
   Test này **bắt được 1 bug thật**: chế độ keyless không có `duration_s` → bộ lọc `min_duration_s`
   giết sạch kết quả (gold = 0). Đã sửa: `innertube.parse_length()` đọc `lengthText` ('15:29' → 929s),
   `enrich` ưu tiên API rồi mới rơi xuống giá trị này. Verify lại: 78/78 dòng có duration (226s–6988s).
