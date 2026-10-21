# CLAUDE.md — PHẦN CHI TIẾT (tách khỏi CLAUDE.md ngày 2026-10-21 để giảm ngữ cảnh nền mỗi lượt)

Nguyên văn các mục cũ, không sửa chữ nào. CLAUDE.md chỉ còn luật bắt buộc + trỏ sang đây. Đọc đúng mục khi task chạm tới.

## Sự thật đã verify (2026-09-09) — đừng probe lại
- InnerTube search keyless: HTTP 200, trả view + tuổi video + channelId. Params sort=viewCount:
  `CAMSBAgCEAE` = today · `CAMSBAgDEAE` = this week · `CAMSBAgEEAE` = this month
- Channel `/about` HTML: lấy được `subscriberCountText`, `viewCountText`, `joinedDateText` (ngày tạo kênh)
- `channels.list` trả `snippet.publishedAt` chính xác tới mili-giây + `contentDetails.relatedPlaylists.uploads`
- **pytrends CHẾT** — `429 TooManyRequestsError` ngay request đầu. Đừng đưa Google Trends vào đường chính.
- Nhiễu đã gặp thật: kênh 7–25 subs cho `view/sub` = 2618× (vô nghĩa); CM chính phủ kênh 6 năm tuổi lọt top
  → luôn dùng sàn `subs ≥ 300` + trần `ch_age ≤ 1095d`, và ưu tiên `breakout` (so median kênh) hơn `mult`
- **`hit_rate` đo NGƯỢC thứ mình cần.** Kênh nào MỌI video đều 100k view sẽ có median cao nên không video
  nào đạt 3× median → `hit_rate ≈ 0`, đúng kênh đáng học lại bị chấm 0. Dùng **`ch_mult = median/subs`**
  (độ ỔN ĐỊNH) để nhận diện "ngách đáng test"; `hit_rate` chỉ giữ làm số tham khảo.
- **Ngưỡng phải hiệu chỉnh trên phân phối thật.** `ch_mult≥5 + median≥20k` chỉ 2/50 kênh đạt (median-của-median
  thật = 3.104) → chốt `≥3.0 / ≥8 video / ≥5.000`. `RISING` với ngưỡng `views_24h>0` bật cho 58/117 video.
- **Baseline phải BỎ video <7 ngày.** Kênh faceless đăng mỗi ngày nên 12 video mới nhất luôn dính mấy cái
  chưa kịp tích view — đo thật median 306 vs 460. Không lọc thì `breakout` của mọi video bị thổi phồng.
- **`views_24h` phải chia cho số ngày THẬT** giữa 2 snapshot (tool có thể nghỉ vài ngày).
- **Phân biệt "kênh có công thức" với "kênh ăn may".** シニア健康日和 có video 500.027 view nhưng 12 video
  gần nhất chỉ 57–521 view (`ch_mult` 0,14) — KHÔNG đáng học. 他人の人生【タニジン】 median 100.863
  (`ch_mult` 18,8) — đó mới là cỗ máy. Cột `verdict` trong `TRD_NEW` nói thẳng điều này.
- **Chạy lại trong ngày làm nhân đôi báo cáo** → `write_daily_block()` ghi đè TẠI CHỖ khối cùng `snap_date`.
  Không xoá được nên lượt sau ít dòng hơn thì dòng dư nằm lại — tool cảnh báo chứ không im lặng.
- **Lượt chạy NHỎ từng đè mất báo cáo đầy đủ** (test 3 keyword xoá top 28 dòng, chương trình vẫn báo
  thành công). `ShrinkGuard` chặn khi lượt mới < 70% số dòng khối cùng ngày; muốn đè phải `--force`.
  → Khi test tay, LUÔN dùng `--dry-run`, đừng dùng lượt nhỏ ghi thẳng Sheet.
- **Sheets API giới hạn 60 read/phút/user** — gspread KHÔNG tự retry. Chạy vài lượt liên tiếp là
  429 chết giữa chừng. Mọi lời gọi Sheet phải bọc `gapi.retry_api` (backoff luỹ thừa + jitter),
  và `guard_snapshot` dùng `values_batch_get` (1 request) chứ đừng đọc từng tab.
