# CLAUDE.md — YouTube Trend & Outlier Hunter

## ⛔⛔ QUY TẮC NGÔN NGỮ — BẮT BUỘC TUYỆT ĐỐI (user chốt 2026-10-19)
**TẤT CẢ TIẾNG NHẬT PHẢI DỊCH SANG TIẾNG VIỆT.** Áp dụng cho MỌI output của dự án:
báo cáo HTML/artifact, file handoff, tin nhắn chat, bảng số liệu, chú thích, log bàn giao.
- Tiêu đề video Nhật → dịch nghĩa tiếng Việt. Muốn giữ nguyên văn để đối chiếu thì đặt
  **sau** bản dịch, trong ngoặc: `Dân Edo ăn mì soba thế nào? (江戸っ子のそばの食べ方とは)`
- Từ khoá tìm kiếm, tên kênh, tên nhân vật lịch sử → phiên âm/dịch tiếng Việt trước,
  nguyên văn trong ngoặc nếu cần tra cứu.
- Trích dẫn comment/phụ đề tiếng Nhật → dịch hết; giữ nguyên văn chỉ khi có lý do
  chứng minh cụ thể (vd phân tích lỗi ASR nghe sai tên riêng) và phải nêu rõ lý do.
- **CẤM** để tiếng Nhật trần làm nội dung chính của bất kỳ mục nào người dùng đọc.
Quy tắc này thắng mọi thói quen cũ trong repo (kể cả các báo cáo trước đã lỡ để tiếng Nhật).

## 📖 BẮT BUỘC ĐỌC TRƯỚC MỌI TASK NGHIÊN CỨU/TÌM KIẾM
`docs/RESEARCH_PLAYBOOK.md` — quy trình 7 bước dùng chung cho MỌI loại tìm kiếm (tìm ngách mới,
tìm kênh để clone/reup, tìm đề tài trong ngách đã chọn). Đúc kết từ Lane A + Lane C, có bảng
"cạm bẫy đã gặp" — đọc trước để không lặp lại sai sót đã trả giá thật (kênh ăn may tưởng mạnh,
báo cáo quá nhiều tab, link ẩn không bấm được, bàn giao khi chưa được duyệt...).

