# HỒ SƠ GIAO VIỆC — Kênh 大人の盲点【漫画でわかる人生の裏側】 (dịch: "Điểm mù của người lớn — mặt trái cuộc đời hiểu qua manga") — 2026-09-26

Trạng thái: **ỨNG VIÊN, user đã chọn là 1 trong 2 kênh ưng ý (25/09) — chưa gán LANE/HANDLE, chưa bàn giao h2dev.**

## 1. Kênh gốc
- https://www.youtube.com/@otonanomouten · ID `UCsWLzQF-6knOsQlHYBNtvwg`
- 526 sub · 6 video · 148.242 view tổng (đo 26/09/2026 02:19 UTC) · tập đầu đăng 10/09/2026
- Manga drama cho đàn ông 60–65 vừa nghỉ hưu: mỗi tập = 1 danh sách N選 (việc làm thêm / sở thích / câu cửa miệng)
  kể qua nhân vật cố định 高瀬健一 (64 tuổi, cựu trưởng phòng quỹ tín dụng 信用金庫) + vợ 恵子. Câu chốt mọi tập: 「盲点だった。」 ("Đúng là điểm mù.")

## 2. Số liệu then chốt
| Video | View | View/ngày |
|---|---|---|
| 60代以降でも気楽に働ける人気のアルバイト・パート7選 (7 việc làm thêm người 60+ làm thoải mái) | 92.034 | 5.888 |
| 60代以降でも一人で一生遊べる人気の娯楽・趣味7選 (7 sở thích chơi một mình cả đời) | 26.982 | 2.321 |
| 周りから愛される60代が使う魔法の口癖7選 (7 câu cửa miệng được quý mến) | 11.145 | 2.995 |
| 60代が「楽そう」で選ぶと後悔するアルバイト・パート13選 (13 việc trông nhàn mà hối hận) | 10.442 | 1.210 |
| なぜ定年後も働き続けるシニアが増えたのか？…7つの理由 (vì sao người hưu vẫn đi làm — 7 lý do) | 6.634 | 1.160 |
| 60代の再就職で月5万円を目指すには？…11選 (kiếm 5 vạn/tháng — 11 việc), mới 0,6 ngày | 1.005 | — |

Kết luận đề tài: góc "nên chọn gì + lợi ích cụ thể" thắng góc "cảnh báo tiêu cực" và "giải thích なぜ" 2–5 lần.
Đối thủ cùng thể loại có video 186k–1,14 triệu view đều dùng móc tiết kiệm (安く / ぜんぶ0円 / 1円もかからない) hoặc 最強/神 — kênh này chưa dùng.

## 3. Báo cáo + tài liệu
- **Artifact:** https://claude.ai/artifact/BKu4dtyGMNJVMhU6Ky5Xe4
- Báo cáo nguồn: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\OTONANOMOUTEN_CHANNEL_REPORT.html`
- CHANNEL_DNA.md (tool K1+K2 h2dev, QC 12/11 + bổ sung thumbnail đọc tay + đính chính):
  `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\channel_dna\otonanomouten\CHANNEL_DNA.md`
  (+ `VIDEO_ANALYSIS\*.json` 6 video, `TAG_STATS.json`)
- Dữ liệu thô: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\otonanomouten\` (channel.json, transcripts 6/6, thumbs,
  competitor_thumbs + competitors.json, comments.json, hook_records.json)
- Hook Library: 6 video đã nạp `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\hooks.jsonl` — H02+K06 (10/12), H02+K03, H01+K09/K04,
  H01+H21+K12, H33+K22, H14+H21+K09.

## 4. Verdict
ĐƯỢC clone, có điều kiện: nhân vật riêng (không dùng 高瀬/恵子/「盲点だった」), chỉ làm góc lợi ích + móc tiết kiệm,
18–24 phút với mục xếp hạng đầu trước phút 4, QC tên riêng qua giọng đọc máy + lỗi ảnh AI + chi tiết thực tế.

## 5. Việc còn chờ quyết
- Thể loại chồng lên Lane F (teinengo-real) và Lane G (teinengo-tanoshimi) của h2dev → chọn: (a) nâng cấp F/G bằng DNA này,
  hay (b) mở lane mới chuyên "việc làm thêm tuổi 60".
- Chưa đo khung hình video (số ảnh/cảnh, chuyển cảnh) — làm bằng skill `video-chuyen-canh` nếu cần.
