# HỒ SƠ LANE L — 4 TẬP MỚI (14–17) + 2 DỰ PHÒNG · nguồn 社会観測所 · TRENDING-RESEARCH 2026-10-10

Lane: `shakai_no_naze` · 社会のなぜ研究室 ("Phòng nghiên cứu Vì sao của xã hội") · tab sheet `L-shakai-no-naze` (13/13 đề tài đã làm hết).
Kênh nguồn mới: **社会観測所** ("Trạm quan sát xã hội") https://www.youtube.com/channel/UCiSvbUPLCeB6SiZ2PSKgEeQ — 8.470 sub, 64 video, trung vị 12 video gần nhất 75.306 view.
Thư mục hồ sơ: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneL_tap14-17_from_research_2026-10-10\`

Mỗi tập có sẵn trong `mau\<slug>\`: `series_ctx.txt` (đủ [Dn] + URL đã mở kiểm, nhân vật, cảnh hook, luật, câu trả lời なぜ, đảo chiều, danh sách cấm lặp), `title.txt`, `promise.txt`, `competitor.txt` (transcript video gốc, auto-caption), `competitor.NGUON.txt` (nhãn nguồn), `video_goc.json`. Tập 14 có thêm `tham_khao_hook_jzVO80stWM4.txt` (transcript whisper video メシのタネ 674k — chỉ để học hook, không phải khung).

---

## §0. ĐỌC TRƯỚC — 6 ĐIỀU QUAN TRỌNG NHẤT

1. **Thứ tự làm: 14 リベンジ退職 → 15 手取り → 16 早期退職 → 17 育成キャンセル.** Tập 16 cách tập 11 (50代) hai tập, đúng luật "cùng khán giả thì giãn ra".
2. **Video gốc của 社会観測所 có số liệu SAI/CŨ** (mục §6). Đừng chép số từ `competitor.txt`. Chỉ dùng số trong `series_ctx.txt` (đã mở từng trang nguồn).
3. **Khung 社会観測所 khác ウラガワ một chút:** câu chuyện liền mạch có 2 bạn thân (ひなの ngây thơ chọn sai, みお tỉnh táo giải thích) + người kể chen số liệu. Lane L giữ cách của mình: người trong cuộc là nhân vật chính của tập, さくら là người hỏi (luật 3). Không dùng tên ひなの/みお.
4. **Hook của 社会観測所 yếu (em chấm 5–9/12, mở chậm, không có câu độc).** View đến từ ĐỀ TÀI. Hook phải làm theo cách của lane: cảnh xung đột lạnh, 1–2 câu độc, im lặng, ảo tưởng (mỗi `series_ctx.txt` đã có "CẢNH XUNG ĐỘT CHO HOOK").
5. **Số liệu theo luật anh sửa ep13 (08/10):** nhân vật không đọc thống kê; người kể nói tối đa ~4 số/tập, mỗi số 1 dòng có tên khảo sát + năm; còn lại định tính. Thuế/bảo hiểm (tập 15) tuyệt đối không đọc công thức.
6. **Không trả thù, không hả hê (luật 4)** — tập 14 là chỗ dễ trượt nhất (đề tài "リベンジ"). Đọc kỹ §2.4.

---

## §1. VÌ SAO 4 TẬP NÀY (bằng chứng view thật, đo 2026-10-10)

"Độ nóng tháng" = quét YouTube theo từ khoá, lọc video đăng ≤30 ngày, sắp theo view (dữ liệu `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_L_kansokujo_20261010\heat.json`).

| Tập | Đề tài | Video gốc (社会観測所) | Độ nóng 30 ngày | Kênh mình đã có gì gần |
|---|---|---|---|---|
| 14 | リベンジ退職 (nghỉ việc "trả đũa") | Qafq_LhubTM 73.498 view | 18 video; メシのタネ 674.364 view/21 ngày cùng khuôn manga | tập 3 静かな退職 (người trẻ làm tối thiểu) — khác hướng |
| 15 | 手取り (về tay) | P570Lbe9OXY 86.926 view | 64 video, 13 video ≥10k; 借金ストーリーランド 157k + 121k | tập 5 給料 = tập tốt nhất kênh (5.773 view) — cùng nhóm tiền, khác câu hỏi |
| 16 | 早期退職 50代 | xrUHdGDgR0w 20.200 view sau 2 ngày (~11k/ngày) | 67 video, 38 video ≥10k (đều nhất) | tập 11 50代 — cùng khán giả, khác đề |
| 17 | 育成キャンセル (sếp bỏ dạy vì sợ bị tố) | 6i4rUV1Kbnc 394.830 view (khung) | ABEMA Prime 635.673 view/14 ngày; ウラガワ 102.952 | tập 3 mượn khung ウラガワ YFjKKrYJMw8 nhưng đề khác |

Kênh mình (12 video): tiền/công sở thắng (給料 5.773 · 出世 3.500 · 静かな退職 3.047), đời sống không công sở thua (年賀状 293 · 副業 359). Cả 4 tập đều là công sở + tiền.

---

## §2. TẬP 14 — 『リベンジ退職』なぜ"断らないベテラン"ほど突然辞めるのか ("Nghỉ việc trả đũa" — vì sao người kỳ cựu "không bao giờ từ chối" lại hay đột ngột nghỉ)

### 2.1 Video gốc 社会観測所 — 【漫画】中高年のリベンジ退職が増えている本当の理由とは？ (Lý do thật khiến người trung niên nghỉ việc trả đũa ngày càng nhiều)
https://www.youtube.com/watch?v=Qafq_LhubTM · 73.498 view · 247 like · 45 bình luận · 16 phút

**Tiêu đề:** 【漫画】 + đề tài + 「本当の理由とは？」. Trong 48 video ≥7 ngày tuổi của kênh, tiêu đề có 「本当の理由」 trung vị 60.823 view, không có thì 17.616 (mẫu nhỏ: 6 video). Từ khoá 「リベンジ退職」 là từ tìm kiếm đang nóng.
**Mô tả:** ngắn, chung chung (hashtag #退職 #早期退職 #転職 #就職氷河期世代 + 2 câu "lần này đi tìm hiểu…"). Không nguồn, không mốc thời gian. Không có gì đáng học.

**Dòng thời gian nội dung (auto-caption):**
| Mốc | Cảnh | Đánh giá |
|---|---|---|
| 0:00 | 2 bạn thân thế hệ băng hà than mệt: "phải chiều tụi trẻ, nói nặng là thành quấy rối" | mở than thở, chậm |
| 0:30 | định nghĩa 就職氷河期 1993–2005 (video ghi 2005; định nghĩa chính thức của 内閣府 là 1993–2004) | số lệch |
| 1:40 | hồi tưởng 20 năm trước: sếp 「嫌ならやめろ。全て自己責任だ」 (không thích thì nghỉ. Tất cả là trách nhiệm của mày) | ✅ câu độc tốt |
| 3:21 | nữ nhân viên đến sớm 30 phút pha trà; 4:02 sếp 「体調を崩すなら土日に崩さなきゃだめじゃないか」 (muốn ốm thì phải ốm vào thứ Bảy Chủ nhật chứ) | ✅ bình luận gọi là "パワーワード" (19 like) — nhưng của video gốc, KHÔNG dùng lại |
| 5:19 | cơ chế: thế hệ không được dạy tử tế nay phải dạy người trẻ | ✅ ý hay |
| 5:52 | cơ chế: tăng lương người trẻ → trung niên bị "しわ寄せ" | ✅ ý hay (định tính) |
| 7:26 | sếp: 「若い子は分かんないから水島君にしか頼めなくて」 (tụi trẻ không biết, nên chỉ nhờ được cô Mizushima)「君は有能だから」 (vì cô giỏi mà); đề xuất dạy thêm người bị gạt | ✅✅ gieo payoff |
| 8:34 | 「上司が評価していたのは私の仕事じゃなくて断らないところだった」 (cái sếp đánh giá không phải công việc của tôi, mà là việc tôi không từ chối) | ✅✅ câu hay nhất video |
| 9:39 | phong bì 早期退職 45 tuổi trở lên, tiền thôi việc ×1,5 | ổn |
| 11:19 | bạn được scout, rồi chính mình cũng được scout vào CÙNG công ty | ❌ trùng hợp, mất tin |
| 13:00 | lên kế hoạch "trả đũa": nghỉ đúng mùa bận | ❌ luật 4 lane cấm |
| 14:47 | 1 tháng sau: khách gọi, không ai biết việc → 「みお君に電話して呼び戻せ」 (gọi Mio quay lại đi) | ✅✅ payoff của 7:26 |
| 15:25 | nhân vật chặn số, 「リベンジ退職して良かったな」 (nghỉ kiểu trả đũa là đúng) | ❌ hả hê |

**Bình luận nói gì (45):** đứng hẳn về phía người trung niên — 「若い子へのパワハラは駄目なのに、中高年へのパワハラはいいんですね」 (16 like); 「"リベンジ退職"と、まるで氷河期世代が悪いような表現だけど」 (6). Có người chê: "tiền thôi việc ×1,5 và được dùng phép là công ty trắng rồi" (12) → **khán giả biết rõ thực tế, nhân vật phải khổ thật**.

### 2.2 Mẫu hook: メシのタネ — 【漫画】リベンジ退職をするとどうなるのか？ (Nghỉ việc trả đũa thì sẽ ra sao)
https://www.youtube.com/watch?v=jzVO80stWM4 · 674.364 view/21 ngày · 1.446 like · 131 bình luận (transcript whisper: `mau\ep14-revenge-taishoku\tham_khao_hook_jzVO80stWM4.txt`)

- 0:00 cold open: định về → sếp chặn → 「お前の代わりなんていくらでもいるんだよ」 (người thay mày thiếu gì) → lời dẫn "đây là ghi chép một người làm công bình thường đã chiến đấu với công ty". Em chấm 10/12 (H22 + B câu sốc).
- 1:50 đêm khuya định phá dữ liệu rồi nghỉ → cuộc gọi chặn lại. 8:22 bàn giao bằng sổ tay hoàn chỉnh. 11:14 công ty sụp vì không ai làm được. 13:20 trả lại câu hook: 「代わりなどいくらでもいるとおっしゃったのは専務ですよね」 (chính ngài nói người thay tôi thiếu gì mà).
- Bình luận top: 「リベンジのつもりが痛くも痒くもないのがほとんど」 (62), 「とても合理的な手法…感情ではなく法律通りに」 (57), 「主人公が当初考えていた方法は…止めてもらえてよかった」 (27) → **khán giả thích "đi đúng cách" hơn "phá"**. Đây là cửa cho lane L.
- Không dùng: 退職代行 (luật 5), luật lao động dài, ghi âm, chặn số, kết "当然の報い".

### 2.3 Câu hỏi なぜ cần trả lời (chi tiết + [Dn] ở `series_ctx.txt`)
1. Vì sao việc dồn vào người không từ chối? → cái được đánh giá là "không từ chối".
2. Vì sao người trung niên thấy bất công? → công ty dồn tiền cho người trẻ: 75.6% công ty lớn tăng lương khởi điểm 2026 [D3].
3. Vì sao họ chịu đựng lâu thế? → thế hệ 氷河期 (1993–2004 [D4]) tin "rời đi là hết".
4. Vì sao giờ lại đi đột ngột? → chuyển việc 40–50 tuổi tăng liên tục từ 2021 [D1]: cửa mở thì đi một lần.
5. Vì sao trả đũa không trúng sếp? → 29.0% người từng thấy "リベンジ退職" nói chính họ phải gánh việc [D2] → nhân vật tự bỏ ý định.

### 2.4 Hướng kịch bản mới (khác video gốc ở đâu)
- Bối cảnh mới: **宴会課 của một khách sạn lâu đời** (đời sống: tiệc cưới, 金婚式 — kỷ niệm 50 năm cưới). Nhân vật nam 48 (khán giả 50+ nam đông hơn ở chủ đề này).
- Hook = cảnh văn phòng 9 giờ đêm: tập đề xuất dạy người khác bị đặt ra mép bàn → câu độc → phong bì → im lặng → email nghỉ việc **hẹn giờ gửi** vào sáng tiệc 金婚式. Dừng ở ngón tay trên nút 「送信予約」 (hẹn giờ gửi). (Thay cho "phá dữ liệu" của メシのタネ — cùng lực, không chép.)
- Payoff giữ cơ chế 7:26 → 14:47 của 観測所 (đề xuất bị gạt → không ai biết việc) nhưng **người lãnh hậu quả là sếp và hệ thống, không phải người ngồi cạnh**, vì nhân vật đã chọn bàn giao bằng cuốn sổ.
- Vị tha: 支配人 không ác hoạt hình; câu bản lề + đêm ông lần đầu mở tập đề xuất. Nhân vật nghe điện thoại, chỉ trang sổ, từ chối lễ phép — không chặn số.

---

## §3. TẬP 15 — 「昇給したのに減った」なぜ手取りは増えないのか ("Được tăng lương mà lại giảm" — vì sao tiền về tay không tăng)

### 3.1 Video gốc — 【漫画】手取り14万円…。増加するマイルド貧困層のリアルな生活 (Về tay 14 vạn… đời sống thật của tầng lớp "nghèo nhẹ")
https://www.youtube.com/watch?v=P570Lbe9OXY · 86.926 view · 366 like · 98 bình luận · 17 phút

**Tiêu đề:** con số cụ thể + 「…。」 + "tầng lớp nghèo nhẹ" + 「リアルな生活」. Mô tả: ngắn, chung. Hashtag #手取り15万 #一人暮らし #家計.
**Dòng thời gian:**
| Mốc | Cảnh | Đánh giá |
|---|---|---|
| 0:00 | ngày lĩnh lương: 「あれ？14万円だけ？18万円のはずだけど。何この引かれ方？」 (Ơ? Chỉ 14 vạn? Phải là 18 vạn chứ. Sao bị trừ kiểu này?) | ✅✅ hook 9/12 — khoảnh khắc ai cũng từng có |
| 0:20 | người kể: "Cục Thuế 2024: bình quân 430 vạn" | ❌ số sai (chính thức 令和6年分 = 478万; xem §6) |
| 0:43 | liệt kê dòng trừ: 健康保険・厚生年金・雇用保険・所得税 | ✅ nhưng chỉ 40 giây — câu hỏi "vì sao bị trừ" bị bỏ dở |
| 2:07–5:49 | ở nhà bố mẹ, anh trai ly hôn mang con về, mất phòng sở thích, phải góp thêm → bỏ ra ở riêng | ❌ lạc đề; bình luận 33 like chê logic gia đình |
| 8:16 | liệt kê ngân sách tháng → 「残り1万4000円。う、嘘でしょ？」 (còn lại 1 vạn 4 nghìn. Không thể nào) | ✅ cảnh mạnh |
| 12:11 | từ chối bạn đi nhà hàng Ý; ngại thử serum | ✅ mất mát nhỏ, thật |
| 13:44 | đau răng, đám cưới bạn, tủ lạnh hỏng | ✅ "chi bất ngờ" |
| 16:09 | kết: tiết kiệm + làm thêm | ❌ lời khuyên chung chung |

**Bình luận:** top 1 (42 like) 「平均でデータを出さないで。中央値で出しなよ」 (đừng đưa số bình quân, đưa trung vị đi) → **khán giả soi số; đừng dùng bình quân lương**. 「地方ですが、総支給16〜とかザラ」 (31) → con số "14 vạn" đúng đời thật.

### 3.2 Câu hỏi なぜ (lõi tập 15 — video gốc bỏ dở)
1. Vì sao tăng lương tháng 4 mà tháng 6 về tay lại ít hơn? → năm thứ 2, thuế cư trú bắt đầu trừ từ tháng 6 vì tính trên thu nhập năm trước [D4].
2. Vì sao mùa thu lại giảm thêm? → bảo hiểm tính lại theo lương tháng 4–6, đổi từ tháng 9 [D5].
3. Vì sao tuổi 40 thấy "thêm một dòng"? → 介護保険 từ 40 tuổi [D2]; năm 2026 thêm 子ども・子育て支援金 0.23% từ lương tháng 5 [D3].
4. Vì sao 20 năm qua "về tay" chậm hơn "lương"? → hưu trí 13.58% → 18.3% [D1]; lương thực tế −1.3% khi giá +3.2% [D6]; thuế + bảo hiểm 45.7% thu nhập quốc dân [D7].

### 3.3 Hướng kịch bản mới
- Bối cảnh: **phòng kế toán (経理課) bệnh viện** — さくら là người làm bảng lương, bị mang phiếu tới chất vấn. Hook = quầy 経理 ngày phát lương: 「四月に昇給したんです」 (tháng 4 tôi được tăng lương)「なのに、先月より減ってるんですけど」 (vậy mà ít hơn tháng trước) + điều dưỡng 40 tuổi 「知らない行が、二つ増えてる」 (có thêm hai dòng tôi không biết) + 事務長 lạnh 「文句があるなら、国に言ってください」 (có gì không vừa ý thì nói với nhà nước).
- Câu trả lời đi theo **từng dòng trên phiếu** (đồ vật), không đọc tỷ lệ phí, không làm phép tính. Không số tiền lương cụ thể (không có tư liệu).
- Vị tha: phiếu lương của 事務長 nặng nhất phòng; ông nói câu lạnh vì năm nào cũng bị trách cho những dòng ông không quyết.
- Tránh thiết bị tập 5 (phiếu lương của bố 29 năm trước).

---

## §4. TẬP 16 — 「退職金が増える」なぜ早期退職した50代は後悔するのか ("Tiền thôi việc tăng thêm" — vì sao người 50 tuổi nghỉ sớm lại hối hận)

### 4.1 Video gốc — 【漫画】「退職金が増える」早期退職制度を利用した50代の末路 ("Tiền thôi việc tăng" — kết cục người 50 tuổi dùng chế độ nghỉ sớm)
https://www.youtube.com/watch?v=xrUHdGDgR0w · 20.200 view sau 2 ngày · 92 like · 29 bình luận · 16 phút

**Tiêu đề:** 「lời hứa hấp dẫn」 + 制度 + 「の末路」. Trong kênh, tiêu đề có 「」 trung vị 64.446 view (4 video) vs 19.816. 「末路」 riêng thì không mạnh ở kênh này (2 video). Mô tả: ngắn, chung.
**Dòng thời gian:**
| Mốc | Cảnh | Đánh giá |
|---|---|---|
| 0:00 | nữ trưởng phòng 50 tuổi nhận tờ thông báo +1000 vạn, tính ra 2500 vạn | ✅ đồ vật mở đầu tốt |
| 0:37 | số 人事院: 45 tuổi 80,6% → 55 tuổi 35,2% | ⚠ số của năm 2011, video nói như số mới |
| 1:48 | 「課長までやったし…すぐ次が見つかる」 (mình làm tới trưởng phòng rồi… việc mới sẽ có ngay) | ✅ ảo tưởng rõ |
| 2:23 | đọc 1.18倍 → "thiếu người mà" | ✅ cơ chế hay: hiểu sai con số |
| 4:43 | việc văn phòng: người muốn nhiều, tin tuyển ít | ✅✅ lõi câu trả lời |
| 8:34 | bạn hỏi: "cấp dưới mấy người? giải quyết được gì? con số?" → không trả lời được | ✅✅ cảnh hay nhất |
| 9:50 | phỏng vấn: 「課長だったという部分に少し頼りすぎ」 (hơi dựa quá nhiều vào chuyện từng là trưởng phòng) | ✅ |
| 12:25 | 20 công ty, phỏng vấn 2, đậu 0; tiền thôi việc vơi dần | ✅ |
| 14:40 | đồng nghiệp trẻ dạy hệ thống, 「新卒みたい」 (như người mới ra trường) | ✅ |
**Bình luận:** 「こんな20代みたいな50代の女はいない」 (23), 「何故こんな考えの人が課長になれたんだ」 (21), 「退職金額を通話で語るなど有り得ない」 (không ai nói số tiền thôi việc qua điện thoại) → **nhân vật thiếu thật là điểm yếu lớn nhất**.

### 4.2 Câu hỏi なぜ
1. Vì sao công ty đưa tiền nhiều thế? → phần lớn công ty cắt khi đang lãi: 2025 có 43 công ty niêm yết, 1万7875 người, 67.4% công ty có lãi [D2] — không phải "cứu công ty".
2. Vì sao tiền thêm lại "càng già càng ít"? → mức cộng thêm giảm theo tuổi [D1, số năm 2011 — phải nói năm].
3. Vì sao "thiếu người" mà không ai nhận? → tỷ lệ chung 1.18倍 [D3], việc văn phòng ở Tokyo 0.36倍 [D4].
4. Vì sao chậm? → người 50 tuổi chuyển việc ít nhất (3.8%), dù đang tăng [D5].
5. Vì sao 30 năm kinh nghiệm không giúp? → chức danh không theo mình ra khỏi công ty.

### 4.3 Hướng kịch bản mới
- Nam 53, 総務課長 công ty xây dựng, nợ nhà, con học đại học. Hook = phòng họp nhỏ, 人事部長 xoay tờ giấy, 「今なら、千二百万円を上乗せできます」 (nếu là bây giờ, có thể cộng thêm 1.200 vạn yên)「来年は、この条件は出せません」 (năm sau không có điều kiện này nữa), nhân vật cười 「いい話じゃないですか」 (chẳng phải chuyện tốt sao) — dừng ở ảo tưởng.
- Cảnh "sổ chi tiêu của vợ" (dòng 「収入　なし」 (thu nhập: không) bằng bút chì) thay cho việc nói số tiền.
- Vị tha: 人事部長 giành được con số đó cho anh; năm sau chính ông nằm trong danh sách.

---

## §5. TẬP 17 — 『育成キャンセル』なぜ上司は部下を叱らなくなったのか ("Huỷ đào tạo" — vì sao sếp không còn nhắc nhở cấp dưới)

### 5.1 Video khung — 【漫画】企業がZ世代を採用しなくなった理由とは？ (Vì sao doanh nghiệp ngừng tuyển Gen Z)
https://www.youtube.com/watch?v=6i4rUV1Kbnc · 394.830 view · 1.261 like · 574 bình luận · 15 phút

**Tiêu đề:** 主語 doanh nghiệp + Z世代 + 「理由とは？」. Video nổi nhất kênh sau iPhone. Mô tả: ngắn, chung.
**Cảnh dùng được làm khung (không chép nguyên văn):** 3:16 người mới: "cách chị nói nghe hơi nặng" → người dạy chết lặng 「一瞬何を言われたのか理解できなかった」 (trong khoảnh khắc tôi không hiểu mình vừa bị nói gì); 4:15 "không biết nhắc tới đâu thì được"; 5:47 nhắc lễ phép rồi tự hỏi "mình có nói quá không"; 6:54 ý "không ai dạy thì lỗi lọt ra tới khách" (ở tập mình là lịch tour sai, không phải ảnh SNS).
**Không dùng:** AI tóm tài liệu, mẹ gọi xin nghỉ (luật 5), 退職代行 (luật 5), ảnh bảng trắng lên SNS, cuốn sổ tiền bối.
**Bằng chứng đề tài mới:** ABEMA Prime 【育成キャンセル】 https://www.youtube.com/watch?v=btupuBgNJHo — 635.673 view, 1.278 bình luận. Bình luận top: 「これから大人が叱ってくれなくなる…」 (672), 「日本はいつも極端なんだよな」 (455), 「何がパワハラになるかは相手次第って雰囲気にした時点で何もしない選択肢選ぶのは当たり前」 (380), 「お前の言ってることや言い方は間違ってなかったと思うよって言ってくれる同僚」 (111). ウラガワ YFjKKrYJMw8: cơn giận dồn vào 人事部 tin một phía (48, 59 like).

### 5.2 Câu hỏi なぜ
1. Vì sao sếp im? → 63.3% quản lý ngập ngừng vì sợ bị coi là quấy rối; 61.2% đã "bỏ dạy" [D1].
2. Vì sao lại sợ đến thế? → không ai nói rõ ranh giới; "chỉ dẫn hợp lý" vốn không phải quấy rối [D2].
3. Vì sao im lặng không giúp người trẻ? → 78.2% người trẻ muốn được nói thẳng [D1]; người không được dạy thì đi [D5].
4. Vì sao hai bên không gặp nhau? → ranh giới của cả hai giống nhau: một đối một thì được, trước mặt mọi người thì không [D1]. Lỗi hai năm trước là "trước mặt mọi người", không phải "nhắc lỗi".
5. Giữ cân bằng: quấy rối vẫn có thật, 19.3% [D3] — không biến tập thành "phòng chống quấy rối là thừa".

### 5.3 Hướng kịch bản mới
- Bối cảnh: **công ty du lịch, phòng tour đoàn** (tour suối nước nóng của hội người cao tuổi — sát đời sống). Cold open: các cụ đứng ngoài gió vì xe sai chỗ → 「戸倉さんのせいじゃないよ。誰か、見てくれる人はいなかったのかね」 (không phải lỗi cô Tokura. Không có ai xem giúp cô ấy à) → 「課長、気づいてましたよね」 (trưởng phòng đã nhận ra rồi phải không)「……なんで、言ってくれなかったんですか」 (…sao anh không nói với em) → 「その三週間前――」 (ba tuần trước đó—) → bút dừng trên dòng ngày tháng → 「……いいんじゃないか」 (…được rồi đấy).
- Chìa khoá vị tha: người khiếu nại cũ nói 「あのとき嫌だったのは、みんなの前だったからです」 (hồi đó tôi khó chịu vì bị nói trước mặt mọi người)「言われた内容は、正しかったです」 (lấy cảm hứng từ bình luận 111 like ABEMA, viết lời mới).
- Kết: cây bút đỏ ra khỏi ngăn kéo; 「面談室B」 (phòng họp nhỏ B), một đối một.

---

## §6. KIỂM SỐ LIỆU CỦA VIDEO GỐC (đừng chép số từ competitor.txt)

| Video gốc nói | Thực tế (đã mở nguồn 2026-10-10) | Nguồn |
|---|---|---|
| 手取り: "国税庁 2024 bình quân 430万円" | 令和6年分: 1 năm làm đủ 478万円; chính thức 545万円 / không chính thức 206万円 | https://www.nta.go.jp/publication/statistics/kokuzeicho/minkan/gaiyou/2024.htm |
| 早期退職: 割増 45歳80.6% / 50歳56.1% / 55歳35.2% (nói như số mới) | Đúng số, nhưng là điều tra **平成23年度 (2011)**, công bố 3/2012 | https://www.jinji.go.jp/content/900040854.pdf |
| リベンジ: 氷河期 = 1993〜2005 | 内閣府: 概ね 1993〜2004 | https://www5.cao.go.jp/keizai1/c_hyogaki/seika_r6.pdf |
| 生活保護: 2022 高齢 55.4% / 障害 24.9% / 母子 4.1% / khác 15.5% | 被保護者調査 R7.7 概数: 55.0% / 障害・傷病 25.5% / 母子 3.6% / khác 15.9% | https://www.mhlw.go.jp/toukei/saikin/hw/hihogosya/m2025/dl/11-01.pdf |
| Z世代: "2026 Gen Z sợ điện thoại 80.3%" | **Không tìm ra nguồn.** Điều tra 2026 của ソフツー: 64.4% người ở chỗ làm sợ điện thoại, **người 30 tuổi sợ hơn người 20 tuổi** | https://prtimes.jp/main/html/rd/p/000000106.000028096.html |
| ウラガワ (mô tả YFjKKrYJMw8): "8 phần 10 sếp không mắng nặng" | Không tìm ra. Gần nhất: Job総研 2023 "6 phần 10 sếp không dám mắng"; 2026 "sếp khó xử 69.9%" | https://news.yahoo.co.jp/articles/92fdb13adcd61fdac0521fb4598b78aeb125e337 |
| 早期退職: 有効求人倍率 2026年7月 1.18倍 / マイナビ 50代 3.8% | ✅ đúng | §4 [D3][D5] |
| 手取り: 実質賃金 2025 −1.3%, CPI +3.2%, 食料 +6.8% | ✅ đúng | §3 [D6] |

Nhật ký kiểm: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_L_kansokujo_20261010\verify\` (va/vb/vc/vd.log).

---

## §7. TIÊU ĐỀ VÀ MÔ TẢ — điều đo được

**Tiêu đề (đo trên video ≥7 ngày tuổi; mẫu nhỏ, chỉ để định hướng):**
| Kênh | Có 「」/『』 | Không | Có なぜ | Không なぜ |
|---|---|---|---|---|
| 社会観測所 (48 video) | 64.446 (4) | 19.816 (44) | 23.023 (15) | 20.743 (33) |
| 社会のウラガワ (13 video) | 354.180 (2) | 60.861 (11) | 10.081 (8) | 75.449 (5) |
- Video nổ nhất của ウラガワ không mở bằng なぜ: 『Z世代はもう雇わない』 (700k), 「50代になるにつれて何をしても楽しくなくなる理由」 (956k). Kênh mình 12/12 tiêu đề dạng 「…」なぜ〜のか; tập tốt nhất có người + số + ⁉ (「29歳会社員、父と給料がほぼ同じ⁉」 (Nhân viên 29 tuổi lương gần bằng bố⁉)).
- Đề xuất: giữ khuôn lane (21–35 ký tự, có なぜ để gate lời hứa chạy) nhưng **đặt TỪ KHOÁ TÌM KIẾM trong 『』 ở đầu** khi từ đó đang nóng (『リベンジ退職』, 『育成キャンセル』), hoặc **câu thoại của người trong cuộc** khi đề tài là đời thường (「昇給したのに減った」, 「退職金が増える」). Tiêu đề 4 tập đã viết theo cách này (`mau\*\title.txt`, đã đếm ký tự: 33 · 27 · 31 · 30).
- Tiêu đề/mô tả/thumbnail đang TẮT toàn dự án từ 01/10 → đây chỉ là `title.txt` cho cổng lời hứa + gợi ý cho dự án TITLE khi bật lại.

**Mô tả:** 社会観測所 viết ngắn, không nguồn. タニジン (Oc81ttmqgU8) có mục lục mốc giờ + danh sách 参考文献 URL. メシのタネ có câu "phim hư cấu, không nhằm công kích nghề nào". Mô tả kênh mình đã tốt (kể truyện + số có nguồn + mốc giờ + 「登場人物は架空…」). Gợi ý thêm: cuối mô tả 1 khối 「参考資料」 (tài liệu tham khảo) liệt kê URL [Dn] — khán giả lane này soi số (bình luận "đòi trung vị").

---

## §8. HAI ĐỀ TÀI DỰ PHÒNG (chỉ có competitor.txt + video_goc.json, chưa viết series_ctx)

**A. Điện thoại ở chỗ làm** — `mau\du_phong-denwa\` (khung F6DqxRMCHH4 「なぜZ世代は無能と言われるのか？」 (Vì sao Gen Z bị gọi là vô dụng?) 97.690 view). Góc mới, có số đã kiểm: ソフツー 2026年7月 — 64.4% người ở chỗ làm sợ điện thoại, **người 30 tuổi sợ hơn người 20 tuổi**, nhầm chuyển máy tăng ~1,6 lần (https://prtimes.jp/main/html/rd/p/000000106.000028096.html); BCC 2025年2月 — 50.8% nhân viên ≤3 năm sợ nghe, 48.8% sợ gọi (https://prtimes.jp/main/html/rd/p/000000112.000012929.html). Tiêu đề gợi ý: 「30代のほうが電話が怖い？」 (Người 30 tuổi sợ điện thoại hơn?)なぜ職場の電話は嫌われるのか【漫画】 (31 ký tự). Cách tập 1/3 (đều về người trẻ) ít nhất 3 tập. KHÔNG dùng số 80.3% của video gốc.

**B. Trợ cấp sinh hoạt** — `mau\du_phong-seikatsu-hogo\` (84hB7FjqjhE, 126.056 view, nhanh nhất kênh). Số đã kiểm: 被保護者調査 R7.7 (bảng §6). "Tỷ lệ người đủ điều kiện mà thực nhận" (捕捉率) không có số chính thức (ước tính 15–23% tuỳ cách tính) → chỉ nói định tính. Rủi ro: 3 bình luận top (112–121 like) công kích người nước ngoài nhận trợ cấp → nếu làm, cửa vào phải là công sở (tăng ca → kiệt sức) như video gốc, giọng ấm, không nhắc quốc tịch. Tiêu đề gợi ý: なぜ本当に困っている人ほど生活保護を申請しないのか【漫画】 (29).

---

## §9. VIỆC CỦA H2DEV (làm theo thứ tự)

1. Ghi sheet `L-shakai-no-naze` 4 dòng mới (STT 14–17) bằng đúng `title.txt` của 4 thư mục mẫu; cột C = thư mục tập `E:\CLAUDE\YOUTUBE\h2dev\assets\shakai_no_naze\ep14-revenge-taishoku\` … `ep17-ikusei-cancel\` (slug giữ như thư mục mẫu, đổi được nếu quy ước h2dev khác — báo lại).
2. Mỗi tập: chép 6 file từ `mau\<slug>\` vào thư mục tập (`series_ctx.txt`, `title.txt`, `promise.txt`, `competitor.txt`, `video_goc.json`; tập 14 thêm `tham_khao_hook_jzVO80stWM4.txt` vào `_ref\` hoặc giữ ngoài pipeline). `competitor.NGUON.txt` là nhãn nguồn, không đưa vào pipeline.
3. Máy 1 được sửa PHẦN TRUYỆN của `series_ctx.txt` (tên, bối cảnh, cảnh) nếu thấy hợp lane hơn; **KHÔNG sửa khối [Dn] và SỐ ĐƯỢC PHÉP**. Cần số mới → tự tra, ghi [D7]… kèm URL đã mở.
4. Chạy như tập thường: `py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\make_video.py --profile shakai_no_naze --slug ep14-revenge-taishoku --den B3G` → khoá xong giao máy 3/anh soát (luồng `HUONG_DAN_TAP_TIEP_THEO.md`).
5. Soát riêng khi khoá kịch bản: (a) nhân vật có đọc thống kê không; (b) tập 14 có câu/cảnh hả hê không; (c) tập 15 có câu khuyên tài chính/công thức không; (d) tập 16 người kể có nói năm 2011 khi dùng số 人事院 không; (e) tập 17 có câu chê thế hệ hay "パワハラ対策はやりすぎ" không.
6. Ghi báo cáo: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_H2DEV_LANE_L_TAP14-17_<ngày>.md`.

---

## §10. DỮ LIỆU GỐC (TRENDING-RESEARCH)
- Transcript đầy đủ + bình luận 15 video: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_L_kansokujo_20261010\*.json`; bình luận thêm (メシのタネ, ABEMA, ウラガワ, 借金ストーリーランド): `comments_extra.json`; mô tả + tag: `meta.json`.
- Độ nóng 14 đề tài: `heat.json`. Danh sách video 3 kênh nguồn: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_L_check_20261010\source_videos.json`.
- Hook: 15 video lane này đã nạp `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\hooks.jsonl` (gồm jzVO80stWM4 10/12).
- Báo cáo xếp hạng sáng 10/10: https://claude.ai/artifact/TfQ4VVsfXK5UT3juNmaL6f