- **Guard đếm cột A là SÓT.** `GMAIL` có 12 dòng trống cột A nhưng có dữ liệu cột khác → hai cách
  đếm ra 89 vs 101, tưởng mất dữ liệu. Tab của user phải đọc `A:Z` rồi băm nội dung.
- **Đừng gom keyword theo `niches.split("|")[0]` của video.** Video khớp keyword của 2 ngách sẽ xé
  1 keyword thành 2 dòng số liệu, mà khoá DB là `(keyword, snap_date)` nên đè nhau, mất dữ liệu im lặng.
- ramclouds `https://ramclouds.me/v1` + model `gemini-3.5-flash-low` là tầng insight (key trong `config/.env`).
  API key YouTube KHÔNG gọi được Gemini (`generativelanguage` trả 403 blocked).

## Thiết kế báo cáo (user chốt 2026-09-09)
Tab `TRENDING` = **10 video tinh hoa/ngày, mỗi kênh 1 video** — bản chắt lọc để đọc hết,
KHÔNG phải bảng tra cứu 150 dòng. Cổng lọc ở `score.is_elite()`; then chốt là `ch_mult ≥ 3`
(loại kênh ăn may). Dữ liệu thô đầy đủ vẫn nằm trong SQLite.
Dòng thừa của khối cũ trong ngày được đánh dấu `<ngày> ⏹cũ` ở cột A — **annotate chứ không xoá**.

## Lane A — 都市伝説/vũ trụ/bí ẩn (đã bàn giao sang h2dev)
- `docs/LANE_A_BLUEPRINT.md` — cấu trúc sản xuất (khung 5 chương, số đo kịch bản, nguồn tư liệu)
- `docs/LANE_A_NICHE_KIT.md` — 8 mục nghiên cứu ngách (khán giả, từ khoá, công thức tiêu đề +
  thumbnail, nhịp giữ chân, 10 nguyên tắc, khoảng trống, checklist 5 video đầu)
- **Thân video = clip stock; THUMBNAIL = ảnh AI.** Đừng lẫn hai cái.
- **Retention của đối thủ KHÔNG lấy được** — đã thử 4 client InnerTube + trang watch + phiên đã
  đăng nhập, đều không có heatmap. Đừng thử lại.

## Lane C — 「他人の人生」nghề nghiệp/lối sống (✅ ĐÃ DUYỆT 2026-09-10, đã bàn giao)
- Kênh mẫu: 他人の人生【タニジン】 `UCvA0jwPl5qjhsHQOWuZYe-g`
- `docs/LANE_C_HANDOFF.md` — bàn giao đầy đủ 13 mục (khán giả, cấu trúc, quy trình sản xuất
  10 bước, đặt tên/mô tả/hashtag/tag SEO kênh mới, checklist video đầu)
- Đã copy sang `h2dev/docs/laneC_from_research/` cùng data gốc (transcript/comment/thumbnail) + tool
- **`ch_mult` cao KHÔNG đủ — phải kiểm `trend` thật** (đã dính: 妻は静かに笑う `ch_mult` 34,9 nhưng
  `trend` 0,43 đang tụt, suýt đề xuất nhầm lần 2 sau 極秘接触 ở Lane A)
- Kênh 70代けいちゃんの台所 số liệu đẹp nhưng LOẠI HẲN vì là vlog người thật, không clone được

## Lane D — 色でたどる戦争の記録 (WWII ảnh thật AI tô màu, ✅ ĐÃ DUYỆT 2026-09-10, đã bàn giao)
- Kênh mẫu: 色でたどる戦争の記録 `UCaj1dslbibbHEnOAOh0tyYw` — 15 ngày tuổi, trend 1,57
- `docs/LANE_D_HANDOFF.md` — bàn giao đầy đủ 14 mục, đã copy sang `h2dev/docs/laneD_from_research/`
- **Pipeline hình ảnh thứ 3** (khác Lane A clip stock / Lane C manga AI): ảnh chiến tranh THẬT được AI
  tô màu lại — bắt buộc ảnh có nguồn thật, KHÔNG sinh được bằng AI từ đầu (kênh lịch sử không bịa ảnh).
