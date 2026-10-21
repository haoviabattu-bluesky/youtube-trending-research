# YÊU CẦU TỪ DỰ ÁN h2dev — ĐỔI VAI NGHIÊN CỨU KÊNH (Phương án A)

> Người gửi: `E:\CLAUDE\YOUTUBE\h2dev` (tab Lane I `sengoku-uragawa`) · Ngày 2026-09-23.
> Đơn này **tự chứa** — đọc hết file là làm được, không cần hỏi lại bên h2dev.
> Làm theo đúng thứ tự mục 3 → mục 4 → checklist mục 6. Mục 1 là bằng chứng, đọc để hiểu vì sao.

---

## 1. KẾT LUẬN ĐIỀU TRA — KHÔNG PHẢI LỖI GEMINI

Bên h2dev nghi "dùng Gemini nên phân tích kém" nên đã soi lại toàn bộ đường dữ liệu của kênh
どっこい日本史 (`UCxXV78OIGchz13GAA7RGbEQ`) trong ngày 2026-09-23. Kết quả: **6/6 lỗi nằm ở DỮ LIỆU
ĐƯA VÀO và ở CÔNG CỤ, không lỗi nào do model đọc sai.**

| Lỗi | Nguyên nhân thật | Đổi model có cứu? |
|---|---|---|
| Chỉ phân tích 8/21 video của kênh | tham số `--n-select` mặc định 10 | Không |
| Tiêu đề đem đi phân tích là **tiếng Anh** | `yt-dlp` trả bản YouTube TỰ DỊCH theo ngôn ngữ giao diện | Không |
| Mục "Thumbnail patterns" trống | công cụ **không gửi ảnh** cho model | Không |
| Thiếu `channel_keywords` | hàm gom tag không gọi hàm lấy channel keywords | Không |
| Trích sai kanji: 今川**吉本** (đúng 義元), 教科書には**乗**らない (đúng 載らない), こ宵いも (đúng 今宵も) | nguồn là **phụ đề tự động**, YouTube nghe nhầm | Không |
| `data\channel_analysis_どっこい日本史.json`: 6 khối phân tích **rỗng**, `channel_age_days=4`, `upload_frequency_per_week=35.0` | pipeline bên này **không điền field**; 2 con số kia sai so với chính `publish_date` nằm trong file | Không |

Ngược lại, phần model thật sự phải suy nghĩ thì làm tốt: 7 quy tắc viết bài, cấu trúc 5 hồi, công
thức CTA 4 bước — đều kèm trích dẫn thật. Ở mục thumbnail nó còn **tự khai "không đủ dữ liệu" thay
vì bịa** — đó là hành vi đúng, đáng giữ.

> **Luật rút ra (áp cho cả hai bên):** mỗi con số trong báo cáo phải **tra ngược được về dữ liệu
> thô**. `channel_age_days=4` nằm cùng file với 20 `publish_date` trải 154 ngày — chỉ cần một phép
> trừ là lộ. Không có phép kiểm thì đổi model bao nhiêu lần cũng vậy.

---

## 2. ĐỔI VAI TỪ HÔM NAY

| Việc | Ai làm |
|---|---|
| Quét ngách, chấm outlier, tách kênh ăn may vs kênh có công thức | **TRENDING-RESEARCH** |
| Đo thumbnail DNA của kênh mẫu (`lanes\<lane>\thumb_dna.json`) | **TRENDING-RESEARCH** |
| Liệt kê TOÀN BỘ đề tài kênh mẫu đã làm + view từng cái | **TRENDING-RESEARCH** |
| Viết `CHANNEL_DNA` (hook, cấu trúc, CTA, giọng kể, rules viết bài) | **h2dev** — đã tự chạy được |
| Đo char-rate, độ dài tiêu đề, ngưỡng gate | **h2dev** |

Lý do bỏ phần `CHANNEL_DNA` khỏi bên này: h2dev có `pipeline\channel_analyzer.py` chạy **195 giây
cho cả kênh 21 video** (đo thật hôm nay) — tự crawl, lấy transcript, tổng hợp, QC đủ 11 đề mục.
Hai bên cùng làm một việc thì chỉ đẻ ra hai bản khác nhau, không bản nào là nguồn chân lý.

---

## 3. NĂM VIỆC PHẢI SỬA (theo thứ tự)