## 🎣 HOOK TRƯỚC TIÊN (user chốt 2026-09-23)
Research ra video nào → đọc hook 0–90s trước, phân loại, nạp kho `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\`
(skill `youtube-hook-research`; xem RESEARCH_PLAYBOOK §-2). Từ 21/10 chạy `src/hook_auto.py ID ... --lane <lane>`
(model ngoài chấm + nạp kho, in 1 dòng/video); chỉ đọc tay `src/hook_fetch.py` cho 1–2 video cần đào sâu.

## ⛔ ĐỀ TÀI PHẢI SÁT ĐỜI SỐNG NGƯỜI DÂN (user chốt 2026-10-08, sau khi chê kho đề tài lane Q)
Đề tài đề xuất cho MỌI lane phải là thứ người dân thường chạm tới và thích xem: đồ ăn (ホタテ, sushi, gạo),
du lịch/khách sạn/phố đông, phim, anime, ca sĩ, hàng hoá, giá cả, thương hiệu ai cũng biết.
**CẤM đề xuất làm tập chính** các đề tài chính trị/ngoại giao/quân sự/công nghiệp xa đời sống: nghị quyết LHQ,
lá phiếu năm 1995/2005, điều khoản hiệp ước, danh sách kiểm soát xuất khẩu, tàu chiến, đất hiếm, bán dẫn.
Chúng chỉ được làm chi tiết phụ bên trong một tập đời sống. Tự kiểm trước khi đề xuất: "bà nội trợ / ông về hưu
xem tiêu đề có hiểu ngay và muốn bấm không?" — không thì bỏ.
Lane Q cụ thể: khung bắt buộc **TQ chê/cấm/tẩy chay một thứ của Nhật, tưởng Nhật sẽ thiệt → Nhật làm tốt
→ quay xe, bên thiệt là TQ** (mẫu đúng: tập 3 hãng bay TQ lỗ). Kho đề tài: `E:\CLAUDE\YOUTUBE\MG_STUDIO\lanes\q\NGHIEN_CUU.md` §12.

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
- **Tab lane h2dev (chỉ ĐỌC tag/đề tài) đổi tên 2026-09-24 theo quy ước `{Lane}-{tên kênh}`:** `A-shinya_shiryoshitsu` ·
  `Satori-Lopezzapa68` · `E-70dai-kenko` · `F-teinengo-real` · `G-teinengo-tanoshimi` (kokoro-kazoku/sengoku-uragawa/
  teinengo-fuufu chưa đổi; tab `irogatatarukioku` không còn trên sheet lúc kiểm 24/09). Tên tab khai ở
  `config/video_hunt.yaml` `lanes.<x>.tab`; key lane + `col` cột RESEARCH + thư mục `lanes/<kênh>/` GIỮ tên kênh không tiền tố.
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

## ⛔ TIẾT KIỆM QUOTA CLAUDE (anh duyệt 2026-10-21)
Đo 07–21/10: subagent Opus 48% · ngữ cảnh nền 23% · dữ liệu thô in vào chat 15% · Claude tự viết file dài 12%;
75% chi phí rơi vào lượt có ngữ cảnh >150k. Luật:
- **Đọc nhiều / viết nháp → model ngoài trước** (gate `ext_*` ở `config/models.yaml`, cửa chung `src/ext_llm.py`; từ 21/10 chạy chính Haiku/Sonnet 5.5 qua provider `claude_lite` = `claude -p` gọn (--tools "" --strict-mcp-config --safe-mode --system-prompt-file, nền ~0,8k token), ns24 dự phòng):
  dịch + phân loại tiêu đề `src/title_classify.py` · hook `src/hook_auto.py` (thay đọc tay hook_fetch) ·
  chủ đề bình luận theo tổng like `src/comment_topics.py` · tìm + trích số [Dn] `src/source_extract.py`
  (câu nguyên văn phải khớp trang đã tải, không khớp → `bi_loai`) · nháp hồ sơ/báo cáo `src/draft_writer.py` (Sol, tự soát [Dn]/số lạ/tiếng Nhật trần).
  Claude chỉ: quyết, soát cảnh báo, kiểm ngẫu nhiên 2–3 [Dn] bằng cách mở `nguon/*.txt`, nói chuyện với anh.
- **Subagent:** chỉ khi thật cần. Thu tư liệu 1 vụ → agent `thu-tu-lieu` (Haiku, effort thấp); soạn hồ sơ 1 tập → `soan-tu-lieu-tap` (Sonnet) — định nghĩa ở `.claude/agents/`. Việc khác luôn truyền `model: "sonnet"`/`"haiku"`; `.claude/settings.json` đặt CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5-5 làm mặc định dự phòng.
- **Script in ≤40 dòng**, dữ liệu đủ ghi file; cấm `cat` cả transcript/JSON lớn vào chat.
- **Mỗi việc một phiên**; giao xong nhắc anh `/clear`. Xem tốn bao nhiêu ở model ngoài: `py -3.13 -X utf8 src/ext_llm.py [YYYY-MM-DD]`.

## Chi tiết dự án (đã tách sang `docs/CLAUDE_CHI_TIET.md` — đọc đúng mục khi cần)
Mục ở đó: Sự thật đã verify (InnerTube params, ngưỡng ch_mult/breakout, bẫy Sheet 60 read/phút, ShrinkGuard) ·
Thiết kế báo cáo TRENDING · Lane A / C / D / P đã bàn giao · Housekeeping · VIDEO HUNT V2 · NEWS RADAR.
Tóm tắt phải nhớ: test tay luôn `--dry-run`; mọi lời gọi Sheet bọc `gapi.retry_api`; báo cáo curation bằng Artifact HTML,
không Sheet nhiều tab; scheduled task `YouTubeTrendHunter` đang tạm dừng; KHÔNG tự mở/tắt Chrome profile của anh;
pytrends chết; retention đối thủ không lấy được; luôn kiểm `trend` chứ không chỉ `ch_mult`.

## Git conventions
- Commit theo từng phase, không gộp
- `feat(phase-N): ...` / `fix: ...` / `docs: ...`