- **Đã điều tra thật 6 nguồn ảnh tư liệu** (không suy diễn — đọc trang, xác nhận điều khoản): PICRYL/
  GetArchive (NARA, miễn phí), 沖縄県公文書館 (miễn phí, 22.131 ảnh Okinawa), LOC (miễn phí, Manzanar),
  NDL Digital Collection (miễn phí, ~336k tư liệu Nhật hết hạn bản quyền), 昭和館 (miễn phí xem, cần
  xin phép để dùng), Getty/AP/Kyodo/Mainichi (có phí, dự phòng cuối). Xem §7 file handoff.
- Bước AI tô màu ảnh **CHƯA thử nghiệm lần nào** — rủi ro kỹ thuật lớn nhất, phải thử trước khi cam kết
  lịch sản xuất.

## Lane P — 「Nhật đúng · Trung Quốc sai」 phim trường tranh luận 海外の反応 (✅ ANH DUYỆT 2026-10-07, đã bàn giao)
- Kênh mẫu: おもてなしJAPAN `UCpz9rHmxYJiTNhMZUrr_wEw` (19 video, trung vị 549k). Anh chốt: mọi tập khen Nhật, chê Trung Quốc.
- Hồ sơ: `docs/LANE_P_HANDOFF.md` (bản sao của `h2dev\FlowHandoff_local\results\laneP_from_research_2026-10-07\HO_SO_BAN_GIAO_LANE_P.md`),
  phiếu `h2dev\FlowHandoff_local\shared\GIAO_VIEC_LANE_P_2026-10-07.md`, data `data/omotenashi_japan/`, báo cáo `docs/OMOTENASHI_JAPAN_CHANNEL_REPORT.html`.
- **Ranh giới đã khoá:** chê chính quyền/chính sách/doanh nghiệp TQ, không chê dân tộc; show hư cấu 『世界の天秤』, không tên đài thật;
  không bịa câu cho người có tên thật; không dùng mặt/clip người thật đóng vai. Kênh mẫu vi phạm cả 4 (comment đã bắt).
