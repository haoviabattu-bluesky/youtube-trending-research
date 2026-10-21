# HỒ SƠ GIAO VIỆC — Kênh シニアの人生これから (dịch: "Đời sau nghỉ hưu của người cao tuổi bắt đầu từ đây") — 2026-09-28

Trạng thái: **ĐÃ GÁN LANE N, đã bàn giao h2dev — chưa tạo kênh thật (giai đoạn 2 chờ user duyệt).**

## 1. Kênh gốc
- https://www.youtube.com/@senior_korekara · ID `UCL8PFGotC_jY_UbzfRTnnng`
- 3.410 sub · 64 video · 1.703.422 view tổng (đo 28/09/2026) · tạo 17/07/2026 (~73 ngày)
- Manga ảnh AI 100% + slideshow tĩnh + narration **NGƯỜI THẬT** (F0 median 122,1 Hz, jitter 17,56%,
  F0 p10→p90 80,8→210,5 Hz ⇒ không phải TTS). Nhân vật cố định: ông hói đeo kính, áo sọc xanh, 60s–70s.
- Chủ đề: đời sống người Nhật 60–70 tuổi SAU nghỉ việc — việc làm, hôn nhân, chuyển đi, viện dưỡng lão,
  tiền, cô đơn. Tần suất 6,1 video/tuần, độ dài điển hình ~16 phút, 6 chương có tên trong description.

## 2. Số liệu then chốt
| Video | View | View/ngày | Tuổi |
|---|---|---|---|
| シルバー人材センターは結局どうなのか？辞めとけって本当？ (Trung tâm nhân lực bạc rốt cuộc thế nào?) | 443.785 | 49.309 | 9d |
| キツくないのに稼げる！？老後におすすめの仕事ランキング7選 (7 việc nhẹ mà kiếm được) | 242.757 | 13.486 | 18d |
| 婚活パーティーで年金目当ての男が大量発生…66歳独身女性の末路 (Bữa tiệc kết hôn toàn đàn ông nhắm lương hưu) | 142.953 | 3.864 | 37d |
| 老後の同窓会で笑い者に。独り身のシニア男が同窓会に参加した末路 (Họp lớp tuổi già, bị cười nhạo) | 109.064 | 2.371 | 46d |
| 老後に軽井沢移住して1年後「もう帰りたい」 (Chuyển lên Karuizawa 1 năm, "muốn về rồi") | 87.031 | 5.802 | 15d |
| 老後の年金別の生活レベル!年金6万円と25万円の格差 (Mức sống theo lương hưu: 6 vạn vs 25 vạn) | 76.880 | 1.538 | 50d |
| 72歳で老人ホームの体験入居へ。3泊4日で初めて知った施設のリアル (Ở thử viện dưỡng lão 3 đêm 4 ngày) | 68.984 | 8.623 | 8d |
| 入居金1億円の高級老人ホームに入った結果 (Viện dưỡng lão cao cấp phí vào 1 oku) | 58.557 | 1.428 | 41d |

Kết luận đề tài: góc **cạm bẫy cụ thể + con số thật** (viện dưỡng lão, lương hưu, việc làm) thắng;
video "điểm danh nghề tốt" (ranking 7選) cũng ăn rất mạnh — VPD 13.486 đứng thứ 2 kênh.
Video tự sự ngôi 1 về **cô đơn / hôn nhân tuổi già** cũng leo đều.

**Chỉ số kênh (28/09/2026):** median view **6.928** · mean 26.615 (**3,84×** median) · `trend_vpd_30d`=**14,61×**
· `ch_mult`=3,84 · hit_rate 23,4% · Top1 chiếm 26,1% / Top3 48,7% (có phụ thuộc video nổ) ·
`trend_vpd_90d`=`null` (kênh mới 73 ngày, không có video nào >90 ngày — KHÔNG báo lỗi).

## 3. Báo cáo + tài liệu
- Báo cáo nguồn: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\SENIOR_KOREKARA_CHANNEL_REPORT.html`
- CHANNEL_DNA.md (K1+K2):
  `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\channel_dna\senior_korekara\CHANNEL_DNA.md`
  (+ `VIDEO_ANALYSIS\*.json` 15 video, `TAG_STATS.json`, `_raw\{segments,meta,thumbs,transcripts.json}`)
- Dữ liệu thô: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\senior_korekara\`
  (channel.json 64 video, transcripts **15/15 THẬT** — phủ ~100% độ dài, via `api+proxy1`,
  thumbs 15/15, comments.json 779 bình luận, hook_records.json 15)
- Hook Library: **15 video đã nạp** `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\hooks.jsonl`,
  `lanes_fit=["senior_korekara"]`. Phân bố: D×5, C×5, A×3, E×2, B×1; điểm 8–10/12.
  Top: H03+K02 (10/12) · H03+H12+K09 (10/12) · H18+H08+K01 (10/12).

## 4. Verdict
ĐƯỢC clone. Nhân vật riêng (KHÔNG dùng ông hói kính + áo sọc xanh, KHÔNG dùng mô-típ
「シルバー人材センター」), giữ: manga ảnh AI + slideshow tĩnh + **narration người thật** (không TTS),
lương hưu/số tiền nêu bằng con số cụ thể ở 0–30s, 6 chương có tên, kết thúc **nghiệm tùng** (2,8%)
chứ không quả báo cay đắng. Ưu tiên định dạng **dạng danh sách N選** cho tập thử đầu tiên
(VPD cao nhất phân khúc content: 13.486).

## 5. Việc còn chờ quyết
- **Chồng ngách:** Lane N chồng một phần Lane J (teinengo-fuufu) ở mảng "đời sau nghỉ hưu" →
  chọn: (a) nâng cấp Lane J bằng DNA này, hay (b) giữ Lane N độc lập chuyên "việc làm + cạm bẫy tuổi 60".
- **Giai đoạn 2 chưa làm:** tạo kênh thật (`mail` / `handle` / tên kênh / avatar / banner) —
  cột C–F + K tab NOTE (Google Sheet) **đã ghi**, các cột giai đoạn 2 (STT, NHẬN KÊNH, MAIL, HANDLE, KÊNH) vẫn để trống.
- **3 tập thử mảng việc làm dạng LIST 7選** (theo video nổ VPD 13.486) — user chưa chốt bắt đầu.
- **Chốt giọng:** thu người thật (như kênh mẫu) hay TTS — user chưa chốt.
