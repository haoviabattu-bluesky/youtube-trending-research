# HỒ SƠ BÀN GIAO — LANE P 「Nhật đúng · Trung Quốc sai」 (phim trường tranh luận, dòng 海外の反応)

Từ: TRENDING-RESEARCH · Ngày: 2026-10-07 · **Anh duyệt mở Lane P ngày 2026-10-07**, chữ cái lane do anh đặt.
Định hướng anh chốt: **mọi tập theo mô típ khen Nhật, chê Trung Quốc**. Đề tài phương Tây/khác để sau.
Kênh mẫu: **おもてなしJAPAN** (Omotenashi Japan, "Nhật Bản hiếu khách") · https://www.youtube.com/channel/UCpz9rHmxYJiTNhMZUrr_wEw · `UCpz9rHmxYJiTNhMZUrr_wEw`
Báo cáo có ảnh cho anh: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneP_from_research_2026-10-07\BAO_CAO_KENH_MAU.html` (bản online https://claude.ai/artifact/JJZdV63n2CYbs5jQBECpzX)

Ranh giới (đơn `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\YEU_CAU_TU_H2DEV_2026-09-23.md`): `CHANNEL_DNA`, profile, gate, SOP là của h2dev. Gói này giao **bằng chứng + đề xuất cụ thể**. Mọi câu trích từ phụ đề tự động gắn `[auto-caption, chưa kiểm]`. Phụ đề tự động của kênh nghe sai đều đặn 「おもてなし」 thành 「表なし」, tên người cũng sai; trong hồ sơ em sửa lại trong ngoặc vuông.

---

## 0. Đọc theo thứ tự

| # | Mục | Vì sao đọc |
|---|---|---|
| 1 | §1 Lane P là gì, số liệu kênh mẫu | Hiểu vì sao chọn Trung Quốc |
| 2 | **§2 Luật nội dung (bắt buộc)** | Ranh giới "chê Trung Quốc" để không mất kiếm tiền/không bị gậy |
| 3 | §3 Khung tập 35 phút + beat sheet video Suzuki | Xương sống kịch bản |
| 4 | §4 Kinh thánh phim trường (show, 3 vai, nghi thức) | Thứ thay cho footage người thật của kênh mẫu |
| 5 | §5 Hook (H1–H4) | Khuôn + ví dụ thật + checklist |
| 6 | §6 Tiêu đề · §7 Thumbnail (đo pixel) · §8 Mô tả | Gói đăng |
| 7 | §9 Hình + dựng · §10 Giọng | Pipeline hình/giọng |
| 8 | §11 Nguồn tài liệu + quy trình dựng `series_ctx.txt` | Cách lấy [Dn] |
| 9 | §12 Kho đề tài 8 tập ưu tiên (+ 3 tập mẫu đã soạn sẵn hồ sơ trong `mau\`) | Làm tập nào trước |
| 10 | §13 Bình luận khán giả · §14 QC · §15 Dữ liệu · §16 Rủi ro · §17 Việc của h2dev | |

---

## 1. Lane P là gì

**Một câu:** mỗi tập dựng một chương trình tranh luận quốc tế HƯ CẤU, trong đó phía Trung Quốc chê/coi thường Nhật bằng một sự kiện THẬT, rồi một chuyên gia phương Tây lần lượt lật lại bằng dữ kiện thật, cuối cùng kết quả N năm sau chứng minh Nhật đúng.

### 1.1 Kênh mẫu (đo 07/10/2026 qua YouTube Data API, `data\channel.json`)

- 19 video, 21.500 sub, 12,5 triệu view. Kênh tạo 18/02/2026, video đầu 03/03/2026.
- Trung vị 12 video ≥7 ngày tuổi: **549.417 view/video** (gấp 26,9 lần sub). Trend 1,56. Top 1 chiếm 14% tổng view (không phải kênh 1 hit).
- Đà: 3 video tháng 9: Suzuki **92.760 view/ngày** (1,04M sau 11 ngày), cá voi 78.290/ngày, Hàn Quốc 15.993/ngày.
- 13/19 video nhắm Trung Quốc, 4 nhắm Hàn, 2 khác.

| Video (Trung Quốc) | Tiêu đề gốc | View | View/ngày |
|---|---|---|---|
| [XvBkKSN1NEI](https://www.youtube.com/watch?v=XvBkKSN1NEI) | 「日本の車ちっさーーｗｗ」中国自動車産業から突如追い出された日本→5秒後、中国に在庫の山が爆誕した理由【海外の反応】 ("Xe Nhật bé tíiii ｗｗ" Nhật bị đuổi khỏi ngành ô tô TQ → 5 giây sau TQ tồn kho chất núi) | 1.039.686 | 92.760 |
| [qW6hWVrs-ug](https://www.youtube.com/watch?v=qW6hWVrs-ug) | 「日本だけレアアース輸出禁止ねｗ」中国に30倍の値上げされた日本→10年後、価格が暴落し中国が土下座した結果...【海外の反応】 ("Riêng Nhật cấm xuất đất hiếm nhé ｗ" → 10 năm sau giá sập, TQ quỳ lạy) | 1.543.192 | 23.308 |
| [o-z1VN3rjSY](https://www.youtube.com/watch?v=o-z1VN3rjSY) | ウジャウジャと湧き出す中国ロボットに日本が惨敗。5秒後...イーロン・マスクが暴いた中国の闇に番組がお蔵入りになった理由 (Nhật thua robot TQ… 5 giây sau Elon Musk lật góc tối TQ) | 1.489.011 | 11.355 |
| [1klsrQGv9qU](https://www.youtube.com/watch?v=1klsrQGv9qU) | 「日本の方がマナー悪くね？ｗ」中国人ジャーナリストが日本のマナー問題を指摘→5秒後、中国人が食べ放題で盗りまくる姿に世界が絶句 (Nhà báo TQ chê manner Nhật → 5 giây sau cảnh vơ buffet) | 583.023 | 10.576 |
| [Of-kzzUkIZ0](https://www.youtube.com/watch?v=Of-kzzUkIZ0) | 中国作業服が突如爆発しイギリスのビルが完全崩壊・・・ブチギレたBBC記者が日本に突撃し世界が絶句 (Áo quạt TQ phát nổ… phóng viên BBC lao sang Nhật) | 648.617 | 8.859 |
| [mtK69Kp7d14](https://www.youtube.com/watch?v=mtK69Kp7d14) | 「日本の地◯を見てみたーーーいｗｗ」親日家で有名だったジャッキーチェン→反日発言を繰り返し世界で大炎上した理由 (Thành Long… **video thua nhất kênh**) | 31.549 | 592 |

Bảng đủ 19 video: `data\videos_enriched.json` (có `vpd` = view/ngày).

### 1.2 Vì sao Trung Quốc (số đo toàn ngách)

Quét 06/10: 8.616 video của 188 kênh 海外の反応 (phản ứng nước ngoài); lọc video ≥8 phút, 7–150 ngày tuổi còn 6.121 video/183 kênh (`data\niche_topics.json`).

| Tiêu đề kiểu ざまぁ/lật ngược (hả dạ), nhắm vào | Số video | Trung vị view | % video ≥100k |
|---|---|---|---|
| **Trung Quốc** | 203 | **34.704** | **34%** |
| Hàn Quốc | 80 | 11.958 | 16% |
| Phương Tây | 200 | 9.244 | 9% |

→ Trung Quốc có sàn view cao nhất ngách. Đổi lại cạnh tranh đông và rủi ro chính sách cao hơn (§2, §16).

### 1.3 Thắng thua trong kênh mẫu do ĐỀ TÀI, không do hook

15/19 video dùng cùng một khuôn hook mà view/ngày chênh 150 lần.
- Thắng: đối đầu cấp quốc gia/doanh nghiệp (Suzuki, đất hiếm, robot) + **một con số tiền lớn** (1000億, 2000億…) + **kết cục kiểm được** ("N năm sau").
- Thua: chuyện một ngôi sao (Thành Long 592/ngày), sự cố du lịch nhỏ (ngựa cắn 4.083/ngày), đề tài văn hoá cũ (nhặt rác World Cup 1.455/ngày, video ngắn nhất 22 phút).
- Tiêu đề có 「N年後」: trung vị 31.384 view/ngày (4 video); có 「5秒後」: 8.725 (8 video); không mốc: 2.808 (7 video, phần lớn là video tháng 3 khi kênh còn mới).

### 1.4 Đề xuất mã/địa chỉ (h2dev chốt)

- Mã lane (`id`): `nicchu-gyakuten` (日中逆転, "đảo ngược Nhật–Trung"). Thư mục: `assets\P-nicchu-gyakuten\`. Tab: `P-nicchu-gyakuten`.
- `body.mode`: `ai_images` (trường quay + nhân vật AI + cảnh minh hoạ), chèn ảnh/clip tư liệu tự do và thẻ số liệu (§9).

---

## 2. Luật nội dung — BẮT BUỘC (đọc trước khi viết bất cứ tập nào)

Kênh mẫu thắng nhưng làm nhiều việc mà lane mình KHÔNG được làm. Lý do là thực tế, không phải đạo đức suông:
- **Chính sách YouTube:** quốc tịch/dân tộc là nhóm được bảo vệ trong chính sách lời nói thù hằn. Chê chính phủ, chính sách, doanh nghiệp là bình luận chính trị, được phép. Nhắm vào "người Trung Quốc" như một nhóm thì video bị giới hạn quảng cáo hoặc bị gỡ, kênh có thể bị gậy.
- **Mạo danh/gây hiểu lầm:** kênh mẫu gán chương trình bịa cho BBC/ABC, dùng footage người thật (Paul Watson, Nick Clegg, nghi Jack Ma) đóng vai nhân vật bịa. Bình luận đã bắt: 「これフェイク動画ですよ。この動画で取り上げてあるBBCの番組なんて存在しません」 (Đây là video giả. Chương trình BBC trong video không tồn tại) `[auto-caption không áp dụng, bình luận gốc]`.
- **Bôi nhọ (名誉毀損) theo luật Nhật:** kênh mẫu gán câu bịa cho người có tên thật (cầu thủ Hàn, Thành Long, cả 鈴木修 Suzuki Osamu trong cảnh họp dựng lại).
- **Sai dữ kiện:** video tháp Petronas gán chuyện tháp nghiêng 25 mm cho phía Hàn, trong khi Wikipedia ghi tháp nghiêng là Tower 1 của Hazama (Nhật). Bình luận đã bắt.

| ĐƯỢC | KHÔNG ĐƯỢC |
|---|---|
| Chê **quyết định của chính quyền Bắc Kinh**, Bộ Ngoại giao, truyền thông nhà nước, doanh nghiệp/sản phẩm cụ thể có sự cố được báo chí ghi nhận | Chê "người Trung Quốc" như một dân tộc; khái quát 「中国人は民度が低い」 (người TQ dân trí thấp); dùng 「シナ」「支那」「チャンコロ」 |
| Trích **nguyên văn câu thật** của quan chức/báo nhà nước, có ngày + nguồn (vd. 毛寧 Mao Ning 19/11/2025) | Bịa câu cho bất kỳ người có tên thật nào, kể cả người Nhật (鈴木修, 豊田章男…) |
| Chương trình **hư cấu có tên riêng** 『世界の天秤』, 3 nhân vật AI hư cấu cố định (§4) | Gắn tên BBC/CNN/ABC/NHK cho chương trình bịa; dùng mặt/clip người thật đóng vai |
| Kể tai nạn có người chết như sự kiện nghiêm túc, chê **cách chính quyền xử lý** | Hả hê trên người chết; dùng 「ざまぁ」「自業自得」 cho tai nạn, thiên tai |
| Thừa nhận một điểm phía Trung Quốc nói đúng (kênh mẫu cũng làm, giúp video nghe công bằng) | Bẻ số, đảo ai làm gì, đổi "đề xuất" thành "đã quyết" |
| Nhịp VỊ THA cuối: người dân TQ cũng chịu thiệt vì quyết định chính trị | Kết bằng kêu gọi thù ghét |
| Ghi trong mô tả: 「本動画は実際の出来事をもとに再構成したフィクションです。討論番組と登場人物は架空です。」 (Video là hư cấu dựng lại từ sự kiện thật; chương trình và nhân vật là hư cấu) + danh sách nguồn | Đẩy người xem vào LINE/cộng đồng trả phí như kênh mẫu (「裏・日本会議 参加者募集」) |

**Nhãn YouTube:** bật "Nội dung bị thay đổi hoặc tổng hợp" (altered or synthetic) khi đăng, vì nhân vật AI trông như người thật đang nói. Kênh mẫu cũng đã bật (bình luận trích phần 「音声や映像は、AIによって一部変更されているか、すべてAIが生成したものです」 = âm thanh/hình ảnh do AI chỉnh hoặc tạo).

---

## 3. Khung tập (đo trên 19 video, đọc toàn văn 4 video)

### 3.1 Số đo (`data\struct.json`, phụ đề tự động, sai số ±5%)

| Đo | Toàn kênh (19) | 8 video thắng (≥8.000 view/ngày) |
|---|---|---|
| Ký tự / video | trung vị 12.134 | 11.818 |
| Ký tự / phút | 329 (318–366) | 325 |
| Thời lượng | trung vị 36 phút (22–47) | 36 phút |
| Mốc chào kênh 「…JAPANです」 | giây 42 (34–48) | giây 42 |
| Câu treo 「この後…ことになるのです」 | trung vị 5/video | 5,5 |
| Lần nhắc 「コメント」 | trung vị 3 | 3 |
| Số chương trong mô tả | 6–11 | 7–11 |

**Đề xuất gate cho Lane P:** 3 tập đầu 9.000–10.000 chữ (~28–30 phút ở ~330 chữ/phút, h2dev đo lại char-rate giọng của mình). Khi lane chạy ổn mới nâng lên 11.000–12.000 chữ (~35 phút). Không làm dưới 25 phút: video ngắn nhất kênh mẫu (22 phút) là video thua thứ hai.

### 3.2 Khung 9 khối

| # | Khối | Mốc (bản 35') | Việc phải có |
|---|---|---|---|
| 1 | **Trailer / hook** | 0:00–0:40 | Câu chê nguyên văn ở giây 0 → ai nói, ở đâu → 1 dữ kiện thật có số → hứa lật ("N năm sau…") → 「そしてこの一言が後に世界を巻き込む大論争へと発展していくのです」 (§5) |
| 2 | **Nghi thức kênh** | 0:40–1:30 | Chào + định nghĩa từ khoá kênh + "nhưng trên đời có những kẻ…" (gọi tên LOẠI phản diện) + nhắc lại tiêu đề thành câu hỏi + 「一緒に見ていきましょう」 (cùng xem nhé). Lane P không xin đăng ký ở đây (luật h2dev: CTA 1 lần ở cuối) |
| 3 | **Bối cảnh sự thật** | 1:30–4:00 | Sự kiện gốc: năm, tổ chức, con số. Giải thích thuật ngữ (đất hiếm là gì, ALPS là gì) |
| 4 | **Dựng trường quay** | ~4:00 | Thành phố + tên chương trình + chủ đề hôm nay; MC giới thiệu 2 khách, mỗi người 1 câu tả ngoại hình/thái độ |
| 5 | **Vòng 1–2: phe Trung Quốc chiếm thế** | 5:00–15:00 | リン đưa luận điểm chính thức + 1 số liệu THẬT đứng về phía TQ. グレイ hỏi lại 1 con số → câu treo 「その数字が、後に彼自身を追い詰めることになるとは…」 (con số đó sau này dồn chính anh ta vào chân tường). Thừa nhận 1 điểm TQ nói đúng |
| 6 | **Người kể tâm sự + 1 câu hỏi comment** | ~12:00 (≈35%) | Người kể rời câu chuyện 30–60 giây, nói 1 chuyện đời thường liên quan bài học, hỏi người xem 1 câu dễ trả lời. KHÔNG xin like/sub (xem §13) |
| 7 | **Vòng 3–5: phe Nhật lật** | 15:00–30:00 | Mỗi vòng lật bằng 1 [Dn] ("グレイ教授は1枚の資料を取り出しました" — giáo sư lấy ra 1 tờ tài liệu). Phe TQ cãi, lui dần. Câu treo mỗi 3–5 phút |
| 8 | **Đòn kết + kết quả N năm sau** | 30:00–33:30 | Con số kết cục lớn nhất ([Dn] "payoff"). Câu hỏi giả định cuối cho phe TQ. Trường quay im lặng → vỗ tay |
| 9 | **Bài học + VỊ THA + cảm ơn** | 33:30–35:00 | Câu chốt đặc trưng của グレイ: 「日本は言い返しませんでした。結果で答えたのです。」 (Nhật không cãi lại. Họ trả lời bằng kết quả). VỊ THA: người dân TQ cũng là nạn nhân của quyết định chính trị. Cảm ơn + 高評価 + チャンネル登録 (1 lần) |

Ghép với `CUNG_CAM_XUC` của h2dev: KÍCH = khối 1–5 (phe TQ chiếm thế, không giải toả sớm); GIẢI TOẢ = khối 7–8; VỊ THA = khối 9; KẾT CẢM ƠN = khối 9.

### 3.3 Beat sheet mẫu: video Suzuki (TQ, thắng nhất, 44 phút) `[auto-caption, chưa kiểm]`

| Mốc | Chương (mô tả) | Diễn biến | Thiết bị |
|---|---|---|---|
| 0:00 | OP | Cựu cán bộ tập đoàn nhà nước TQ nháy mắt: 「25年もこの国で儲けさせてやったのに、その恩を忘れちゃったのかな」 (Cho kiếm tiền ở nước này 25 năm mà quên ơn rồi à). 2018 Suzuki rút khỏi TQ; 人民日報 (Nhân dân nhật báo) nói do Suzuki kém công nghệ | H02: câu mỉa ở giây 0 + "báo nhà nước nói" |
| 0:43 | | Chào + おもてなし + 「甘い蜜で誘惑し日本の技術を奪い取ろうとする人たちや国がいます」 (có kẻ, có nước dụ bằng mật ngọt để cướp công nghệ Nhật) + câu hỏi "doanh thu hay linh hồn Suzuki" | K27 |
| 1:37 | 30年続くスズキと中国の関係 (quan hệ Suzuki–TQ 30 năm) | Suzuki ở Hamamatsu, xe nhỏ cho nước đang phát triển; Alto ở TQ được gọi 「小型車の王」 (vua xe nhỏ) | Bối cảnh + tự hào |
| ~4:00 | | MC ビクトリア; khách ワン (cựu lãnh đạo 長安汽車 Changan, "trực tiếp đàm phán 2018"), nhà phân tích ナイジェル | Dựng trường quay |
| 5:00 | | ワン: "2024 hơn 60% xe điện bán ra là hàng TQ; Suzuki bám xe xăng nên thua". Doanh số Suzuki ở TQ 25万台 (FY2015) → 10,5万台 (FY2018) | Phe TQ có số thật |
| 6:44 | 中国がスズキに突きつけた究極の二択 (lựa chọn tối hậu TQ đặt ra) | ナイジェル: quy định NEV 2017 (áp 2019) "nhắm" xe nhỏ chạy xăng; TQ đòi công khai công nghệ lõi. ワン: "luật áp cho mọi hãng" | Thừa nhận + lật dần |
| 11:31 | スズキ、1元の屈辱 (Suzuki, nỗi nhục 1 tệ) | Bán phần vốn liên doanh 長安鈴木 giá **1 tệ** ("たった16円"); so với Jaguar Land Rover bán 2400億円. ワン: thời SUV, xe nhỏ hết giá | Số tiền lớn ↔ số tiền tí hon |
| ~15:00 | | ワン mỉa: 「日本の企業は逃げるのが得意」 (doanh nghiệp Nhật giỏi chạy trốn) → trường quay im lặng | Đỉnh KÍCH |
| 16:05 | 鈴木修の最終決断 (quyết định cuối của Suzuki Osamu) | ナイジェル: "không bị đuổi, tự chọn đi". **Cảnh họp dựng lại có lời bịa cho 鈴木修** ← Lane P KHÔNG làm | Kênh mẫu vi phạm §2 |
| 21:15 | 鈴木修の生い立ちとインド市場参入 (tiểu sử + vào Ấn Độ) | 1978 làm chủ tịch tuổi 48; câu thật nổi tiếng 「どこの国でもいいから1番になりたい」 (nước nào cũng được, muốn đứng số 1); 1982 vào Ấn Độ, liên doanh Maruti. ワン đùa "căng-tin có cà ri" | Hồi tưởng + phản diện hề (Lane P bỏ đoạn hề) |
| ~29:00 | | **Người kể tâm sự**: 「というか私がそうでした… 情けは人のためならず… 皆さんも年を重ねることで学んだことはありますか?よかったらコメントで教えてください」 (thật ra tôi cũng vậy… làm ơn rồi ơn lại về mình… các bạn có học được gì khi có tuổi? hãy viết comment) | Khối 6 |
| 29:39 | スズキの信念、ハート・ツー・ハート | Maruti Suzuki ~40% thị phần Ấn Độ; lãi ròng FY2026/3 ~2480億円 kỷ lục; TQ chỉ ~3% doanh số toàn cầu của Suzuki | Đòn số liệu |
| 35:34 | 過去最高益のスズキとEVの墓場になった中国 (Suzuki lãi kỷ lục, TQ thành nghĩa địa xe điện) | Năng lực sản xuất TQ ~5.500万 xe/năm; ~400 công ty ô tô biến mất; "nghĩa địa EV"; xe 460万円 lãi 7万円; liên doanh cũ đổi tên 12/2020 | Kết cục N năm sau |
| ~42:00 | | Bình luận của "khán giả trường quay" (đọc to), vỗ tay | Giải toả |
| 44:15 | ED | Bài học: nước làm xe nhà nước muốn vs công ty làm xe khách hàng muốn; "con cháu chúng ta"; xin like | Khối 9 |

Các số trong bảng là lời video, **chưa kiểm**. Tập Lane P nào dùng lại phải tra lại từ nguồn gốc.

---

## 4. Kinh thánh phim trường (thay cho footage người thật)

### 4.1 Chương trình

- Tên: **『世界の天秤』** (Sekai no Tenbin, "Cán cân thế giới"). Chương trình tranh luận quốc tế, ghi hình ở **London**. Không gắn tên đài. Câu dựng cảnh mẫu: 「ロンドンのスタジオで、国際討論番組『世界の天秤』の収録が始まろうとしていました。今夜のテーマは…」 (Tại trường quay London, chương trình tranh luận quốc tế "Cán cân thế giới" sắp ghi hình. Chủ đề tối nay là…).
- Mỗi tập ghi năm ghi hình = năm hiện tại (2026), nhìn lại sự kiện cũ ("16年が経った今" = 16 năm sau).
- Khán giả trường quay: có, vỗ tay ở cuối, thì thầm ở các cú lật (kênh mẫu dùng).

### 4.2 Ba vai cố định (dùng xuyên kênh như dàn diễn viên, REF-LOCK)

| Vai | Tên (hư cấu) | Hồ sơ | Ngoại hình (cho prompt ảnh) | Giọng | Câu cửa miệng |
|---|---|---|---|---|---|
| MC | **エレナ・ホワイト** (Elena White) | Người Anh, ~45 tuổi, "nổi tiếng trung lập", hỏi thay khán giả | Tóc vàng búi thấp, vest navy, khuyên tai ngọc trai nhỏ, ngồi giữa bàn tròn | Nữ, điềm tĩnh, rõ | 「では、記録を見てみましょう」 (Vậy ta xem hồ sơ) |
| Phe Nhật đúng | **アーサー・グレイ教授** (GS Arthur Gray) | Người Anh, ~62 tuổi, giáo sư sử kinh tế châu Á, từng làm ở Nhật | Tóc muối tiêu, râu ngắn tỉa gọn, kính gọng đồi mồi, áo tweed nâu, luôn có kẹp tài liệu | Nam trầm, chậm, không bao giờ quát | 「数字は嘘をつきません」 (Con số không nói dối) · câu chốt tập: 「日本は言い返しませんでした。結果で答えたのです」 |
| Phe TQ | **リン・ハオユー** (Lin Haoyu) | ~50 tuổi, cựu nghiên cứu viên viện nghiên cứu nhà nước, nói đúng lập trường chính thức | Vest xám, sơ mi trắng không cà vạt, tóc chải ngược, hay khoanh tay, cười khẩy | Nam trung, nhanh, tự tin | 「それは日本側の一方的な見方でしょう」 (Đó là cách nhìn phiến diện của phía Nhật) |

- リン là người **thông minh**, dùng số thật, thua vì dữ kiện chứ không vì bị làm nhục. Không cho リン đùa kiểu "căng-tin có cà ri" như kênh mẫu. Cuối tập リン thừa nhận một phần, giữ thể diện → nhịp VỊ THA.
- Tên hư cấu; trước khi dùng h2dev tra Google một lượt cho chắc không trùng người nổi tiếng.
- Khách mời phụ (tuỳ tập): một "người làm nghề" không tên (ngư dân Hokkaido, kỹ sư đường sắt) xuất hiện qua cảnh minh hoạ ※再現イメージ (hình tái hiện), không phát biểu như người thật.

### 4.3 Người kể (narrator)

Ngôi 3, giọng tiểu thuyết: tả nét mặt, nhịp im lặng (「リンの表情から、余裕が少しずつ消えていきました」 = vẻ ung dung trên mặt Lin dần biến mất). Được nói ý kiến riêng ở khối 6 và khối 9.

### 4.4 Nghi thức kênh (khối 2) — viết theo tên kênh anh chọn

3 phương án tên kênh (anh chọn):
1. **日本は正しかった** (Nhật Bản đã đúng) — em khuyên: nói thẳng lời hứa của mọi tập.
2. **世界が黙った日本** (Nhật Bản khiến thế giới im lặng) — hợp đuôi tiêu đề 「世界が絶句」.
3. **天秤ニッポン** (Cán cân Nippon) — gắn với tên chương trình.

Mẫu nghi thức (phương án 1):
「皆さんこんにちは。『日本は正しかった』です。このチャンネルでは、世界から笑われ、責められた日本が、のちに正しかったと証明された出来事を、記録と数字でお伝えしています。しかし世の中には、{kiểu phản diện của tập: 資源や市場を武器に他国を従わせようとする国}があります。今回は{nhắc lại tiêu đề}。{câu hỏi}一緒に見ていきましょう。」
(Xin chào, đây là "Nhật Bản đã đúng". Kênh kể bằng hồ sơ và con số những lần Nhật bị thế giới chê cười, trách móc rồi sau đó được chứng minh là đúng. Nhưng trên đời có {nước dùng tài nguyên/thị trường làm vũ khí bắt nước khác phục tùng}. Lần này là {…}. Cùng xem nhé.)
Không chép câu おもてなし của kênh mẫu.

---

## 5. Hook (map vào H1–H4 của h2dev)

### 5.1 Mã kiểu trong kho (`E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\patterns.json`, bản trích `data\hook_patterns_laneP.json`)

- Mở đầu: **H02** (Người ngoài nói thẳng một câu hạ bệ). Dự phòng H14 (nhân vật tự tin nói điều sai của mình).
- Khoá: **K27** (mới, thêm 07/10 từ kênh này): báo trước QUY MÔ 「後に世界を巻き込む大論争へ」 → chào kênh kèm định nghĩa → 「しかし世の中には〜」. Phụ: K02 (biến con số thành bí ẩn).
- Khai profile: `script.hook.patterns: ["H02"]`, `script.hook.closer: "K27"`.
- 9 hook kênh mẫu đã chấm điểm /12: `data\hooks_omotenashi_9video.json`.

### 5.2 Khuôn 20–35 giây (H4 viết theo)

```
「{câu chê ngắn, tự tin hoặc mỉa, của phe TQ — nguyên văn thật có nguồn HOẶC lời của リン}」
{ai nói, ở đâu: 国際討論番組『世界の天秤』で、中国の論説員リン・ハオユーが言い放ちました / 中国外務省の報道官は会見でこう述べました}。
{năm}年、{sự kiện thật 1 câu, có 1 con số}。{vì sao lúc đó trông như Nhật thua}。
しかし{N}年後、誰も予想しなかった結末が待っていました。
そしてこの一言が、後に世界を巻き込む大論争へと発展していくのです。
```

### 5.3 Ba hook thật của kênh mẫu (nhắm TQ) `[auto-caption, chưa kiểm]`

- **Suzuki (0–35s):** 「25年もこの国で儲けさせてやったのに、その恩を忘れちゃったのかな。カメラに向けてウィンクしながら挑発的に語ったのは中国国有中央企業グループの元幹部でした。2018年、スズキは中国市場からの撤退を発表。『スズキは市場の変化についていけなかったんでしょう』。なんと中国大手メディア人民網ではスズキの技術不足が主因と報じられています。なぜスズキは世界最大の市場から追い出されたのか。その裏には世界中を震撼させる衝撃の事実が隠されていたのです。」
  (Cho kiếm tiền ở nước này 25 năm mà quên ơn rồi à — cựu lãnh đạo tập đoàn nhà nước TQ vừa nháy mắt vừa khiêu khích. 2018 Suzuki tuyên bố rút khỏi TQ. Báo lớn TQ viết nguyên nhân chính là Suzuki thiếu công nghệ. Vì sao Suzuki bị đuổi khỏi thị trường lớn nhất thế giới? Đằng sau là một sự thật chấn động.)
- **Đất hiếm (0–30s):** 「レアアースの輸出を止めたら日本の産業は崩壊するんですよ。2010年、中国は日本へのレアアース輸出を突如としてストップ。…世界生産の97%を握る中国に輸入の9割を頼っていた日本。これにより世界で日本の自動車産業は終わると報じられました。しかし16年後、誰も予想しなかった衝撃の真実が明らかになります。その運命を変えたのは、たった1人の日本人が下したある決断だったのです。」
  (Ngừng xuất đất hiếm là công nghiệp Nhật sụp. 2010 TQ bất ngờ ngừng xuất. Nhật phụ thuộc 90% vào TQ, nước nắm 97% sản lượng thế giới. Báo chí nói ngành ô tô Nhật tiêu đời. Nhưng 16 năm sau sự thật không ai ngờ lộ ra: vận mệnh đổi nhờ quyết định của một người Nhật.)
- **Manner (0–30s):** 「（笑い）日本人のマナーがいいというのは幻想に過ぎません。イギリスBBCの番組で中国人ジャーナリストが放った一言がスタジオを騒然とさせました。…日本は中国を見習うべきですね。そしてこの発言が、後に世界を揺るがす大論争の引き金となったのです。」
  (Người Nhật lịch sự chỉ là ảo tưởng… Nhật nên học TQ. Và phát ngôn này về sau thành ngòi nổ một cuộc đại tranh luận.) ← Lane P đổi "BBC" thành 『世界の天秤』.

### 5.4 Checklist hook Lane P (Lớp 3 đọc `hook_locked.txt`)

1. Giây 0 là câu thoại của phe TQ, không phải chào, không phải tên kênh.
2. Trước giây 15 có năm + 1 con số thật nằm trong `SỐ ĐƯỢC PHÉP`.
3. Có lời hứa lật ngược nhưng KHÔNG nói kết cục (không lộ "kỷ lục 1兆7005億円" trong hook).
4. Có câu quy mô K27 trước giây 35.
5. Câu chê ở giây 0, nếu gán cho người có tên thật, phải đúng nguyên văn trong [Dn].
6. Không có "BBC/CNN/NHK".
7. Chữ dòng đỏ thumbnail (hoặc ý của nó) xuất hiện trong 45 giây đầu (nguyên tắc 1 trong `NGUYEN_TAC_HOOK_GOI_DANG.md`).
8. Không dùng từ miệt thị (§2).

---

## 6. Tiêu đề

- **Khuôn 4 mảnh:** `「{lời chế giễu kéo dài âm + ｗ/ｗｗ}」{ai}が{làm gì}→{N年後 / 5秒後 / 1か月後}、{kết cục}した理由【海外の反応】`
- Độ dài kênh mẫu: trung vị 62 ký tự (35–78). Đề xuất `gate.title_len` 55–75.
- Đuôi: 「理由」 (lý do) dùng nhiều nhất; 「結果」 (kết quả), 「瞬間」 (khoảnh khắc) dự phòng. Luôn kết 【海外の反応】.
- **Ưu tiên 「N年後」** (kết cục thật) hơn 「5秒後」 (§1.3). Số năm phải đúng với [Dn].
- Mảnh 1 = câu chế giễu của phe TQ. Câu này **không** để trên thumbnail; thumbnail giữ câu đáp trả của phe Nhật (§7).
- Ví dụ thắng của kênh mẫu: 「日本だけレアアース輸出禁止ねｗ」中国に30倍の値上げされた日本→10年後、価格が暴落し中国が土下座した結果...【海外の反応】
- Lane P tránh từ 「土下座」 (quỳ lạy) khi không có sự kiện quỳ thật; thay bằng kết cục có số: 「過去最高」 (cao nhất lịch sử), 「13年連続」, 「4270万人」.
- Grep bắt buộc trước khi chốt: mọi số/năm trong tiêu đề phải có trong `script.txt` (nguyên tắc 8).

## 7. Thumbnail (đo pixel 19/19 ảnh, `data\thumb_dna_measured.json`, `measured: true`)

Ảnh 1280×720. Cả 19 ảnh cùng một template, màu gần như không đổi giữa các video:

| Vùng | y (px, trung vị 19 ảnh) | Màu đo được | Nội dung |
|---|---|---|---|
| **Tầng trên** | 17 → 150 | chữ vàng `#fcff08`, viền đen dày | 1 câu thoại trong 「」, ≤16 ký tự. Thường là **câu đáp trả của phe Nhật** (vd 「レアアース規制？やってみろ」 = Hạn chế đất hiếm à? Cứ thử xem) |
| **Tầng giữa** | 150 → 479 | ảnh | Trái: nhân vật giận (biểu tượng 💢 đỏ). Mũi tên đỏ trái→phải ở giữa. Phải: nhân vật bối rối (「??!」 đỏ, tay ôm trán). Cờ quốc gia góc trái/phải (khung trắng). 1–2 bóng thoại trắng nhỏ (「ふざけるな!」 Đừng có đùa / 「中国は〇〇か？」). Logo kênh tròn góc trái, ngang y ~270–330 |
| **Dòng 1** | 479 → 584 | chữ xanh nhạt `#afe8fa` (một số ảnh trắng), viền đen | Bối cảnh + **số tiền lớn**, ~16–20 ký tự (「日本の捕鯨を30年間猛批判してきたIWC」) |
| **Dòng 2** | 598 → 709 | chữ đỏ hồng `#f22b53`, viền trắng + đen | 「5秒後…」/「結果…」 + kết cục, ~16–18 ký tự |
| Nền dải chữ dưới | 479 → 720 | gần đen `#090102` | dải tối phía sau 2 dòng chữ |

