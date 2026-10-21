---
title: NEWS RADAR — tool quét tin nóng/viral hằng ngày (Google · X · YouTube · Yahoo) để chọn đề tài video dạng tin tức
status: draft — chờ anh duyệt phương án
created: 2026-10-17
author: Claude (TRENDING-RESEARCH)
---

# 1. Vấn đề
Các lane hiện có (F/L/N/O/P/Q) là đề tài "evergreen" chọn theo tuần. Anh muốn thêm dạng video TIN TỨC:
tin nóng chính trị/thời sự/vụ án/giật gân lên trong ngày → cần biết SỚM cái gì đang viral, đã có ai làm video
chưa, nguồn tư liệu ở đâu, rồi quyết có làm hay không. Hiện không có tool nào trong `src/` làm việc đó
(`run_video_hunt.py` quét theo keyword ngách cố định, không theo trend thời gian thực).

# 2. Mục tiêu
- Mỗi 30–60 phút tự quét 5 nguồn trend, gom thành "cụm sự kiện", chấm độ nóng + khoảng trống cung–cầu trên YouTube.
- 2–3 lần/ngày trả bản tóm tắt ≤10 đề tài (tiêu đề VN+JP, vì sao nóng, góc kể, nguồn [Dn], rủi ro, còn nóng bao lâu).
- Với top 3–5: gói tư liệu sẵn (bài báo gốc đã đọc, số liệu, ảnh có nguồn, video đối thủ + hook).
- KHÔNG viết kịch bản, KHÔNG dựng video (ranh giới dự án, CLAUDE.md).

# 3. Nguồn đã probe thật 17/10/2026 (keyless, HTTP 200)
| Nguồn | URL | Lấy được | Ghi chú |
|---|---|---|---|
| Google Trends daily | `https://trends.google.com/trending/rss?geo=JP` | từ khoá + approx_traffic + bài báo kèm | pytrends chết nhưng RSS sống; đổi `geo` cho US/VN |
| Google News | `https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja` (+ `/rss/search?q=`) | tiêu đề/báo/giờ | tìm theo keyword cụm |
| Yahoo! JAPAN ranking | `https://news.yahoo.co.jp/ranking/access/news` | top truy cập + ヤフコメ ranking | ヤフコメ = chỉ số "dân cãi nhau" = giật gân |
| X trends (qua aggregator) | `https://trends24.in/japan/` (25 snapshot/giờ), `https://getdaytrends.com/japan/` | hashtag + thứ hạng theo giờ | X trực tiếp cần login, không dùng |
| YouTube | InnerTube search sort=viewCount window=today (`src/innertube.py` có sẵn) | video 24h + view + kênh | đo CUNG; `/feed/trending` HTML không có videoRenderer → cần browse FEtrending nếu muốn |
| Loại | NHK RSS (301), Reddit (403) | — | bỏ |

# 4. Kiến trúc đề xuất (5 lớp, mỗi lớp 1 file ≤200 dòng trong `src/news_radar/`)
1. **collect/** — 1 collector/nguồn, trả bản ghi chuẩn `(source, keyword, rank, traffic, url, ts)` → SQLite `data/news_radar.db` bảng `signal`.
2. **cluster.py** — gộp keyword cùng sự kiện (cùng tên người/địa danh/số vụ) bằng gemini-3.8-flash (ramclouds, `src/hunt_v2/llm_client.py` có sẵn) + gắn thể loại 政治/事件/芸能/経済/スポーツ + điểm "giật gân" 1–5.
3. **heat.py** — điểm nóng = số nguồn xuất hiện × tốc độ tăng giữa 2 snapshot × traffic; **khoảng trống** = cầu (trend) ÷ cung (số video YouTube 24h + tổng view). Trend to mà cung ít = cơ hội; đây là lõi giá trị.
4. **evidence.py** — top N cụm: `pw_search.py` (Chrome nền cổng 9461, Google→Yahoo) lấy 5–10 bài gốc, đọc trang, trích [Dn] số liệu/trích dẫn/mốc giờ; ảnh có nguồn; video đối thủ + hook qua `src/hook_fetch.py` (ASR khi bị chặn).
5. **brief.py** — Artifact HTML + bản markdown `runs/news_radar/<ngày>/brief_<giờ>.md`; ping Telegram khi 1 cụm vượt ngưỡng "bùng" (tăng ≥3× trong 1 giờ).

Lịch: 1 tiến trình `run_news_radar.py --loop 45m` (lockfile có sẵn `src/lockfile.py`), brief 07:00 / 12:00 / 19:00 JST.

# 5. Phương án
- **A. Radar nhẹ** (lớp 1–3 + brief không tư liệu): ~1 tuần. Biết cái gì nóng, chưa có nguồn.
- **B. Radar + gói tư liệu top 5** (lớp 1–5) — **KHUYẾN NGHỊ**: ~2 tuần. Đủ để h2dev viết ngay.
- C. B + tự gọi h2dev viết kịch bản: KHÔNG làm bây giờ (vi phạm ranh giới research/sản xuất; tin tức cần anh duyệt rủi ro từng tập).

# 6. Rủi ro phải nhìn trước
- **Tin nguội trong 24–48h.** Pipeline h2dev hiện 2–3 ngày/tập → phải có "đường nhanh" ≤12h (motion graphics + ảnh báo + TTS) hoặc chọn tin "nóng kéo dài" (phiên toà, điều tra, scandal nhiều hồi).
- **YouTube:** tin tức dùng lại footage/ảnh báo dễ bị "reused content" + giới hạn quảng cáo cho vụ án/thảm hoạ; vụ án đang điều tra có rủi ro phỉ báng người thật tên thật → cần ranh giới như Lane P (không bịa câu cho người thật, không dùng mặt người thật).
- **Chính trị:** CLAUDE.md đang cấm chính trị làm tập chính (lane Q). Lane tin tức là NGOẠI LỆ → anh xác nhận rõ.
- **Google chặn /sorry** khi tìm dày: dùng pw_search có sẵn, giãn nhịp; X chỉ qua aggregator.

# 7. Cần anh chốt (5 điểm)
1. Thị trường: chỉ JP, hay thêm US/VN? (mỗi thị trường = 1 bộ geo/hl, cùng code)
2. Thể loại cho phép: chính trị ✔/✘ · vụ án ✔/✘ · giải trí/芸能 ✔/✘ · thảm hoạ ✔/✘
3. Nhịp brief: 3 lần/ngày hay chỉ sáng? Nhận qua Artifact, Telegram, hay cả hai?
4. Chọn A hay B.
5. Kênh đăng: kênh mới riêng tin tức, hay gắn vào lane cũ (P/Q kiểu 海外の反応 về tin Nhật–Trung)?
