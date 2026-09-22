# Codebase Summary

## Module map

| File | Trách nhiệm | Phụ thuộc | Trạng thái |
|---|---|---|---|
| `src/innertube.py` | Discovery keyless: `search(query, window)` + `channel_about(id)` + parser số/tuổi đa ngôn ngữ (JP/EN/KR). Ném `BotCheckError` khi IP bị chặn | `requests` | ✅ Phase 1 |
| `src/ytapi.py` | Enrich chính xác qua Data API: `videos_batch`, `channels_batch`, `recent_uploads`. Có `QuotaCounter` + `QuotaExhausted` khi chạm ngưỡng an toàn 9.000 | `requests` | ✅ Phase 1 |
| `src/enrich.py` | Hợp nhất 2 nguồn theo thứ tự ưu tiên API → scrape; cache metadata kênh; sinh dòng chuẩn `ROW_FIELDS` | `innertube`, `ytapi` | ✅ Phase 1 |
| `src/run_probe.py` | CLI Phase 1: keyword → CSV + thống kê parse/quota/gold | tất cả trên | ✅ Phase 1 |
| `src/store.py` | SQLite: schema + upsert snapshot `(id, snap_date)` + delta + dedupe video đa-keyword | — | ✅ Phase 2 |
| `src/score.py` | Chỉ số video + kênh → nhãn → score z-score theo ngách + `pick_elite()` | — | ✅ Phase 2 |
| `src/sheet_schema.py` | Cột từng tab + whitelist + 2 lớp guard | — | ✅ Phase 3 |
| `src/gapi.py` | Retry backoff cho Sheets API (60 read/phút) | `gspread` | ✅ Phase 3 |
| `src/publish.py` | Quyết định ghi gì lên tab nào + verify toàn vẹn | `report`, `sheets` | ✅ Phase 3 |
| `src/pipeline.py` | 2 bước nặng: quét keyword, tính baseline kênh | `innertube`, `ytapi` | ✅ |
| `src/sheets.py` | Ghi Sheet: **append/update only**, whitelist tab, guard_snapshot, migrate header | `gspread` | ✅ Phase 3 |
| `src/report.py` | Dựng ma trận giá trị cho từng tab (tách khỏi lớp ghi để test offline) | `score` | ✅ Phase 3 |
| `src/keywords.py` | Momentum + content gap (thay Google Trends) | `store` | ✅ Phase 5 |
| `src/deepdive.py` | Transcript + comment + title pattern + insight LLM (tuỳ chọn) | `youtube-transcript-api`, `youtube-comment-downloader` | ✅ Phase 4 |
| `src/lockfile.py` | Khoá chống 2 lượt chạy chồng (Windows + Linux) | — | ✅ Phase 6 |
| `src/run_daily.py` | Orchestrator hằng ngày | tất cả | ✅ |

## Data flow

```
config/niches.yaml ─(Phase 3: → tab TRD_CONFIG)─┐
                                                ▼
   innertube.search()  ──discovery, 0 quota──►  found{video_id: row}
                                                ▼
   enrich.build_rows() ──ytapi.videos_batch + channels_batch (fallback: /about scrape)
                                                ▼
   store.upsert_snapshot()  ──►  data/trending.db   (nguồn chân lý)
                                                ▼
   score.label()  ──►  🔁 PROVEN_NICHE / 🌱 NEW_CHANNEL_HIT / 🚀 BREAKOUT / 📈 RISING
                                                ▼
   sheets.push()  ──append only──►  Google Sheet (TRENDING + TRD_*)
```

## Quy ước

- Cột chuẩn của 1 dòng video: `enrich.ROW_FIELDS` — **mọi module dùng chung**, đừng tự định nghĩa lại
- Cột `src` ghi nguồn từng dòng dạng `v:api/c:scrape` để truy ngược khi số liệu đáng ngờ
- `snap_date` = `date.today().isoformat()` — khoá phân vùng của mọi snapshot
- Ngưỡng lấy từ `niches.yaml → defaults`, không hard-code trong logic

## Đã verify (2026-09-09)

- InnerTube params sort=viewCount: `CAMSBAgCEAE` today · `CAMSBAgDEAE` week · `CAMSBAgEEAE` month
- Parse rate 98.8% trên mẫu 80 video (yêu cầu ≥95%)
- 4 keyword × 1 lát = 63 video / 46 kênh, **3 quota**, 4 giây
- `uploads_playlist` = `"UU" + channel_id[2:]` — tính được, không cần gọi API
- Full run 120 kw × 3 lát: 3.239 dòng, 282s, **106 quota**, parse 98,3%, `ch_age_days` 100%
- Chế độ `--no-api` (keyless hoàn toàn) verify chạy được: subs/ngày-tạo-kênh lấy từ `/about`,
  `duration_s` lấy từ `lengthText` — **luôn test nhánh này riêng, nó không bao giờ chạy khi có API key**

## Số đo lượt chạy đầy đủ (2026-09-09)

125 keyword × 3 lát × 2 ngách → **3.375 video / 2.063 kênh**, dedupe còn 3.269.
**570 giây · 666 quota / 10.000** · parse InnerTube 98,3%.
Nhãn: NOISE 1.710 · WATCH 1.353 · PROVEN_NICHE 118 · BREAKOUT 48 · NEW_CHANNEL_HIT 40.