- Font: gothic rất đậm (kiểu 源ノ角ゴシック Heavy / Noto Sans JP Black), viền kép. Chữ do PIL vẽ (skill `youtube-thumbnail`), không để model ảnh vẽ chữ.
- 5/9 thumbnail thắng có số 億 (trăm triệu yên) ở dòng 1 (1000億, 2000億, 1500億, 400億).
- **Lane P đổi gì:** tầng giữa dùng **2 nhân vật AI cố định** (グレイ phía Nhật, cờ Nhật / リン phía TQ, cờ TQ), giống star system của トラブルバスターズ; khán giả quen mặt sau vài tập. Tập nào hook là câu thật của quan chức (vd 毛寧) thì có thể đặt ảnh thật của người đó **chỉ khi ảnh có giấy phép** (ảnh lãnh đạo TQ trên Wikimedia Commons lấy từ kremlin.ru là CC BY 4.0; ghi công trong mô tả).
- Logo kênh: tròn, ~90px, góc trái giữa (đo bằng mắt trên `data\thumbs\K5h68SBuLq8.jpg`).
- Mẫu chữ thumbnail 3 tập đầu: `mau\ep0*\…thumb…txt`.
- Lưới thumbnail kênh mẫu: `hinh\grid_top9_web.jpg` (9 thắng), `hinh\grid_rest10_web.jpg` (10 còn lại).

