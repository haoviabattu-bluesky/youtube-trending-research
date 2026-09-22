---
title: YouTube Trend & Outlier Hunter — săn kênh/video hiện tượng hằng ngày
date: 2026-09-09
status: approved
type: brainstorm
next: /ck:plan
---

# Brainstorm — YouTube Trend & Outlier Hunter

## 1. Problem Statement

Cần tìm **ngách YouTube faceless đáng làm** trước khi nó thành trend lớn. YouTube đã bỏ trang Trending tổng hợp (2025), Studio Trends không có API, và pytrends đã bị Google chặn 429. Việc tìm tay ("video nào nhiều view") cho ra toàn kênh triệu sub — không nhân bản được. Thứ đáng săn là **hiện tượng**: kênh nhỏ/mới có video view gấp hàng chục lần subscriber, và **bùng nhiều lần chứ không phải một video may mắn**. Cần tool tự chạy hằng ngày, báo cáo lên Google Sheet.

## 2. Requirements (Approved)

**Functional**
- Quét ≥150 keyword/ngày trên ≥2 ngách (JP người già/sức khỏe/tiền hưu; JP satori/chuyện cảm động/2ch)
- Phát hiện outlier ở 2 cấp: **video** (bứt phá so với baseline kênh) và **kênh** (mới + nhiều hit)
- Theo dõi delta theo ngày (`views_24h`) — tín hiệu "đang được thuật toán đẩy", không chỉ view tích luỹ
- Tự tính momentum + content gap theo keyword (thay Google Trends đã chết)
- Đào sâu top 5 video/ngày: transcript + comment → hook, cấu trúc, insight khán giả
- Ghi báo cáo lên Google Sheet; đọc ngược config (keyword/ngưỡng) từ chính Sheet đó
- Chạy hằng ngày tự động: máy nhà trước, VPS sau

**Non-Functional**
- 1 lần chạy ≤ 15 phút cho 150 keyword × 2 ngách
- **TUYỆT ĐỐI không xoá dòng/cột nào trong Google Sheet** (chỉ append/update) — quy tắc global của user
- Không phụ thuộc 1 nguồn duy nhất: keyless chết → fallback API, API hết quota → fallback keyless
- File code ≤ 200 dòng/file
- Chạy lại giữa chừng không hỏng dữ liệu (idempotent theo `(id, snapshot_date)`)

## 3. Tech Stack (Approved)

| Lớp | Chọn | Lý do |
|---|---|---|
| Ngôn ngữ | Python 3.13 (`py -3.13`) | Đã có sẵn toàn bộ lib cần |
| Discovery | InnerTube `youtubei/v1/search` (requests, keyless) | 0 quota, không giới hạn keyword — **đã verify HTTP 200** |
| Enrich | YouTube Data API v3 (`videos.list`, `channels.list`, `playlistItems.list`) | 1 quota/50 item, số liệu chính xác — **đã verify key sống** |
| Enrich fallback | Channel `/about` HTML scrape | Lấy được subs + total views + ngày tạo kênh khi API chết |
| Transcript | `youtube-transcript-api` 1.2.4 | Đã cài, đã verify |
| Comment | `youtube-comment-downloader` 0.1.83 | Đã cài, đã verify |
| Lưu trữ | SQLite (`data/trending.db`) | Cần snapshot theo ngày để tính delta; Sheet không làm được việc này |
| Báo cáo | `gspread` + service account | Đã có key, đã verify mở được Sheet |
| Lịch chạy | Windows Task Scheduler (P1) → systemd timer + flock (P2, VPS) | Theo skill `daily-batch-vps-scheduler.md` |

## 4. Evaluated Approaches

