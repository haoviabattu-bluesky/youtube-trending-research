# HỒ SƠ LANE N — 4 TẬP MỚI (11–14) · việc làm sau tuổi hưu · TRENDING-RESEARCH 2026-10-15

Lane: `senior_korekara` · シニア暮らし研究所 ("Viện nghiên cứu đời sống người cao tuổi") · tab sheet `Lane-N`.
Thư mục hồ sơ: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneN_tap11-14_from_research_2026-10-15\`
Trạng thái: **anh đã duyệt HƯỚNG ①+② (15/10). 4 đề tài, nhân vật, tiêu đề dưới đây CHỜ ANH DUYỆT.** Anh gật thì bảo tab h2dev đọc phiếu
`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\GIAO_VIEC_LANE_N_TAP11-14_2026-10-15.md`.

## §0. Sáu điều đọc trước
1. **Vì sao đổi hướng.** Kênh mình 8 video. Video về chọn việc (ep02) được 3.881 view, các video khác 33–845. Ở các kênh nhỏ, view dồn vào 2 khung: ① 1 nghề · 1 người · 「〜と思っていた」 và ② 2 người · 2 lựa chọn việc làm · ◯年後. Bằng chứng: https://claude.ai/artifact/YTduf9mYUrctW6EZWnGiej
2. **Luật lane KHÔNG đổi:** mỗi tập 1 nhân vật mới, đổi nghề so với video gốc, 6 chương có tên chứa số, kết nghiệm tùng, không quả báo, không list/xếp hạng (tránh trùng Lane M).
3. **Nghề ở đây có 2 lớp.** NGHỀ CŨ (danh tính 40 năm, phải mới, không trùng nghề cấm của lane) và VIỆC SAU HƯU (đề tài tập: xưởng cơm hộp, vệ sinh bệnh viện, bảo vệ đêm, スキマバイト). Thói quen của nghề cũ là chìa khoá giá trị bản thân ở câu chốt.
4. **Giá trị bản thân nằm ở câu chốt, không nằm ở tiêu đề.** Mỗi tập có 1 câu cửa miệng nghề cũ, lặp ở cuối với nghĩa đổi, không giải thích.
5. **Số liệu:** chỉ dùng [Dn] trong `series_ctx.txt`, mọi khối đã mở trang gốc, có URL + nguyên văn, đã qua `kiem_nguon.py` (NẶNG 0 · VỪA 0 cả 4 tập). Số trong truyện (tuổi, lương giờ, giờ giấc) là số truyện. Nhãn ⚠ = cách nói bắt buộc.
6. **competitor.txt = whisper large-v3, chưa kiểm.** Chỉ mượn khung nghề + nhịp. Danh sách tình tiết/câu/tên cấm chép ở cuối mỗi series_ctx.

## §1. Bốn tập (thứ tự đề xuất)
| STT | Slug | Tiêu đề (title.txt) | Khung | Video gốc (khung) |
|---|---|---|---|---|
| 11 | ep11-bento-line | 【漫画】64歳で弁当工場のラインに立った元銀行員。「詰めるだけの仕事」と思っていた1か月後、ラインを止めた理由とは？ (Người 64 tuổi, cựu nhân viên ngân hàng, đứng dây chuyền xưởng cơm hộp. Tưởng "chỉ việc xếp vào hộp", một tháng sau vì sao ông dừng dây chuyền?) | ① | https://www.youtube.com/watch?v=KuUcJiGXzuA (212.059 view, kênh 812 sub) |
| 12 | ep12-byouin-seisou | 【漫画】66歳、朝5時半からの病院清掃。「掃除するだけ」と思っていた元売店員が、患者さんに名前を呼ばれた日 (66 tuổi, dọn vệ sinh bệnh viện từ 5 giờ rưỡi sáng. Ngày người cựu bán hàng ở quầy ga, vốn tưởng "chỉ là lau dọn", được một bệnh nhân gọi tên) | ① | https://www.youtube.com/watch?v=hj7CgEiGfOk (204.996 view, kênh 1.720 sub) |
| 13 | ep13-yakan-keibi | 【漫画】65歳でショッピングモールの夜間警備員になった元テレビ局員。「見回るだけの楽な仕事」のはずが… (65 tuổi làm bảo vệ đêm ở trung tâm thương mại, cựu kỹ thuật viên đài truyền hình. Tưởng là "việc nhàn chỉ đi tuần"…) | ① | https://www.youtube.com/watch?v=etNkNIg8ALw (119.018 view, kênh 1.720 sub) |
| 14 | ep14-saikoyou-sukima | 【漫画】60歳で再雇用に残った人と、辞めてスキマバイトを選んだ人。同じホテルのフロントにいた2人の5年後 (Người ở lại tái tuyển dụng năm 60 tuổi và người nghỉ để làm việc thời vụ qua app. 5 năm sau của 2 người từng đứng cùng quầy lễ tân khách sạn) | ② | https://www.youtube.com/watch?v=TXpTRGszzHY (317.112 view, kênh 1.030 sub) |

Cân bằng: 2 nam chính (ep11, ep13) · 1 nữ chính (ep12) · 2 nữ song song (ep14). Lane N mới có 2 tập nữ chính (ep03, ep07).

## §2. Từng tập — tóm tắt (đầy đủ trong `mau\<slug>\series_ctx.txt`)

### ep11 — 弁当工場 (xưởng cơm hộp)
- Nhân vật: 河合誠 64 tuổi, cựu nhân viên ngân hàng địa phương 42 năm, câu cửa miệng 「確認は、二度」 (kiểm tra hai lần).
- Mạch: thói quen kiểm hai lần bị chê chậm ở dây chuyền. Một tháng sau ông dừng dây chuyền vì 1 lô nhãn bản cũ thiếu 「カシューナッツ」. Hạt điều được thêm vào danh mục bắt buộc ghi nhãn từ 1/4/2026 ([D4] Cục Người tiêu dùng). Ông được giao đối chiếu nhãn. Kết: vẫn không theo kịp tốc độ, chuyển xuống 3 ngày/tuần.
- Dữ liệu: 65 tuổi trở lên có 943 vạn người đi làm, khoảng 1/7 lực lượng lao động · 76,1% làm không chính thức · thị trường đồ ăn sẵn 11,7 nghìn tỷ yên.
- Vì sao: nghề xưởng thực phẩm là nhóm mạnh nhất (xưởng bánh mì 1,19 triệu view, xưởng cơm nắm 212k, xưởng bánh mì bản ăn theo 113k).

### ep12 — 病院清掃 (dọn vệ sinh bệnh viện)
- Nhân vật: 内田和枝 66 tuổi, 45 năm bán hàng ở quầy ga, câu cửa miệng 「声をかけるのが、仕事だから」 (bắt chuyện là việc của tôi).
- Mạch: luật công ty cấm bắt chuyện với bệnh nhân. Một cụ ông nằm viện, 30 năm sáng nào cũng mua báo ở quầy của bà, nhận ra giọng bà. Bà giữ luật, chỉ nói 「失礼します」 (xin phép). Kết: bà xin chuyển sang ca lau sảnh khám ngoại trú.
- Dữ liệu: 57,9% người làm vệ sinh toà nhà từ 60 tuổi trở lên, 27,0% từ 70 tuổi · 3/4 là bán thời gian · thường làm từ sáng sớm. Nguồn: Bộ Y tế–Lao động 6/2025, số liệu điều tra dân số 2020, nên không gắn năm 2026.
- Vì sao: nhóm dọn vệ sinh trung vị 42k view; 205k (dọn toà nhà sáng sớm) và 109k (nhân vật nữ).

### ep13 — 夜間施設警備 (bảo vệ đêm ở trung tâm thương mại)
- Nhân vật: 長谷部透 65 tuổi, cựu kỹ thuật viên phòng phát sóng tổng của đài truyền hình 42 năm, câu cửa miệng 「画面の中で、いつもと違うものを探せ」 (tìm thứ khác thường trong màn hình).
- Mạch: đội trưởng 38 tuổi bảo ông bớt nhìn màn hình, đi tuần nhiều hơn. 21:47 ông thấy trên camera một cụ bà đi vòng mãi ở bãi đỗ xe nhiều tầng. Bà là người sa sút trí tuệ đi lạc, được tìm thấy trong đêm, an toàn, gia đình không biết tên ông.
- Dữ liệu: 596.985 nhân viên bảo vệ, 21,6% từ 70 tuổi (Cảnh sát Quốc gia, 2025) · năm 2025 có 17.345 người sa sút trí tuệ bị báo mất tích; trong số được tìm thấy, 11.369 người tìm thấy ngay trong ngày nhận báo, 573 người được xác nhận đã chết.
- Vì sao: nghề bảo vệ có trung vị cao nhất trong các nghề cụ thể (56,8k); 157k và 119k ở kênh 1.720 sub.

### ep14 — 再雇用 vs スキマバイト (khung ②)
- Nhân vật: 2 bạn cùng khoá ở quầy lễ tân một khách sạn, 42 năm.
  - 杉浦美穂 ở lại tái tuyển dụng: lương 6 phần, làm hậu trường ở trung tâm đặt phòng, sếp là cấp dưới cũ.
  - 石塚絹代 nghỉ, làm thời vụ qua app: 412 lần làm việc, phần lớn dọn phòng khách sạn.
- Mạch: 5 năm sau, đêm trước lễ kỷ niệm 50 năm khách sạn, hai người gặp nhau ở hành lang tầng 9 trong hai bộ đồng phục khác nhau. Không ai thắng.
- Dữ liệu: 99,9% công ty có biện pháp giữ việc tới 65 tuổi, 65,1% qua chế độ tái tuyển dụng, 34,8% có biện pháp tới 70 tuổi · trên app (タイミー tự khảo sát), người từ 60 tuổi trở lên có 308.000 người, gấp 1,9 lần năm trước · tỉ lệ có việc của nhóm 65–69 tuổi là 54,5%.
- ⚠ Lane F đã nhận khung 「辞めた男 vs 残った男」 (đàn ông nghỉ vs đàn ông ở lại) từ 源さん ngày 14/10. Tập này phải là nữ, có スキマバイト, và đo bằng chuyện ở khách sạn.

## §3. Luật tiêu đề mới
`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneN_tap11-14_from_research_2026-10-15\LUAT_TIEU_DE_LANE_N.md`
Tóm tắt: tên nghề cụ thể + tuổi + danh tính cũ + định kiến 「」 + 「と思っていた/のはずが」 + mốc thời gian. Bỏ khuôn 「3つの〜」 trừu tượng. Giá trị bản thân để ở câu chốt.

## §4. Chưa làm / rủi ro
- Chưa có tập nào của khung mới được đăng. Hiệu quả chỉ là suy từ kênh khác + 1 video của mình.
- [D3] ep11 (thị trường đồ ăn sẵn) và [D2] ep14 (タイミー) là nguồn cấp 2: báo trích sách trắng / công ty tự khảo sát. Đã gắn ⚠.
- Nhãn hạt điều có thể còn thời gian chuyển tiếp. Đã khoá cách nói 「古い版のラベル」 (nhãn bản cũ), cấm nói 「違法」 (phạm luật).
- Danh sách tên cấm ep01–ep10 lấy từ series_ctx ep10. Nếu ep10 sau đó có thêm tên, h2dev kiểm lại.
- Chưa kiểm tên hư cấu (みどり食品, みなと台モール) có trùng doanh nghiệp thật không. h2dev đổi nếu cần.

## §5. Việc của h2dev (khi anh đã duyệt)
Xem phiếu `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\GIAO_VIEC_LANE_N_TAP11-14_2026-10-15.md`.

## Dữ liệu gốc
- `data\` trong thư mục này: `meta.json` (số liệu 11 video qua API ngày 15/10), `transcripts\` (6 transcript whisper), `NGUON_DA_MO.md` (danh sách trang đã mở).
- Bản gốc ở research: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\laneN_tap11-14_20261015\` và `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\senior_baito_hunt_20261015\`.
