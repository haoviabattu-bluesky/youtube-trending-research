# Lane M — Chọn 3 video tốt nhất (20/10/2026)

**Điều kiện anh đưa:** video đăng trong 5 ngày · > 100.000 view · kênh dạng manga · kênh < 10.000 sub
**Chủ đề:** người già · hưu trí · sau nghỉ hưu nên tiếp tục làm hay nghỉ · tái tuyển dụng

---

## 1. Kết quả quét (số thật)

| Chỉ số | Số lượng |
|---|---|
| Video đăng trong 120 giờ, đã làm sạch | 851 |
| Video thuộc kênh < 10.000 sub | 792 |
| Video dạng manga (kênh < 10k sub) | 608 · thuộc 328 kênh |
| **ĐẠT đủ 4 điều kiện (>100k · ≤5 ngày · manga · <10k sub)** | **1** |

Phân phối view của 608 video manga: ≥100k = 1 (0,2%) · ≥50k = 3 (0,5%) · ≥30k = 16 (2,6%) · ≥20k = 24 (3,9%) · ≥10k = 47 (7,7%).

Cách quét: 21 truy vấn YouTube Data API (`order=viewCount`, `publishedAfter=120h`) + 3 truy vấn InnerTube,
gộp trùng → enrich `videos.list` + `channels.list`. Định dạng kiểm bằng **khung hình thật** (tải video, trích 6 khung/video),
không đoán từ thumbnail.

---

## 2. Ba video chọn

| # | Kênh | Nội dung (dịch) | View | Tuổi | View/ngày | Chạm 100k | Sub |
|---|---|---|---|---|---|---|---|
| 1 | 他人事じゃない人生【ヒトゴト】 | Kết cục ông 62 tuổi tiêu sạch 15 triệu yên trợ cấp thôi việc trong 5 năm | 135.098 | 3,9 ngày | 34.379 | ~2,9 ngày | 931 |
| 2 | 老後のこたえ帖【漫画】 | Đôi vợ chồng 65 tuổi đặt du thuyền qua TV bán hàng — sự thật 10 ngày trên biển | 162.819 | 5,8 ngày | 28.072 | ~3,6 ngày | 3.300 |
| 3 | 源さん【定年シニアの人生相談】 | “Vào viện dưỡng lão là hết” — bà cụ 79 tuổi sống một mình | 123.449 | 6,1 ngày | 20.238 | ~4,9 ngày | 8.340 |

### Link
- ① https://www.youtube.com/watch?v=KCvrhcEsU_0 — kênh https://www.youtube.com/channel/UCTbvUrB31kE-8w-mpv2QYgw
- ② https://www.youtube.com/watch?v=Eu0sV2ZCjr4 — kênh https://www.youtube.com/channel/UCPMLcUgy_zHsdK_K2rWtJCA
- ③ https://www.youtube.com/watch?v=inryFzntZa4 — kênh https://www.youtube.com/channel/UCOkbo1BhQw1NhMj1sBdkt6w

---

## 3. Hook đọc từ khung hình (không phải suy đoán)

1. **Video 1, giây 8:** 「五年前　ここには千五百万円あった」
   → “Năm năm trước, ngay chỗ này từng có 15 triệu yên.” (cảnh: ông 62 tuổi trước cây ATM, tay cầm sổ tiết kiệm)
2. **Video 2, giây 8:** 「西村達也、65歳が目を覚ますと、となりのベッドが空だった。」
   → “Nishimura Tatsuya, 65 tuổi, mở mắt dậy thì chiếc giường bên cạnh đã trống không.” (cabin tàu, giường trống)
3. **Video 3, giây 8:** 「中身は老人ホームのパンフレットが3冊。」
   → “Bên trong là 3 cuốn tờ rơi viện dưỡng lão.” (góc nhìn thứ nhất: tay mở phong bì, brochure trên bàn)

Ba hook dùng ba cơ chế khác nhau: **con số + mất mát** · **chi tiết sai lệch** · **vật thể gợi câu hỏi**.

---

## 4. Bóc công thức

### Video 1 — 他人事じゃない人生【ヒトゴト】 (931 sub · kênh 25 ngày · 11 video · 3 video ≥100k)
- Tiêu đề: 【漫画】退職金1500万円を5年で使い切った62歳の末路…何にいくら使ったのか…
  → “Truyện tranh: Kết cục của ông 62 tuổi tiêu sạch 15 triệu yên trợ cấp thôi việc trong 5 năm… đã tiêu vào đâu, bao nhiêu?”
- Khuôn: **số tiền + mốc thời gian + hậu quả + danh sách chi tiêu**.
- 21:16. Có slide số liệu thật ở phút ~8 (mức trợ cấp trung bình 1.896 vạn yên cho người tốt nghiệp đại học) → chặn cảm giác bịa.
- Công thức chủ đạo của kênh là 「Xになるとどうなるのか」 (làm nghề X thì thế nào); tập này đổi sang “tiền hưu bị tiêu hết” và ăn gấp 5 lần trung vị kênh.

### Video 2 — 老後のこたえ帖【漫画】 (3.300 sub · kênh cũ bật lại · 9 video · 2 video ≥100k)
- Tiêu đề: 【漫画】テレビ通販で豪華クルーズを申し込んだ65歳夫婦。テレビではわからない10日間の船旅の実態とは？
  → “Đôi vợ chồng 65 tuổi đặt du thuyền hạng sang qua TV bán hàng. Sự thật 10 ngày trên biển mà TV không nói là gì?”