## 8. Mô tả + chương + tag

Khuôn kênh mẫu (giữ, bỏ phần LINE):
```
#{từ khoá 1} #{từ khoá 2}

「{câu chê nguyên văn — giống hook}」
{2–3 câu bối cảnh}
{1 câu hứa lật, không nói kết cục}
ぜひ本編でお確かめください。

-------------------------------------------------------------
00:00 OP
01:30 {chương 1}
…
{mm:ss} ED
-------------------------------------------------------------

■ 参考資料
{[D1] URL} …

※本動画は実際の出来事をもとに再構成したフィクションです。討論番組と登場人物は架空です。数値は上記資料に基づきます。
```
- Chương: 6–9, đặt tên theo vòng tranh luận, có danh từ cụ thể (「1元の屈辱」 nỗi nhục 1 tệ, 「南鳥島の奇跡」 kỳ tích Minamitorishima).
- Tag kênh mẫu (13 tag/video): `日本, 中国, 世界が見た日本, 中国人, 海外の反応, 国際情勢, 日本称賛, 外国人の反応` + 2–3 tag riêng tập. Lane P bỏ `保守` (bảo thủ) và `韓国`.

## 9. Hình + dựng

### 9.1 Kênh mẫu làm gì (đo 2 video tải về: cá voi 45', đất hiếm 34')

