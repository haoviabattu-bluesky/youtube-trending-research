# CLAUDE.md — YouTube Trend & Outlier Hunter

## 📖 BẮT BUỘC ĐỌC TRƯỚC MỌI TASK NGHIÊN CỨU/TÌM KIẾM
`docs/RESEARCH_PLAYBOOK.md` — quy trình 7 bước dùng chung cho MỌI loại tìm kiếm (tìm ngách mới,
tìm kênh để clone/reup, tìm đề tài trong ngách đã chọn). Đúc kết từ Lane A + Lane C, có bảng
"cạm bẫy đã gặp" — đọc trước để không lặp lại sai sót đã trả giá thật (kênh ăn may tưởng mạnh,
báo cáo quá nhiều tab, link ẩn không bấm được, bàn giao khi chưa được duyệt...).

## ⛔ RANH GIỚI 2 DỰ ÁN (user chốt 2026-09-10)
Dự án này **CHỈ NGHIÊN CỨU**. Việc **làm video thuộc dự án `E:\CLAUDE\YOUTUBE\h2dev`**.
Ở đây: quét ngách, chấm điểm outlier, bóc công thức đối thủ, dò khoảng trống đề tài,
chuẩn bị tư liệu. KHÔNG viết kịch bản, KHÔNG dựng video, KHÔNG sinh ảnh sản xuất.
Bàn giao qua `docs/LANE_A_HANDOFF.md` + `docs/PROMPT_GUI_SANG_h2dev.txt`
(đã copy sang `h2dev/docs/laneA_from_research/`).

## Role
Xây và vận hành tool quét YouTube hằng ngày để tìm **video bứt phá** và **kênh mới nhiều view** trong ngách faceless, chấm điểm outlier, báo cáo lên Google Sheet.

## Workflows
- Skill quy tắc (BẮT BUỘC): `@C:\Users\admin\.claude\skills\quy_tac_tao_tool.md`
- Nền nghiên cứu YouTube: `@C:\Users\admin\.claude\skills\youtube_research_ext.md` — §0 đường KHÔNG extension (transcript + comment thuần Python), §7 cơ chế InnerTube
- Lịch chạy VPS (Phase 6): `@C:\Users\admin\.claude\skills\daily-batch-vps-scheduler.md`
- Ghi Google Sheet: `@C:\Users\admin\.claude\skills\gsheet-pipeline-builder.md`, `@C:\Users\admin\.claude\skills\mcp_google.md`
- Dùng kết quả: `youtube-script`, `youtube-series-builder`, `youtube-thumbnail`, `youtube-image-prompts`

Kế hoạch hiện tại: `plans/260909-1611-youtube-trend-outlier-hunter/`

## ⛔ QUY TẮC TUYỆT ĐỐI — GOOGLE SHEET
Sheet `1xu4iNudIPanWrUxlTODqIySGf9YxLy7rpTq9OtXDMOU` (tên "YOUTUBE") **đã có dữ liệu thật** ở tab `GMAIL` (974 dòng) và `NOTE`.

- **CHỈ được đụng** tab `TRENDING` và tab có prefix `TRD_`. Whitelist hard-code trong `src/sheets.py`.
- **CẤM** mọi thao tác xoá: `delete_rows`, `delete_dimension`, `clear`, `batch_clear`, ghi đè hàng loạt.
- Chỉ `append_rows` và `update` đúng range đã tính.
- Trước/sau mỗi lần chạy: log số dòng của `GMAIL` và `NOTE` — phải không đổi.

## Modularization
- File code ≤ 200 dòng
- Kebab-case / snake_case dài, mô tả rõ
- Check module có sẵn trong `src/` trước khi tạo file mới

## Stack
- Python 3.13 (`py -3.13 -X utf8` — bắt buộc `-X utf8` vì title tiếng Nhật)
- Discovery: InnerTube `youtubei/v1/search` (keyless, 0 quota)
- Enrich: YouTube Data API v3 (`videos.list`, `channels.list`, `playlistItems.list`)
- Store: SQLite `data/trending.db` (nguồn chân lý)
- Report: `gspread` + service account
- Deep-dive: `youtube-transcript-api`, `youtube-comment-downloader`

## Credentials
- `config/.env`: `YOUTUBE_API_KEY`, `SHEET_ID`, `GOOGLE_SHEETS_KEY=d:/CLAUDE/credentials/google-sheets-key.json`
- Service account: `claude-sheets-reader@fifth-glider-495702-b4.iam.gserviceaccount.com` (đã có quyền Editor)
- `.env` nằm trong `.gitignore` — KHÔNG commit

## Commands
```bash
py -3.13 -X utf8 src/run_probe.py --niche jp_senior,jp_satori --limit-kw 60 --out data/probe.csv   # Phase 1
py -3.13 -X utf8 src/run_daily.py --push-sheet                                                      # Phase 3+
```

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

## Housekeeping (2026-09-10)
- User đã xoá hết tab tự động (TRENDING/TRD_*) trên Sheet, chỉ giữ GMAIL/NOTE gốc.
- **Đã tạm dừng** Windows Scheduled Task `YouTubeTrendHunter` — không tự tạo lại tab. Bật lại:
  `Enable-ScheduledTask -TaskName YouTubeTrendHunter`.
- Từ nay báo cáo curation/chọn kênh gửi bằng **Artifact HTML** (theo khung ở `RESEARCH_PLAYBOOK.md`
  §2 Bước 6), KHÔNG đẩy lên Sheet nhiều tab.
- **Không tự ý mở/tắt Chrome profile của user** (`VEO3_PROFILE`, `GROK_PROFILE`...) — luôn xin phép
  trước, kể cả khi chỉ để thử nghiệm (đã có sự cố tắt nhầm profile đang dùng lúc probe heatmap).

## Git conventions
- Commit theo từng phase, không gộp
- `feat(phase-N): ...` / `fix: ...` / `docs: ...`
