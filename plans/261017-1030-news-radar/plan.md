---
title: NEWS RADAR — plan (phương án B, chỉ Nhật, mọi thể loại, báo cáo ngày cho lane Q MG_STUDIO)
status: P1–P3 done 2026-10-17 (brief thật 10 đề tài, 1 LÀM NGAY) · P4 lịch chạy chờ anh đọc brief
approved_by_user: 2026-10-17 (chat: "chỉ Nhật / cho phép tất cả / file báo cáo mỗi ngày / B / lane Q")
---

# Quyết định đã chốt (anh, 17/10/2026)
1. Thị trường: CHỈ Nhật (`geo=JP`, `hl=ja`).
2. Thể loại: tất cả; cái nào nóng hơn thì chọn. Mỗi ngày làm 3–5 video → brief ≤10 đề tài, xếp hạng gắt.
3. Đầu ra: 1 file báo cáo/ngày để dự án làm phim (MG_STUDIO lane Q) đọc và làm.
4. Phương án B: radar + gói tư liệu cho top 5.
5. Đưa vào lane Q: báo cáo ghi ở `E:\CLAUDE\YOUTUBE\MG_STUDIO\lanes\q\NEWS_RADAR\<ngày>.md` + 1 dòng ở `BAN_GIAO_TRENDING.md`.
   Lane Q có khung Nhật–Trung (LUAT.md) → mỗi đề tài gắn cờ `q_fit` (có góc TQ/nước ngoài) nhưng KHÔNG lọc bỏ.

# Kiến trúc file (src/news_radar/, mỗi file ≤200 dòng)
| File | Việc | Phụ thuộc |
|---|---|---|
| `parsers.py` | parse thuần (Google Trends RSS, Google News RSS, Yahoo ranking HTML, trends24/getdaytrends HTML) → list signal | không mạng, test bằng fixtures |
| `collectors.py` | tải 5 nguồn + ghi `signal` | parsers, store |
| `store.py` | SQLite `data/news_radar.db`: signal / cluster / supply / evidence | — |
| `cluster.py` | gộp keyword 24h thành cụm sự kiện bằng LLM (gate `news_cluster`) | hunt_v2.llm_client |
| `supply.py` | InnerTube search window=today cho từng cụm → cung YouTube | src/innertube.py |
| `heat.py` | điểm nóng · tốc độ · khoảng trống cung–cầu · điểm cuối | thuần, test được |
| `evidence.py` | top 5: đọc bài gốc (requests → pw_search `f` dự phòng), trích đoạn; hook 2 video đối thủ (tuỳ chọn) | pw_search.py, hook_fetch |
| `brief.py` | LLM viết tiêu đề JP+VI / vì sao nóng / góc kể / rủi ro (gate `news_brief`) → markdown + json | llm_client |
| `src/run_news_radar.py` | CLI: `--collect` · `--brief` · `--loop 45` · `--dry-run` · `--handoff` | lockfile |
| `config/news_radar.yaml` | geo, nguồn bật/tắt, ngưỡng, đường ra | — |

# Phase
- ✅ **P1 thu + parse + store** — smoke 17/10 12:22: 6 nguồn 10/30/44/22/140/15 keyword, 257 signal vào DB; 6 test parser trên fixtures thật.
- ✅ **P2 cụm + cung + điểm** — smoke 17/10 12:38: 21 cụm/100 keyword, cung đo được (片山 28 video/1,9M view); 6 test heat. Sửa 3 bẫy (SSE UTF-8, max_tokens, gap).
- ✅ **P3 tư liệu + brief + bàn giao lane Q** — smoke 17/10 12:40: `E:\CLAUDE\YOUTUBE\MG_STUDIO\lanes\q\NEWS_RADAR\2026-10-17.md` 10 đề tài, 11 bài gốc đọc được, [D1]–[D5] có tên báo, 1 LÀM NGAY (片山財務相).
- **P4 loop + Scheduled Task** — sau khi anh đọc brief đầu và góp ý.
