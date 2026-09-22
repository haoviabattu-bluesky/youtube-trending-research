---
title: YouTube Trend & Outlier Hunter
status: in-progress
priority: P0
created: 2026-09-09
type: implementation
source: brainstorm-summary.md
---

# Plan — YouTube Trend & Outlier Hunter

Tool chạy hằng ngày, quét YouTube tìm **video bứt phá** và **kênh mới nhiều view** trong ngách faceless JP, chấm điểm outlier rồi báo cáo lên Google Sheet. Discovery keyless (0 quota) + enrich bằng YouTube Data API. SQLite giữ snapshot theo ngày để tính delta 24h.

## Context Links

- Brainstorm: [brainstorm-summary.md](brainstorm-summary.md) — §4 so sánh approach, §5.2 bộ chỉ số, §10 decisions locked
- Skill nền: `@C:\Users\admin\.claude\skills\youtube_research_ext.md` (§0 đường không-extension), `daily-batch-vps-scheduler.md` (Phase 6), `gsheet-pipeline-builder.md`, `quy_tac_tao_tool.md`

## Phases

| # | Phase | Status | Priority | Effort | Depends On |
|---|---|---|---|---|---|
| 1 | [PROBE — discovery + enrich ra CSV](phase-01-probe-discovery-enrich.md) | ✅ completed | P1 | 0.5d | — |
| 2 | [FOUNDATION — SQLite snapshot + delta + scoring](phase-02-store-score.md) | ✅ completed | P1 | 1d | 1 |
| 3 | [**MVP + SHEET** — push tab + đọc ngược TRD_CONFIG ⟵ **SHIP**](phase-03-sheet-mvp.md) | ✅ completed | P1 | 1d | 2 |
| 4 | [DEEPDIVE — transcript + comment top 5](phase-04-deepdive.md) | ✅ completed | P2 | 1d | 3 |
| 5 | [WATCHLIST + KEYWORD MOMENTUM + content gap](phase-05-keyword-momentum.md) | ✅ completed | P2 | 0.5d | 3 |
| 6 | [DEPLOY — Task Scheduler máy nhà → systemd timer VPS](phase-06-deploy.md) | pending | P2 | 0.5d | 4,5 |
| 7 | POLISH — Google Trends Playwright, alert Telegram, README | pending | P3 | 0.5d | 6 |

Phase 4 ∥ 5 (cùng deps `[3]`, không đụng nhau) → chạy song song được.

## Key Dependencies

- Python 3.13 (`py -3.13`) — đã có
- `requests`, `gspread`, `google-api-python-client`, `pandas` — đã cài
- `youtube-transcript-api` 1.2.4, `youtube-comment-downloader` 0.1.83 — đã cài (Phase 4)
- `YOUTUBE_API_KEY` — đã có, verify 2026-09-09 (videos/channels/search đều HTTP 200)
- Service account `claude-sheets-reader@fifth-glider-495702-b4.iam.gserviceaccount.com` → key tại `d:/CLAUDE/credentials/google-sheets-key.json`
- Google Sheet `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` (tên "YOUTUBE") — verify mở được; tab sẵn có: `GMAIL`, `NOTE`, `TRENDING`

## Decisions Locked (trích từ brainstorm §10)

- D1 Hybrid InnerTube discovery + Data API enrich
- D3 Bỏ Google Trends/pytrends (verify 429)
- D4 `breakout` (so median kênh) là chỉ số chính, `mult` (view/sub) chỉ phụ
- D5 Sàn `subs ≥ 300`, trần `ch_age ≤ 1095 ngày`
- D6 SQLite là nguồn chân lý, Sheet là lớp báo cáo
- D8 **Chỉ append/update; không xoá dòng/cột; chỉ đụng tab `TRENDING` + prefix `TRD_`**
- D9 Máy nhà trước, VPS sau

## Out of Scope

Dashboard web · tải/đăng video · API trả phí bên thứ 3 · Shorts · ngách EN/KR giai đoạn đầu · NotebookLM · mọi thao tác xoá trên Sheet. Chi tiết: brainstorm §11.

## Success Criteria (Plan-Level)

- [ ] 1 lần chạy ≤ 15 phút / 150 keyword × 2 ngách
- [ ] ≥ 30 kênh mới (<180 ngày) phát hiện mỗi tuần
- [ ] `views_24h` tính đúng sau 2 lần chạy cách ≥20 giờ
- [ ] Parse InnerTube thành công ≥ 95%
- [ ] Quota Data API ≤ 3.000/ngày
- [ ] Chạy tự động 7 ngày liên tiếp không lỗi
- [ ] 0 dòng bị xoá trong Sheet (số dòng tab GMAIL/NOTE không đổi)

## Next Step

→ [phase-01-probe-discovery-enrich.md](phase-01-probe-discovery-enrich.md)