### 3.1 — Cấm giao file có khối rỗng
Hiện trạng `data\channel_analysis_どっこい日本史.json`: `topic_analysis.winning_topics`,
`title_analysis.common_patterns`, `title_analysis.title_formulas`,
`thumbnail_analysis.common_patterns`, `positioning.content_pillars`,
`positioning.audience_problems` đều là `[]`.

Phải thành: **field nào không đo được thì XOÁ HẲN khỏi file**, đừng để mảng rỗng. Bên nhận không
phân biệt được "đã đo và không có gì" với "chưa bao giờ đo", mà mảng rỗng lại làm cả file trông như
đã hoàn chỉnh.

### 3.2 — Sửa hai con số thời gian, và hạ `overall_confidence` cho đúng
- `channel_age_days: 4` và `upload_frequency_per_week: 35.0` đều **sai**. Tính lại từ chính
  `videos[].publish_date` trong file: sớm nhất 2026-04-10, muộn nhất 2026-09-11 → **154 ngày**;
  21 video → **0,95 video/tuần**.
- `data_quality.videos_deep_analyzed: 2` trên 20 video mà `overall_confidence: "high"`.
  Quy ước mới: deep-analyze **dưới 70 %** số video thì `overall_confidence` **không được** là `high`.

### 3.3 — Tiêu đề phải là TIÊU ĐỀ GỐC, không phải bản YouTube tự dịch
Mọi phân tích tiêu đề (công thức, độ dài, từ khoá) làm trên bản dịch là **vô nghĩa**. Cách lấy bản
gốc bằng `yt-dlp`, kèm đúng cái bẫy đã dính:

```python
# LƯỢT 1: lấy view_count, duration (KHÔNG đặt lang)
opts = {"quiet": True, "extract_flat": True, "playlistend": 500}
# LƯỢT 2: lấy TIÊU ĐỀ GỐC
opts_native = dict(opts, extractor_args={"youtube": {"lang": ["ja"]}})
# BẪY: lượt có lang=ja trả view_count = None cho MỌI video.
#   → phải GHÉP theo video id (title lấy lượt 2, số liệu lấy lượt 1), KHÔNG thay hẳn lượt 1.
```

Kiểm nhanh file cũ có dính không: kênh Nhật mà `videos[].title` bắt đầu bằng `[` ASCII thay vì `【`
thì đang là bản dịch.

(Bên h2dev đã vá y hệt cách này vào `pipeline\channel_analyzer.py` bằng cờ `--meta-lang ja`, có thể
đọc tham khảo.)

### 3.4 — Cấm trích nguyên văn từ phụ đề tự động
Câu khẩu hiệu thương hiệu của kênh này, bản **đúng**:

> 「さあ、教科書に**載**らない歴史の裏側へ。**今宵**も皆様をお連れしましょう。」

Phụ đề tự động cho ra `教科書には乗らない` / `こ宵いも` / `今川吉本`. Quy ước mới: mọi trích dẫn rút từ
phụ đề tự động phải gắn nhãn `[auto-caption, chưa kiểm]`. Câu nào bên h2dev sẽ dùng làm **chuỗi cố
định** (khẩu hiệu, CTA, tên riêng, địa danh) thì phải đối chiếu với **mô tả video / bình luận ghim /
tiêu đề** rồi gõ lại kanji đúng trước khi giao.

### 3.5 — Sửa `lanes\sengoku-uragawa\lane_profile.yaml` (đang SAI)
`label` hiện ghi `chibi manga`. **Sai.** h2dev đã tải đủ **21/21 thumbnail thật** của kênh mẫu và
soi bằng mắt: đó là **manga seinen / anime lịch sử nghiêm túc** — mặt người lớn tỉ lệ thật, nếp
nhăn, lông mày rậm, nét viền dày, cel-shading đậm, biểu cảm nặng (trừng mắt, toát mồ hôi, cam chịu).
Không hề có đầu to thân nhỏ, không hề dễ thương.