| # | Approach | Pros | Cons | Decision |
|---|---|---|---|---|
| A | **YouTube Data API 100%** | Sạch ToS, chạy tốt từ IP datacenter, schema ổn định | `search.list` = **100 quota/lượt** → chỉ ~80 keyword/ngày/key. Muốn quét rộng phải nuôi nhiều key | ❌ Rejected — trần quota giết chết mục tiêu quét rộng |
| B | **Keyless InnerTube 100%** | 0 quota, keyword không giới hạn, chạy được ngay | IP datacenter/VPS dễ dính "Sign in to confirm you're not a bot"; schema YouTube đổi là gãy; subs bị làm tròn | ❌ Rejected làm giải pháp duy nhất — quá mong manh cho job chạy hằng ngày |
| C | **Hybrid: InnerTube discovery + Data API enrich** | Discovery 0 quota (quét 300+ keyword/ngày) + số liệu enrich chính xác chỉ tốn ~1 quota/50 video → **10.000 quota/ngày dư sức**. Mỗi lớp có fallback sang lớp kia | Hai code path phải bảo trì | ✅ **SELECTED** |
| D | Scrape YouTube Studio Trends (Playwright + login) | Có Top searches / Breakout / Content gaps chính thức của YouTube | Không có API, phải login, gãy khi đổi UI, không chạy nổi headless trên VPS | ⏸ Đẩy sang Phase 7 (P3, optional, chạy máy nhà) |
| E | API bên thứ 3 (vidIQ / SocialBlade / viewstats) | Có sẵn chỉ số outlier | Trả phí, rate limit, dữ liệu hộp đen không kiểm chứng được | ❌ Rejected — đã ghi vào Out of Scope |

**Google Trends:** pytrends trả `429 TooManyRequestsError` ngay request đầu (verify 2026-09-09) → **loại khỏi kiến trúc chính**. Thay bằng momentum tự tính từ chính data quét được (§5).

## 5. Final Architecture

```
                 ┌─────────────────────────────────────────┐
                 │  Google Sheet 1xu4iNud… (tab TRD_CONFIG)│  ← user sửa keyword/ngưỡng
                 └────────────────┬────────────────────────┘
                                  ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ [1] DISCOVER  src/innertube.py           (keyless, 0 quota)       │
  │     mỗi keyword × 3 lát thời gian: today / this week / this month │
  │     params: CAMSBAgCEAE / CAMSBAgDEAE / CAMSBAgEEAE (sort=view)   │
  │     + uploads playlist của watchlist kênh (Data API, 1 quota/kênh)│
  └────────────────────────────────┬──────────────────────────────────┘
                                   ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ [2] ENRICH   src/ytapi.py (chính) ─fallback→ src/innertube.py     │
  │     videos.list   → publishedAt chính xác, like, comment, duration│
  │     channels.list → subs, videoCount, viewCount, ngày tạo kênh    │
  └────────────────────────────────┬──────────────────────────────────┘
                                   ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ [3] STORE    src/store.py → SQLite data/trending.db               │
  │     video_snapshot(video_id, snap_date, views, likes, comments)   │
  │     channel_snapshot(channel_id, snap_date, subs, total_views)    │
  │     → delta 24h = snapshot hôm nay − snapshot hôm qua             │
  └────────────────────────────────┬──────────────────────────────────┘
                                   ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ [4] SCORE    src/score.py — 5 chỉ số + nhãn (§5.2)                │
  └───────────────┬───────────────────────────────┬───────────────────┘
                  ▼                               ▼
  ┌──────────────────────────────┐  ┌─────────────────────────────────┐
  │ [5] DEEPDIVE src/deepdive.py │  │ [5b] KEYWORD MOMENTUM           │
  │  top 5 video → transcript +  │  │  n_new_7d, median_views_7d,     │
  │  comment → hook / insight    │  │  demand_delta%, content_gap     │
  └──────────────┬───────────────┘  └────────────────┬────────────────┘
                 └───────────────┬───────────────────┘
                                 ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ [6] PUSH   src/sheets.py → 6 tab (CHỈ append/update, KHÔNG xoá)   │
  └───────────────────────────────────────────────────────────────────┘
```