- 22:01. Tập anh em cùng kênh (mua xe cắm trại 15 triệu yên đi vòng quanh Nhật 1 năm) đạt 244.065 view → mô-típ lặp lại được.
- 65 tuổi là mốc vàng: trong 608 tiêu đề manga, “65歳” xuất hiện 78 lần (gấp 2,8 lần mốc 60 tuổi).

### Video 3 — 源さん【定年シニアの人生相談】 (8.340 sub · kênh 18 ngày · 50 video · 9 video ≥100k, top 611k)
- Tiêu đề: 【漫画】老人ホームは、入ったら終わり…79歳ひとり暮らしの私は、その意味をまだ知らなかった
  → “Truyện tranh: ‘Vào viện dưỡng lão là hết’ — bà cụ 79 tuổi sống một mình như tôi vẫn chưa hiểu hết ý nghĩa câu ấy”
- Mô-típ **“câu nói quen bị hiểu sai”** — rẻ nhất để sản xuất, không cần dữ liệu.
- Đánh đổi: 55:20 (gấp 2,5 lần mặt bằng 20–22 phút). Nhóm video 3–10 ngày tuổi của kênh có trung vị 174.408 view.

---

## 5. Bản đồ đề tài (đếm từ khoá trong 608 tiêu đề manga)

| Nhóm | Số video | Trần view | Kết luận |
|---|---|---|---|
| Trợ cấp thôi việc / lương hưu (退職 58 · 年金 65) | ~120 | 135k–244k | Nóng nhất |
| Nghỉ hẳn hay làm tiếp / tái tuyển dụng (定年 122) | 122 | 611k | Trần cao nhất, đã đông |
| Du lịch / mua sắm lớn khi về hưu | ~20 | 162k–244k | Còn trống, trần cao |
| Viện dưỡng lão / chăm sóc (介護 39 · 老人ホーム 4) | ~43 | 123k | Cần mô-típ mạnh |
| Việc làm thêm tuổi 70 (バイト 6 · 再就職 5 · 再雇用 5 · シルバー 3) | ~19 | 37k–110k | Gần như trống nhưng **trần thấp** |

**Cảnh báo về 2 đề tài mẫu của anh:** dạng “7 việc làm thêm dễ được nhận ở tuổi 70” và “5 thói quen nhỏ sau nghỉ hưu”
thuộc nhóm *danh sách lời khuyên* — có đất (chỉ 19 video/608) nhưng trần thấp:
- ゆうき (Yuki — thông tin hữu ích cho người cao tuổi): 110.480 view nhưng mất **55 ngày** (≈2.000 view/ngày).
- 縁側の知恵 (Hiên nhà — trí tuệ tuổi già): “TOP 5 việc làm thêm nhàn mà kiếm được” = 37.608 view / 3,3 ngày.
- Cùng kênh 縁側の知恵, video “nghỉ ở 60 hay ở lại đến 65 — 5 năm sau khoảng cách” = **223.201 view**.

→ Muốn vượt 100k phải đổi từ “danh sách lời khuyên” sang **một nhân vật + một quyết định + hậu quả sau N năm**.

---

## 6. Đã loại

**ふたりと1匹 (Hai người và một con)** · 106.844 view / 3,0 ngày · 878 sub — **ĐẠT ngưỡng nhưng LOẠI**:
tải video, trích khung hình → đây là **phim quay người thật** (bố mẹ già làm vườn, mặt làm mờ), không phải manga.

## 7. Danh sách theo dõi

| Video (dịch) | View | Tuổi | View/ngày | Ghi chú |
|---|---|---|---|---|
| Nghỉ ở 60 hay ở lại đến 65 — 5 năm sau khoảng cách (縁側の知恵, 1.410 sub) | 223.201 | 15,3 d | 14.588 | Đúng ngách mở rộng, chạm 100k ~ngày 7 |
| Người nghỉ ở 60 và người ở lại đến 65 (源さん) | 611.194 | 10,1 d | 60.514 | Video lớn nhất ngách |
| Lương hưu dự kiến 70.000 yên/tháng — nữ 50 tuổi sống một mình (源さん) | 45.826 | 1,1 d | 43.437 | Đang bùng, chạm 100k ~2,3 ngày nữa |
| Ông 67 tuổi chở bạn đến lớp nước màu (しあわせチャンネル, 651 sub) | 80.573 | 4,2 d | 19.087 | Sát ngưỡng (~ngày 5,2) |

## 8. Chưa làm / rủi ro
- **Không có comment thật**: thư viện tải comment trả 0 cho cả 3 video → báo cáo không có chân dung khán giả bằng trích dẫn.
- “Ngày chạm 100k” là **ước tính** từ view/ngày trung bình, không đo 2 mốc. Video 2 và 3 hiện đã ngoài cửa sổ 5 ngày.
- Định dạng kiểm bằng 6 khung/video, không xem hết 21–55 phút; chưa đếm tỉ lệ panel truyện vs slide trong video 1.
- Chưa bóc thumbnail chi tiết; video 3 dài 55 phút (chi phí sản xuất gấp 2,5 lần).

## 9. Quyết định
A — Duyệt 3 video này (bóc tiếp hook 0–90s + thumbnail + cấu trúc chương, nạp kho hook, viết hồ sơ bàn giao).
B — Đổi hạng 3 sang video “nghỉ ở 60 hay ở lại đến 65” (223k view, đúng ngách mở rộng).
C — Đào sâu kênh 源さん (50 video, 9 video ≥100k trong 18 ngày) để bóc khuôn tiêu đề + nhịp đăng.