- 416 cắt / 45 phút = 6,5 giây/cảnh; 435 / 34 phút = 4,7 giây/cảnh.
- Lớp hình (22 khung video cá voi): clip tin tức người thật đóng vai 50% · stock 36% · ảnh tư liệu 5% · tranh AI 5% · biểu đồ 0%.
- Chữ: lời kể chữ trắng mincho trên dải tối; lời thoại chữ vàng-cam gradient viền nâu, to hơn, kèm nhãn tên vai (katakana, trắng nghiêng, góc trái giữa); banner chương góc trái trên (chữ vàng nghiêng mincho); ô URL nguồn nhỏ góc phải trên khi nêu số.
- Hiệu ứng: zoom chậm, tách màu RGB cho câu sốc, chữ đỏ "chảy máu" cho lời buộc tội, chữ đóng dấu trên nền lửa (「大論争」), số nổi bật màu xanh lá.
- Khung hình: `hinh\frames_whale_0-150s_web.jpg`, `hinh\frames_whale_body_web.jpg`, `hinh\frames_rare_body_web.jpg`, `hinh\scan_qW6hWVrs-ug_0.jpg` / `_1.jpg` (mỗi 15 giây 1 khung).

### 9.2 Lane P làm

| Lớp | Tỉ lệ đề xuất | Cách làm | Tái dùng |
|---|---|---|---|
| Trường quay + 3 vai | ~45% | 1 ảnh master trường quay (bàn tròn, màn hình lớn sau lưng, đèn xanh–cam, khán giả mờ) + mỗi vai 8–10 biểu cảm/tư thế (bình thản, cười khẩy, giận, sững sờ, cúi đầu, giơ tài liệu, chỉ màn hình, khoanh tay). Sinh 1 lần, REF-LOCK xuyên kênh | skill `youtube-image-prompts` |
| Cảnh minh hoạ sự kiện | ~25% | Ảnh AI tái hiện (cảng cá Hokkaido, tàu trên cầu cạn ban đêm, sân bay vắng) + nhãn ※再現イメージ | gpti2/ima2 |
| Tư liệu thật tự do | ~15% | Ảnh/clip PD, CC (§11.4) | `stockfetch.py`, stock_media_sourcing |
| **Thẻ số liệu động** | ~15% | Chỗ kênh mẫu yếu nhất (0 biểu đồ). Mỗi [Dn] có số → 1 thẻ | skill `motion_graphics` |