### 5.1 Data model (SQLite)

```sql
video(video_id PK, channel_id, title, published_at, duration_s, kw_first, first_seen)
video_snapshot(video_id, snap_date, views, likes, comments, PRIMARY KEY(video_id, snap_date))
channel(channel_id PK, title, created_at, niche, first_seen, watchlist INT)
channel_snapshot(channel_id, snap_date, subs, total_views, video_count, PRIMARY KEY(channel_id, snap_date))
keyword_snapshot(keyword, snap_date, n_new_7d, median_views_7d, p90_views_7d, n_new_channels)
deepdive(video_id, snap_date, hook, structure, insight, suggested_titles)
```

### 5.2 Bộ chỉ số & nhãn

**Cấp video**
| Chỉ số | Công thức | Ý nghĩa |
|---|---|---|
| `views_24h` | snapshot hôm nay − hôm qua | Đang được đẩy hay đã nguội |
| `vph` | `views / giờ_kể_từ_khi_đăng` | Vận tốc |
| `mult` | `views / max(subs, 500)` | Outlier so với quy mô kênh — **sàn 500 chống nhiễu** |
| `breakout` | `views / median(10 video gần nhất của kênh)` | Bứt phá so với chính kênh đó |
| `engagement` | `(likes + comments) / views` | Lọc view ảo / CM quảng cáo |

**Cấp kênh**
| Chỉ số | Ý nghĩa |
|---|---|
| `ch_age_days` | Từ `channels.list.snippet.publishedAt` |
| `hit_rate` | Số video breakout ≥3× / 10 video gần nhất — **chỉ số vàng** |
| `sub_growth_7d` | Delta subs 7 ngày |
| `upload_per_week` | Nhịp sản xuất (đo được có nhân bản nổi không) |

**Nhãn (ưu tiên giảm dần)**
| Nhãn | Điều kiện | Hành động |
|---|---|---|
| 🔁 `PROVEN_NICHE` | ≥3 video breakout trong 30 ngày | **Ngách đáng test ngay** |
| 🌱 `NEW_CHANNEL_HIT` | `ch_age ≤ 120d` AND `max_views ≥ 50k` AND `subs ≥ 300` | Nghiên cứu công thức |
| 🚀 `BREAKOUT` | `breakout ≥ 3` AND `age ≤ 14d` AND `views ≥ 30k` | Xem title/thumbnail |
| 📈 `RISING` | `vph` tăng 2 ngày liên tiếp | Theo dõi tiếp |
| ⚠️ `NOISE` | `subs < 300` OR `ch_age > 1095d` OR `engagement < 0.001` | Tự loại khỏi báo cáo |

**Score tổng** (chuẩn hoá z-score **trong cùng ngách**, không so chéo ngách):
```
score = 0.30·z(log breakout) + 0.25·z(log vph) + 0.20·z(log mult_capped)
      + 0.15·new_channel_bonus + 0.10·z(engagement)
```

### 5.3 Momentum & Content gap (thay Google Trends)

Mỗi keyword mỗi ngày ghi `n_new_7d` (cung), `median_views_7d` + `p90_views_7d` (cầu), `n_new_channels`.
- `demand_delta%` = `median_views_7d` hôm nay so với 7 ngày trước → keyword **đang tăng**
- `content_gap` = `z(median_views_7d) − z(n_new_7d)` → **cầu cao, cung thấp** = ngách trống đo được

## 6. Project Structure