- Ảnh gốc đối chiếu: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\_raw\thumbs\`
- Số đo đầy đủ: `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\dokkoi-nihonshi\THUMBNAIL_PATTERNS.md`

Sửa luôn `wanted_topics`: mục `織田信長・豊臣秀吉・徳川家康の裏話` — trong đó **徳川家康 kênh mẫu ĐÃ làm
rồi** (213k view). Danh sách 21 đề tài đã bị đốt ở mục 4.3.

---

## 4. KHUÔN GIAO HÀNG MỚI — giao đúng ba thứ

### 4.1 Hồ sơ kênh ứng viên (thế mạnh của bên này, giữ nguyên)
`subs · median_views · ch_mult · ch_age_days · upload/tuần · view/sub · verdict`.
Mỗi con số phải tra ngược được về dữ liệu thô trong `data\trending.db`.

### 4.2 `thumb_dna.json` đo thật
Đúng khuôn đang làm ở `lanes\teinengo-tanoshimi\thumb_dna.json` — **h2dev đánh giá đây là phần làm
tốt nhất của bên này**: có `measured: true`, `seen_in: "19/19"`, `measured_px`, tỉ lệ theo chiều cao
khung. Đó chính là thứ `CHANNEL_DNA` không bao giờ làm được (model không được xem ảnh).
Giữ nguyên cách này và làm cho `lanes\sengoku-uragawa\` (hiện chưa có).
Bắt buộc: `measured: false` hoặc thiếu `seen_in` thì **đừng giao**.

### 4.3 Danh sách đề tài kênh mẫu ĐÃ ĐỐT — toàn bộ kênh, không phải top 8
Mẫu chuẩn, どっこい日本史 (21/21 video, h2dev đo 2026-09-23):

| Nhóm | View | Nhân vật |
|---|---|---|
| Bứt phá | 771k–142k | 前田慶次 · 柴田勝家 (×2) · 徳川家康 · 武田勝頼 |
| Khá | 91k–58k | 今川義元 · 千利休 · 小早川秀秋 |
| Thường | 27k–15k | 今川氏真 · 明智光秀 · お市の方 · 前田利家 · 石田三成 |
| **Chết** | 10k–3,3k | 春日局 · 豊臣秀長 · 黒田官兵衛 · 近藤勇 · 松永久秀 · ジョン万次郎 · 寧々 · 備中高松城 |

Kèm kết luận rút ra được — đây mới là giá trị, không phải bảng thô:
- **Tử huyệt: nhân vật nữ + ngoài thời Chiến quốc** (春日局 10k · 寧々 4,4k · 近藤勇 6,4k ·
  ジョン万次郎 5,1k), trong khi võ tướng hệ 織田 ăn 142k–771k.
- **Còn trống hoàn toàn**: 織田信長 / 豊臣秀吉 / 伊達政宗 / 真田幸村 / 上杉謙信 / 武田信玄.
- **Thumbnail không quyết định view**: video 771k và video 27k dùng template giống hệt nhau — chênh
  lệch nằm ở độ nổi tiếng của nhân vật.

### 4.4 KHÔNG cần giao nữa
`CHANNEL_DNA`, hook formula, cấu trúc kịch bản, CTA pattern, giọng kể, rules viết bài.

---

## 5. CỔNG NGHIỆM THU — h2dev TRẢ LẠI hồ sơ nếu dính một trong năm điều

1. Có field nào là mảng rỗng `[]` hoặc `null` mà vẫn nằm trong file giao.
2. Kênh không nói tiếng Anh nhưng `videos[].title` lại là tiếng Anh (= bản dịch).
3. Có con số thời gian (`channel_age_days`, `upload_frequency_per_week`) không tra ngược được từ
   `publish_date` trong chính file đó.
4. Có trích dẫn nguyên văn không ghi nguồn, hoặc lấy từ phụ đề tự động mà không gắn nhãn.
5. `thumb_dna.json` có `measured: false`, hoặc thiếu `seen_in` / `measured_px`.

Trả lại thì h2dev gửi kèm danh sách cụ thể và **không tự sửa hộ** — tự sửa hộ thì lần sau sai y hệt.

---

## 6. CHECKLIST VIỆC CẦN LÀM NGAY

- [ ] Sửa `lanes\sengoku-uragawa\lane_profile.yaml`: `chibi manga` → manga seinen (mục 3.5); bỏ 徳川家康 khỏi `wanted_topics`.
- [ ] Đo `thumb_dna.json` cho `lanes\sengoku-uragawa\` theo khuôn `teinengo-tanoshimi` (mục 4.2).
- [ ] Rà mọi `data\channel_analysis_*.json` đã giao: xoá khối rỗng, tính lại 2 số thời gian, hạ `overall_confidence` (mục 3.1 + 3.2).
- [ ] Vá chỗ crawl tiêu đề: thêm lượt `lang=<mã ngôn ngữ kênh>` rồi ghép theo video id (mục 3.3).
- [ ] Viết báo cáo trả lời vào `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_TRENDING_2026-09-23.md` (nêu rõ mục nào đã sửa, mục nào không đồng ý và vì sao).