Thư viện thẻ số liệu cho Lane P (mỗi thẻ góc dưới phải có dòng 出典 nguồn):
1. Số lớn đếm chạy (「1兆7005億円」).
2. Cột trước/sau 2 năm.
3. Bản đồ cắm cờ + mũi tên hàng hoá (ホタテ → 米国/ベトナム).
4. Dòng thời gian năm (2023/8 → 2025/5 → 2025/11 → 2026).
5. **Thẻ trích câu người thật**: ảnh hồ sơ có giấy phép + 「」 + ngày + nguồn.
6. So sánh 2 cột Nhật | TQ (vd tritium 22兆 vs 112兆, kèm năm).
7. Con dấu đóng xuống (「禁輸」 cấm nhập, 「過去最高」 cao nhất).
8. Thẻ câu hỏi của video (khối 2).

Nhịp: 5–6 giây/cảnh như kênh mẫu. Video hook 0–35s theo luồng hook h2dev (storyboard → ảnh → clip Grok).

## 10. Giọng

- 4 giọng: người kể + エレナ + グレイ + リン. Đo cao độ video cá voi: thoại "Daniel" (vai giáo sư) ~78 Hz, khác hẳn giọng kể ~150–190 Hz → kênh mẫu phân vai. Người thật hay TTS: **chưa xác minh**; h2dev nghe đoạn giọng kể sạch ở `https://www.youtube.com/watch?v=K5h68SBuLq8&t=259` (4:19–4:33) và thoại vai ở 5:37–5:50 rồi chọn.
- Đề xuất: người kể nữ hoặc nam trầm kiểu tường thuật tài liệu; グレイ nam trầm chậm; リン nam trung, nhanh hơn ~10%; エレナ nữ rõ. Lane N đã có hạ tầng đa giọng.
- Cách đọc: tên Trung Quốc viết katakana (毛寧 → マオ・ニン, 王勇平 → ワン・ヨンピン), lần đầu kèm Hán tự trên phụ đề. Luật viết số dùng lại `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\lane_keizai_doc_2026-10-06\HO_SO_BAN_GIAO_LANE_KEIZAI_DOC.md` §4.2 (không dùng ▲, 〜, →, ／ trong số).