```
E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\
├── CLAUDE.md
├── README.md
├── .gitignore
├── config/
│   ├── niches.yaml              # ngách → keyword, hl/gl, ngưỡng (bootstrap; sau đọc từ Sheet)
│   └── .env                     # YOUTUBE_API_KEY, SHEET_ID, GOOGLE_SHEETS_KEY
├── credentials/                 # (gitignore) → trỏ d:/CLAUDE/credentials/google-sheets-key.json
├── docs/
│   ├── project-overview-pdr.md
│   └── codebase-summary.md
├── src/
│   ├── innertube.py             # discovery keyless + channel/about fallback
│   ├── ytapi.py                 # Data API enrich + quota counter
│   ├── enrich.py                # hợp nhất 2 nguồn, chọn nguồn, fallback chain
│   ├── store.py                 # SQLite schema + upsert snapshot + delta
│   ├── score.py                 # chỉ số + nhãn + z-score theo ngách
│   ├── keywords.py              # momentum + content gap
│   ├── deepdive.py              # transcript + comment top N
│   ├── insight.py               # phân tích hook/insight
│   ├── sheets.py                # push 6 tab, append-only
│   └── run_daily.py             # orchestrator CLI
├── data/trending.db
└── deploy/                      # Phase 6: systemd unit, vps_control.py, start.bat/stop.bat
```

## 7. Implementation Phasing

| Phase | Deliverable | P | Effort | Deps |
|---|---|---|---|---|
| 1 | PROBE — `innertube.py` + `ytapi.py`, chạy 10 keyword ra CSV, đo latency + tỉ lệ lấy được subs/ngày tạo kênh | P1 | 0.5d | — |
| 2 | FOUNDATION — `store.py` + `score.py`, snapshot SQLite, tính `views_24h` + nhãn | P1 | 1d | 1 |
| 3 | **MVP + SHEET** — `sheets.py` push 4 tab + đọc ngược `TRD_CONFIG` ⟵ **SHIP CHECKPOINT** | P1 | 1d | 2 |
| 4 | DEEPDIVE — transcript + comment top 5 → tab `TRD_DEEPDIVE` | P2 | 1d | 3 |
| 5 | WATCHLIST + KEYWORD MOMENTUM + content gap → tab `TRD_KEYWORDS` | P2 | 0.5d | 3 |
| 6 | DEPLOY — Task Scheduler máy nhà, rồi systemd timer + flock trên VPS | P2 | 0.5d | 4,5 |
| 7 | POLISH — Google Trends qua Playwright (máy nhà), alert Telegram khi có 🔁, README | P3 | 0.5d | 6 |

Phase 4 và 5 **độc lập nhau** (cùng deps `[3]`) → chạy song song được.

## 8. Risks & Mitigations

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| YouTube đổi schema InnerTube → parser gãy | Cao | Parser phòng thủ (walk cây tìm `videoRenderer`, không index cứng); mọi field bọc try/except; fallback sang Data API; Phase 1 ghi rõ tỉ lệ parse thành công |
| IP VPS dính "Sign in to confirm you're not a bot" | Cao | Chạy máy nhà trước (IP đã verify sạch); Phase 6 test VPS riêng; nếu chặn → Data API-only mode hoặc proxy dân cư |
| Hết quota Data API (10k/ngày) | Thấp | Discovery không tốn quota; enrich chỉ ~1 quota/50 item. Thêm bộ đếm quota, tự dừng enrich và chuyển keyless khi chạm 9.000 |
| Subs bị làm tròn (16700 chứ không phải 16.743) | Thấp | Chấp nhận sai số ±3%; nhãn lọc theo **bậc** (≥300, ≥50k) chứ không so từng đơn vị |
| Nhiễu: kênh 7 subs mult 2618×, CM chính phủ 6 năm tuổi | **Đã gặp thật** | Sàn `subs ≥ 300`, trần `ch_age ≤ 1095d`, ngưỡng `engagement`, và ưu tiên `breakout` (so với chính kênh) hơn `mult` |
| Sheet phình / chạm giới hạn ô | Trung bình | Raw giữ trong SQLite; Sheet chỉ giữ N ngày gần nhất; tab `TRD_DAILY` ghi thêm cột `snap_date` để lọc |
| **Ghi đè/xoá nhầm dữ liệu tab GMAIL & NOTE có sẵn** | **Cao** | Tool **chỉ đụng tab có prefix `TRD_` + tab `TRENDING`**; hard-code whitelist tên tab; không bao giờ gọi `delete_rows`/`clear` |