- Hook H02 + K27 (K27 thêm vào HOOK_LIBRARY 07/10). Kho đề tài 8 tập ở hồ sơ §12; tập 1–3 đã có `series_ctx.txt` đủ [Dn] trong `mau\`.

## Housekeeping (2026-09-10)
- User đã xoá hết tab tự động (TRENDING/TRD_*) trên Sheet, chỉ giữ GMAIL/NOTE gốc.
- **Đã tạm dừng** Windows Scheduled Task `YouTubeTrendHunter` — không tự tạo lại tab. Bật lại:
  `Enable-ScheduledTask -TaskName YouTubeTrendHunter`.
- Từ nay báo cáo curation/chọn kênh gửi bằng **Artifact HTML** (theo khung ở `RESEARCH_PLAYBOOK.md`
  §2 Bước 6), KHÔNG đẩy lên Sheet nhiều tab.
- **Không tự ý mở/tắt Chrome profile của user** (`VEO3_PROFILE`, `GROK_PROFILE`...) — luôn xin phép
  trước, kể cả khi chỉ để thử nghiệm (đã có sự cố tắt nhầm profile đang dùng lúc probe heatmap).

## VIDEO HUNT V2 (2026-09-22, shadow mode)
- Kế hoạch + mapping: `IMPLEMENTATION_PLAN.md`; guide gốc `VIDEO_HUNT_V2_CLAUDE_IMPLEMENTATION_GUIDE.md`.
- Code: `src/hunt_v2/` (mỗi gate 1 file). Chạy SAU đường cũ trong `run_video_hunt.py`; cờ ở
  `config/video_hunt.yaml` khối `video_hunt_v2` (`enabled`/`shadow_mode`/từng gate), threshold ở
  `config/hunt_rules.yaml`, model ở `config/models.yaml`, hồ sơ lane ở `lanes/<lane>/` (KHÔNG regenerate).
- **`shadow_mode: true`** → tab `RESEARCH` vẫn nhận pick CŨ; V2 chỉ ghi `TRD_HUNT_AUDIT` + `runs/<ngày>/<lane>/`
  + `logs/llm_*.jsonl`. Bật production = đổi `shadow_mode: false` (chỉ khi Top 2 được accept ≥80%).
- Model đã verify: gemini-3.8-flash qua ramclouds (BẮT BUỘC stream + User-Agent, key `RAMCLOUDS_API_KEY`
  khác `LLM_API_KEY` cũ — key cũ "no access" 3.8), ns24 dự phòng, Sol qua hhtechapi.net, opportunity
  qua `claude -p --model sonnet` (gói Claude Code, không tốn API).
- Cột `HUMAN_DECISION`/`REJECT_REASON` trên `TRD_HUNT_AUDIT` là user gõ tay — tool CHỈ ĐỌC
  (`src/hunt_v2/feedback.py --sync/--propose/--apply`). Không bao giờ update dòng audit.
- Test offline 0 tiền: `py -3.13 -X utf8 -m pytest tests -q` (47 case, gồm regression lỗi owner đã bắt).

## NEWS RADAR — tin nóng/viral Nhật hằng ngày cho lane Q (anh chốt 17/10/2026: chỉ Nhật · mọi thể loại · B · lane Q)
- Kế hoạch: `plans/261017-1030-news-radar/` · code `src/news_radar/` (parsers/collectors/store/cluster/supply/heat/evidence/brief)
  · CLI `src/run_news_radar.py` · cấu hình `config/news_radar.yaml` · gate LLM `news_cluster`/`news_brief` trong `config/models.yaml`.
- Nguồn keyless đã probe 17/10 (HTTP 200): Google Trends RSS `?geo=JP` (pytrends chết nhưng RSS sống), Google News RSS,
  Yahoo!ニュース access ranking (総合 + domestic), X trends qua trends24.in/getdaytrends (X trực tiếp cần login), YouTube InnerTube
  `window=today` đo CUNG. NHK RSS 301, Reddit 403, `/feed/trending` HTML không có videoRenderer → bỏ.
- Điểm: `final = heat × velocity × gap × giật_gân`; gap ∈ [0.5, 1.5] (bão hoà chỉ hạ, không giết tin lớn — 片山さつき 28 video/1,9M view
  vẫn phải đứng #2). Cụm "rác gom"/is_news=false bị loại trước khi chấm. Tiêu đề Yahoo dài → `short_query` (InnerTube trả 0 với tiêu đề 40 ký tự).
- Đầu ra: `runs/news_radar/<ngày>/<ngày>.md|json` + `packs/`; `--handoff` chép sang `E:\CLAUDE\YOUTUBE\MG_STUDIO\lanes\q\NEWS_RADAR\<ngày>.md`
  và thay khối cùng ngày trong `BAN_GIAO_TRENDING.md`. KHÔNG ghi Google Sheet.
- Lệnh: `py -3.13 -X utf8 src/run_news_radar.py --collect` (mỗi 45 phút) · `--brief --handoff [--hooks]` (07/12/19h) · `--loop 45` gộp cả hai.
  Test tay luôn `--dry-run`. Offline: `py -3.13 -X utf8 -m pytest tests -q` (12 case news_radar trên fixtures thật).
- Bẫy đã trả giá 17/10: ramclouds SSE không khai charset → requests decode ISO-8859-1 → JSON tiếng Nhật nát (đã ép UTF-8 trong
  `hunt_v2/llm_transport.py`, ảnh hưởng cả hunt_v2); 150 keyword → output 7,5k token bị cụt ở max_tokens 8k (giờ 100 kw + 16k);
  cache key LlmClient không chứa prompt → sửa prompt phải gắn hash prompt vào `ids`.
- Heredoc bash trên máy này nuốt `\\` → ghi file có đường dẫn Windows/regex bằng Write/Edit, đừng dùng `cat <<EOF`/`py - <<EOF`.