## 11. Nguồn tài liệu + quy trình dựng `series_ctx.txt`

### 11.1 Nguồn câu chê THẬT (phía Trung Quốc)

| Nguồn | URL | Dùng |
|---|---|---|
| Bộ Ngoại giao TQ, họp báo thường kỳ (外交部例行记者会) | https://www.mfa.gov.cn/fyrbt_673021/ (tiếng Trung, có bản tiếng Anh/Nhật một phần) | Câu nguyên văn của người phát ngôn, có ngày |
| 人民網日本語版 (People's Daily tiếng Nhật) | http://j.people.com.cn/ | Lập trường nhà nước, có sẵn tiếng Nhật |
| 新華網日本語 (Xinhua tiếng Nhật) | http://jp.news.cn/ | như trên |
| 環球時報 / Global Times | https://www.globaltimes.cn/ | Câu gay gắt nhất, hợp làm câu giây 0 |
| China Daily (lưu trữ) | https://www.chinadaily.com.cn/ + Wayback | Câu khoe cũ (vd 2011 "hơn Shinkansen") |

Luật: lấy câu gốc tiếng Trung/Anh, dịch sang Nhật, ghi 「(中国外務省の会見より・翻訳)」. Không dựa vào bản dịch của kênh khác.

### 11.2 Nguồn kết cục (phía Nhật / quốc tế)

| Nhóm | Nguồn |
|---|---|
| Xuất khẩu thực phẩm, nông thuỷ sản | 農林水産省 (Bộ Nông Lâm Thuỷ sản) https://www.maff.go.jp/j/shokusan/export/ · 財務省貿易統計 (thống kê hải quan) https://www.customs.go.jp/toukei/info/ |
| Du lịch | JNTO https://statistics.jnto.go.jp/ · 観光庁 (Cục Du lịch) |
| ALPS/処理水 | 経済産業省 (Bộ Kinh tế) https://www.meti.go.jp/earthquake/nuclear/hairo_osensui/ · 復興庁 · IAEA |
| Tài nguyên/đất hiếm | JOGMEC https://www.jogmec.go.jp/ · JAMSTEC (南鳥島) · USGS Mineral Commodity Summaries |
| Đường sắt, hạ tầng | 国土交通省 (Bộ Đất đai–Giao thông) · JICA (dự án ODA) https://www.jica.go.jp/ · Wikipedia EN để dựng khung rồi tra nguồn gốc |
| Doanh nghiệp | Trang IR từng công ty; quy trình đọc IR ở hồ sơ keizai-doc §3 |
| Báo chí quốc tế | Reuters, AP, Bloomberg, Nikkei Asia, Al Jazeera, SCMP, Caixin Global |
| Thống kê thương mại | UN Comtrade https://comtradeplus.un.org/ |

### 11.3 Bảy bước cho mỗi tập

1. Chọn vụ: một **câu/quyết định thật** của phía TQ (có ngày) + một **kết cục đo được** N năm/tháng sau.
2. Gom 6–10 nguồn, ưu tiên nguồn gốc (bộ ngành, tổ chức quốc tế) hơn báo.
3. Lập bảng dữ kiện (`fact_table.csv` như keizai-doc §3.3): `id, gia_tri, don_vi, ngay, trang_thai, nguoi_noi, cau_nguyen_van, url, ghi_chu`.
4. Viết `series_ctx.txt` theo khuôn h2dev: `SỐ ĐƯỢC PHÉP` + [Dn] + QUY ƯỚC. QUY ƯỚC luôn có: tên show + 3 vai; ai được nói câu thật; điều phải nói thật dù bất lợi; điều cấm của tập; gợi ý 3–5 vòng tranh luận gắn [Dn]. Mẫu đủ: `mau\ep01_suisan_kinyu\series_ctx.txt`.
5. `promise.txt` 1 câu; `hook\promise.txt` 4 dòng `core_event/payoff/reveal/timeline_start` (mẫu `mau\ep01_suisan_kinyu\hook_promise.txt`).
6. `competitor.txt`: phụ đề video kênh mẫu **cùng dạng**, lấy từ `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\omotenashi_japan\transcripts\<id>.json` (bảng ở §12 ghi video nào hợp tập nào).
7. QC số trước TTS (§14).

### 11.4 Ảnh/clip tự do

| Nguồn | Giấy phép | Ghi chú |
|---|---|---|
| Wikimedia Commons https://commons.wikimedia.org/ | CC BY / CC BY-SA / PD, ghi công | Ảnh lãnh đạo TQ từ kremlin.ru: CC BY 4.0 |
| 首相官邸, các bộ Nhật | 政府標準利用規約 2.0 (tương thích CC BY 4.0) | Kiểm điều khoản từng trang |
| NOAA Fisheries https://www.fisheries.noaa.gov/ · NASA · DVIDS | PD (chính phủ Mỹ) | Ảnh sò điệp, cá, tàu, vệ tinh |
| Pexels / Pixabay | giấy phép riêng, dùng thương mại được | Cảng, nhà máy, đám đông |
| Tool có sẵn | — | `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\src\stockfetch.py --q "scallop fishing hokkaido" --n 8 --sources nasa,commons` |

Không dùng: clip tin tức của đài (NHK, CCTV, BBC…), ảnh báo chí không giấy phép, mặt người thật cho vai hư cấu.

## 12. Kho đề tài (ưu tiên theo: có câu thật của phía TQ · có kết cục đo được · ít kênh đã làm)

Cột "Ngách đã làm" đếm trong 8.616 video (`data\topic_saturation.json` + bảng đo bổ sung trong phiên).

| # | Đề tài | Câu/quyết định của phía TQ (thật) | Kết cục (thật) | Ngách đã làm | competitor.txt gợi ý | Trạng thái hồ sơ |
|---|---|---|---|---|---|---|
| **1** | **Cấm nhập hải sản 2 lần** | 8/2023 cấm toàn diện; 19/11/2025 cấm lại, 毛寧: hải sản Nhật "không còn thị trường" | Xuất khẩu nông-thuỷ sản + thực phẩm 2025: 1兆7005億円, kỷ lục 13 năm liền; Mỹ thành thị trường số 1; sò điệp giữ đầu bảng nhờ Mỹ/Việt Nam | 1 video (107k) | `qW6hWVrs-ug` (tài nguyên làm vũ khí) | **Đủ** `mau\ep01_suisan_kinyu\` |
| **2** | **Tai nạn Ôn Châu 2011** | 7/7/2011 China Daily: "tàu cao tốc TQ hơn Shinkansen" (⚠ cần bản lưu); nộp 21 bằng sáng chế PCT; 王勇平 "chuyện ăn cắp công nghệ là nực cười" | 23/7/2011: 40 chết, 4 toa rơi, toa bị chôn tại chỗ; câu 「信不信由你，反正我信了」; người phát ngôn bị cách chức 16/8; báo cáo 12/2011 nêu lỗi thiết kế, 54 người chịu trách nhiệm; Tokaido Shinkansen từ 1964 không có hành khách chết vì đâm/trật bánh | 10 video, trung vị 706 | `1TDHsSg9cOk` (tàu) + `c1KNjEECLgU` (kỹ thuật) | **Đủ** `mau\ep02_onshu_jiko\` |
| **3** | **Lệnh hạn chế du lịch Nhật 11/2025** | 14/11/2025 Bộ Ngoại giao TQ khuyên dân tránh sang Nhật | 2025 khách quốc tế 4.270 vạn, kỷ lục (TQ tháng 12 giảm ~45%) | 9 video, trung vị 24.510, 3 ≥100k | `Sr9dD2GaHIw` (khách du lịch) | **Đủ** `mau\ep03_toko_jishuku\` |
| 4 | Sri Lanka: cảng Hambantota | 2017 cảng cho TQ thuê 99 năm (1,1 tỷ USD); 9/2020 Sri Lanka huỷ dự án đường sắt nhẹ Colombo vay Nhật 1,8 tỷ USD | 2022 Sri Lanka vỡ nợ; 5/2023 nội các cho hồi sinh dự án của Nhật; Nhật đòi trả khoản do huỷ trước | 2 video, gần như chưa ai làm | `nR4SR6_X81g` (đường TQ ở Kenya) | Nguồn: businesstoday.in 2017-12-09, aljazeera 2017-07-29, adaderana.lk/news/96386, dailymirror.lk (LRT) |
| 5 | Tàu cao tốc Indonesia | 2015 Indonesia chọn TQ (không cần bảo lãnh chính phủ); Nhật đã làm khảo sát 10 năm | Whoosh nợ ~7,27 tỷ USD, quỹ Danantara tái cơ cấu 2025, Tổng thống Prabowo triệu họp | 56 video, top 444k | `nR4SR6_X81g` | Nguồn: en.wikipedia.org/wiki/High-speed_rail_in_Indonesia, business-standard 2015, jakartaglobe, intellinews |
| 6 | "Ngoại giao khẩu trang" 2020 | TQ hạn chế xuất khẩu, rồi viện trợ/bán khẩu trang có điều kiện | 3/2020 Hà Lan thu hồi 60 vạn khẩu trang TQ; Tây Ban Nha trả 64 vạn bộ test (độ chính xác 30%); Sharp chuyển phòng sạch LCD ở Mie sang làm khẩu trang từ 24/3/2020, đợt bốc thăm đầu 4.706.385 người đăng ký (117,7 lần) | 0 video | `Of-kzzUkIZ0` (hàng giả TQ vs hàng Nhật) | Nguồn: aljazeera 2020-03-29, scmp 3077428, bcnretail 20200324 + 20200428 |
| 7 | Nho Shine Muscat | Giống nho Nhật bị mang sang TQ không phép; TQ trồng 53.000 ha (gấp ~30 lần Nhật), đặt tên 「香印翡翠」 | Bộ Nông nghiệp Nhật ước thiệt hại >100億円/năm (7/2022); 10/2024 Hội đồng người tiêu dùng Thái Lan: 23/24 mẫu tồn dư thuốc trừ sâu (9 mẫu truy được đều từ TQ), giá sập. ⚠ FDA Thái sau đó kết luận hàng nhập đạt chuẩn: **phải nói cả điều này** | 17 video liên quan, trung vị 7,7k | `R3jy4WFy7H0` | Nguồn: bangkokpost 2890277, fruitnet 263283, newsweekjapan 50309, moneypost 957085 |
| 8 | Đất hiếm phần 2 (2025–26) | 4/2025 TQ kiểm soát 7 nguyên tố; sau phát ngôn của Takaichi, 0 lô terbium/dysprosium sang Nhật từ 11/2025 | Nhật chi 390億円 đa dạng nguồn (1/2026); JOGMEC + Sojitz ký với Lynas tới 2038, giá sàn 110 USD/kg cho 5.000 tấn NdPr/năm (3/2026); hút bùn đất hiếm 6.000 m ở Minamitorishima thành công (2/2026). ⚠ Thiếu hụt dự kiến kéo tới 2027: **chưa có kết cục thắng**, kể như "Nhật đã chuẩn bị 16 năm" | 44 video (kênh mẫu 1,54M) | `qW6hWVrs-ug` | Nguồn: csis.org, nippon.com yjj2026012000528, caixinglobal 2026-08-21, scienceportal.jst.go.jp 20260206_n01 |

**Theo dõi, chưa làm:** BYD 「RACCO」 (xe điện kei, bán 28/7/2026, 214,5万円; tranh cãi chênh lệch trợ cấp 15万 vs 58万 của xe Nhật). Ngách đã có 64 video, top 1,19M. Chờ số đăng ký xe 8–10/2026 (全軽自協, Hiệp hội xe kei) rồi mới có kết cục.
**Tránh:** Suzuki rút khỏi TQ (kênh mẫu + ニッポンすんだ村 đã làm, 1,04M và 1,2M), robot TQ, buffet/manner du khách (đi ngược §2).

## 13. Bình luận khán giả → `COMMENT_INSIGHT.md`

Lệnh (h2dev, 0 LLM):
```
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\omotenashi_japan --profile <mã lane P>
```
`comments.json` có 1.326 bình luận của 15 video (4 video tải về 0 bình luận, đã bỏ khỏi bản trong gói).

Research đọc trước, đề xuất cho khối `## ĐƯA VÀO PROMPT` (h2dev viết lại):
- Khán giả 50–70+ tuổi (có người tự giới thiệu 「57歳」, 「７３歳のバアバです」 = bà 73 tuổi). Họ thích kể kiến thức/kinh nghiệm của mình trong comment → câu hỏi khối 6 nên mời họ kể chuyện đời.
- 29% bình luận có nhắc TQ/Hàn, phần lớn với giọng tiêu cực. Kịch bản KHÔNG hùa theo giọng đó (§2); comment có thể gay gắt, video thì không.
- Comment nhiều like nhất khen **cách Nhật làm** (dùng cá voi không phí, giữ nguyên tắc), không khen việc đối thủ thua: 「日本人は鯨に感謝してるから無駄なく活用させて頂いてる」 (người Nhật biết ơn cá voi nên dùng không phí phần nào), 11.000 like.
- Người xem tin chuyên gia phương Tây nói hơn người Nhật tự khen: 「…白人の博士が同じ事言ったらヤベッ、て感じになるのが馬鹿らしい」 (…ông tiến sĩ da trắng nói y hệt thì họ mới giật mình), 1.000 like → giữ vai グレイ.
- Có nhóm nhỏ bắt lỗi (2%): hỏi nguồn, nhận ra chương trình bịa, sửa dữ kiện Petronas → mô tả phải có 参考資料 (tài liệu tham khảo) + dòng hư cấu.

**Khác biệt với luật h2dev cần quyết:** kênh mẫu hỏi comment 2–4 lần/video (giữa bài + cuối). Luật h2dev `_cta_mot_lan` chỉ cho xin 高評価/チャンネル登録 1 lần cuối. Câu hỏi comment không phải CTA like/sub, nên em đề xuất giữ **1 câu hỏi comment ở khối 6** + CTA cuối như luật. h2dev kiểm regex `_cta_mot_lan` có xoá nhầm câu 「コメントで教えてください」 không.

## 14. QC riêng Lane P (thêm vào S3 / lớp 3)

1. Mọi số trong `script.txt` có trong `SỐ ĐƯỢC PHÉP` (máy S3 đã làm).
2. Grep cấm: `BBC|CNN|NHK|ＢＢＣ|シナ|支那|チャンコロ|民度` → có là việc phải sửa (trừ khi nằm trong câu trích có nguồn của chính phía TQ).
3. Grep tên người thật trong `script.txt` → mỗi tên phải nằm trong 1 [Dn] có câu nguyên văn; câu trong 「」 sau tên đó phải khớp [Dn].
4. Câu "kết cục" trong tiêu đề có trong 15% cuối script.
5. Tai nạn có người chết: không có 「ざまぁ」「自業自得」「スカッと」 trong đoạn kể tai nạn.
6. Mô tả có `■ 参考資料` + dòng 「本動画は実際の出来事をもとに再構成したフィクションです」.
7. Bật nhãn "altered or synthetic content" khi đăng.
8. Thumbnail: dòng đỏ có trong 45 giây đầu hook (ý hoặc chữ).

## 15. Dữ liệu trong gói

| Đường dẫn (gốc `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneP_from_research_2026-10-07\`) | Nội dung |
|---|---|
| `BAO_CAO_KENH_MAU.html` | Báo cáo có ảnh (16 mục) |
| `NGUYEN_TAC_HOOK_GOI_DANG.md` | 10 nguyên tắc hook + gói đăng |
| `data\channel.json` | API 07/10: 19 video, tiêu đề gốc, mô tả, tag, view, like, comment, thời lượng, ngày đăng |
| `data\videos_enriched.json` | Như trên + `age` (ngày) + `vpd` (view/ngày), mốc 07/10/2026 12:00 UTC |
| `data\transcripts\<id>.json` | 19 phụ đề tự động có mốc giây `[auto-caption, chưa kiểm]` |
| `data\comments.json` | 1.326 bình luận / 15 video, sắp theo like |
| `data\thumbs\<id>.jpg` | 19 thumbnail 1280×720 |
| `data\thumb_dna_measured.json` | Đo pixel 19/19 ảnh (`measured: true`, `seen_in`, `measured_px`, màu) |
| `data\struct.json` | Số đo kịch bản từng video (ký tự, ký tự/phút, mốc chào, câu treo, mốc comment, 0–90s) |
| `data\hooks_omotenashi_9video.json` | 9 hook đã chấm /12 (H02/K27) |
| `data\hook_patterns_laneP.json` | Định nghĩa H02, H14, H43, K02, K06, K24, K27 |
| `data\niche_topics.json` · `data\topic_saturation.json` | Số đo toàn ngách §1.2, §12 |
| `hinh\` | Lưới thumbnail + khung hình đo dựng |
| `mau\ep01_suisan_kinyu\` | `series_ctx.txt`, `promise.txt`, `title.txt`, `thumb_text.txt`, `hook_promise.txt` |
| `mau\ep02_onshu_jiko\` · `mau\ep03_toko_jishuku\` | `series_ctx.txt` + `title_promise_thumb.txt` |

Bản gốc của research: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\omotenashi_japan\` (thêm 2 file video mp4 trong `video\`, script đo `a1…a5`, `n1`, `n2`). Bản sao hồ sơ: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\LANE_P_HANDOFF.md`.

## 16. Rủi ro

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Video bị giới hạn quảng cáo / gậy vì nội dung nhắm quốc tịch | **Cao** | §2 + QC §14.2. Chê chính quyền, không chê dân tộc |
| Bị coi là tin giả (chương trình bịa trông như thật) | Cao | Tên show riêng, không tên đài, dòng hư cấu trong mô tả, nhãn synthetic |
| Ngách đông, đề tài TQ bị nhiều kênh xào | Trung bình | Kho §12 chọn đề tài ít người làm; kết cục có số mới |
| Sai số / sai tên người khi chê | Trung bình | `fact_table` + grep §14.3 |
| Sản xuất nặng (30–35', 4 giọng, ~350 cắt) | Trung bình | 3 tập đầu 28–30 phút; tái dùng bộ nhân vật |
| Quan hệ Nhật–Trung đổi nhanh (cấm/mở lại liên tục) | Trung bình | Mỗi tập ghi ngày tra; tra lại ngay trước khi đăng |
| Kênh mẫu bị YouTube xử lý → cả dạng "phim trường" bị siết | Thấp–TB | Chuẩn §2 giúp lane khác kênh mẫu về mặt chính sách |

## 17. Giới hạn (nói thẳng)

- Kênh mẫu mới 19 video, 7 tháng; có khoảng trống 29/03 → 19/05 không video (có thể đã xoá, chưa xác minh).
- Giọng người hay TTS, phần mềm dựng của kênh mẫu: chưa xác định.
- Bài China Daily 07/07/2011 hiện trả 404; research chưa lấy được bản lưu (máy này không vào được web.archive.org). h2dev hoặc anh mở Wayback kiểm trước khi dùng mốc "16 ngày".
- Câu của 毛寧 ngày 19/11/2025 lấy từ báo tiếng Anh; cần đối chiếu bản gốc tiếng Trung trên trang Bộ Ngoại giao TQ.
- Không lấy được retention kênh mẫu.
- Số trong beat sheet §3.3 là lời video, chưa kiểm.

## 18. Việc của h2dev (theo thứ tự)

1. Đặt mã lane P, tạo profile từ mẫu Lane M (`teinengo-anaba.json`), `docs\BAT_DAU_LANE\<mã>.md`, SOP; thêm dòng vào `docs\DANH_BA_LANE.md`.
2. Chạy `comment_digest.py` (§13) → viết `COMMENT_INSIGHT.md`.
3. Dựng bộ hình cố định 1 lần: trường quay + 3 vai × 8–10 biểu cảm (§4.2, §9.2) + template thumbnail theo số đo §7. Gửi anh duyệt mặt nhân vật trước khi làm tập.
4. Tập 1 = `mau\ep01_suisan_kinyu\` (hồ sơ đủ, chép vào thư mục tập; `competitor.txt` từ `qW6hWVrs-ug`).
5. Tập 2, 3 = `mau\ep02_onshu_jiko\`, `mau\ep03_toko_jishuku\` (tập 2 chờ kiểm bản lưu China Daily).
6. Báo lại: giờ công thật/tập, char-rate giọng đo được, chỗ nào trong hồ sơ thiếu → `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_H2DEV_LANE_P_<ngày>.md`.

Research sẵn sàng làm tiếp khi được gọi: hồ sơ `series_ctx.txt` cho tập 4–8; đo lại kênh mẫu sau 7 ngày; quét thêm kênh cùng dạng nhắm TQ để tìm đề tài mới.