## 9. Success Criteria

- [ ] 1 lần chạy đầy đủ ≤ **15 phút** cho 150 keyword × 2 ngách
- [ ] Phát hiện ≥ **30 kênh mới (<180 ngày)** mỗi tuần, có ≥1 video ≥50k view
- [ ] `views_24h` tính đúng sau 2 lần chạy cách nhau ≥20 giờ (verify bằng số cụ thể)
- [ ] Tỉ lệ parse InnerTube thành công ≥ **95%** số video trả về
- [ ] Quota Data API tiêu thụ ≤ **3.000/ngày** (còn dư ≥70%)
- [ ] Chạy tự động **7 ngày liên tiếp** không lỗi
- [ ] **0 dòng bị xoá** trong Google Sheet (verify bằng số dòng tab GMAIL/NOTE trước–sau)

## 10. Decisions Locked

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Kiến trúc **hybrid**: InnerTube discovery + Data API enrich | Né trần 100 quota/search; 300+ keyword/ngày |
| D2 | Ngách khởi đầu: **JP người già/sức khỏe/tiền hưu** + **JP satori/chuyện cảm động/2ch** | User chốt; đã có data probe thật |
| D3 | **Bỏ Google Trends/pytrends** khỏi kiến trúc chính | Verify 429 ngày 2026-09-09; thay bằng momentum tự tính |
| D4 | `breakout` (so với median kênh) là chỉ số **chính**, `mult` (view/sub) chỉ là phụ | Probe cho thấy `mult` thuần tạo rác nặng (kênh 7 subs → 2618×) |
| D5 | Sàn cứng `subs ≥ 300`, trần `ch_age ≤ 1095 ngày` | Chống 2 loại nhiễu đã gặp thật |
| D6 | SQLite là nguồn chân lý; Google Sheet chỉ là lớp báo cáo | Sheet không lưu được snapshot theo ngày để tính delta |
| D7 | Google Sheet vừa là **báo cáo** vừa là **bảng điều khiển** (tab `TRD_CONFIG`) | User sửa keyword không cần đụng code |
| D8 | Tool **CHỈ append/update**, không bao giờ xoá dòng/cột; chỉ đụng tab whitelist | Quy tắc global của user; Sheet đã có tab GMAIL/NOTE chứa data |
| D9 | Chạy **máy nhà trước**, VPS sau (Phase 6) | User chốt; IP nhà đã verify sạch |
| D10 | Studio Trends + Google Trends Playwright là **P3 optional** | Không có API, cần login, không headless được trên VPS |

## 11. Out of Scope

- ❌ Dashboard web / Streamlit — Google Sheet **là** UI
- ❌ Tải video, đăng video, tạo nội dung — đó là việc của skill `youtube-script` / `veo3_flow_automation`
- ❌ API trả phí bên thứ 3 (vidIQ, SocialBlade, viewstats)
- ❌ YouTube Studio Trends ở Phase 1–6 (đẩy sang Phase 7, optional)
- ❌ Ngách EN/US và KR ở giai đoạn đầu (thêm sau khi khung chạy ổn — chỉ cần thêm dòng trong `TRD_CONFIG`)
- ❌ NotebookLM knowledge base (cần browser mở + bấm tay, không tự động 100%)
- ❌ Phân tích Shorts (chỉ long-form ≥ 3 phút — faceless story/health là long-form)
- ❌ Xoá bất kỳ dòng/cột nào trong Google Sheet, kể cả để dọn dẹp

## 12. Next Step

→ `plan.md` (index 7 phase) → `phase-01.md` → code Phase 1.
