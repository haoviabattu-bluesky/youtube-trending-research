# HỒ SƠ LANE O — 12 TẬP MỚI (11–22) · TRENDING-RESEARCH 2026-10-15

Lane: `kaigo-sukatto` · kênh **人生のつづき** (Phần tiếp của cuộc đời) https://www.youtube.com/@人生のつづき · tab sheet `Lane-O` (10/10 tập đã làm hết).
Anh duyệt 12 đề tài ngày 15/10 (báo cáo https://claude.ai/artifact/3kxvobNeWsQU4rSnBFL1ZA).
Thư mục hồ sơ: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneO_tap11-22_from_research_2026-10-15\`

Mỗi tập trong `mau\<slug>\`: `series_ctx.txt` (đủ [Dn] + URL đã mở kiểm, CẢNH XUNG ĐỘT CHO HOOK, QUY ƯỚC đủ khối như ep10; KHÔNG có khối LUẬT VIẾT — h2dev tự nạp),
`title.txt`, `promise.txt`, `competitor.txt` + `competitor.segments.json` (transcript video gốc), `competitor.NGUON.txt` (nhãn nguồn), `video_goc.json`,
`PHAN_TICH.md` (kiểm tra chuyên sâu video gốc: số liệu, cấu trúc theo phút, hook 0–90s, bình luận, cách chuyển sang 介護), `hook_record.json` (đã nạp HOOK_LIBRARY).

---

## §0. ĐỌC TRƯỚC — 7 ĐIỀU QUAN TRỌNG NHẤT

1. **Thứ tự làm = đúng số tập 11 → 22** (anh duyệt theo thứ tự này). Tập ấm áp 18, 19 xen giữa các tập "nhân viên khó ưa" để đổi nhịp.
2. **Tiêu đề: giữ đúng `title.txt`.** Studio kênh (15/10) cho thấy CTR vẫn 6–8% nhưng lượt hiển thị tụt từ 88,4k xuống 3k khi tiêu đề chuyển sang kiểu
   giảng giải 「なぜ危険なのか？」「危険な3つの理由」. Cả 12 tiêu đề đều theo khuôn 「câu cửa miệng」+ con số + tình huống, 39–46 ký tự (gate 31–46).
   **Con số trong tiêu đề phải được đọc/nhìn thấy lại ở cao trào** (đã ghi trong từng series_ctx).
3. **Nguồn chính mới là 白衣のうしろ姿** (6 tập: 12, 13, 14, 17, 20, 22) — kênh chép khuôn 千種テンカ, trung vị 22k view. Khán giả đã bắt lỗi chép
   (「これ別動画で同じの見た」 28 like) → mỗi series_ctx có mục **TÌNH TIẾT CẤM CHÉP** liệt kê tên, con số, cảnh chốt, câu kết của video gốc. Không chép.
4. **5 bài học từ bình luận đã cài vào QUY ƯỚC từng tập — đừng gỡ ra khi sửa truyện:**
   - mỗi nhân vật chính có **1 MÂU THUẪN CÓ SỐ** (mồi bình luận số 1 ở kênh đối thủ: 「定時にはこだわるくせに毎日7分遅刻」);
   - **người có quyền lên tiếng ít nhất 1 lần trên màn hình** trước cao trào (video 89k: 6 bình luận top 37–62 like chửi 「店長が悪い」);
   - **người tốt nói thẳng 1 lần** rồi mới để hậu quả tự đến (「ミスを伝えない事の方が良くない」 20 like);
   - **kết phải cho thấy rõ nhân vật xấu ra sao** (kênh mình bị chê 「中途半端な終わり方…どーなったのか」);
   - nghiệp vụ theo cách hiện trường làm thật (khán giả là 介護福祉士 đang xem và bắt lỗi).
5. **Lỗi sản xuất kênh mình bị chê, sửa ở khâu dựng (không nằm trong hồ sơ):** giọng TTS đọc sai chữ Hán (方 かた/ほう, 平野 ひらの, 表 ひょう/おもて — 3 tập bị chê),
   tráo giọng 2 nhân vật (「須藤と安達の声、逆じゃない？」), đạo cụ không liên tục (xe lăn thành ghế thường). Đề nghị: bảng đọc kana cho tên người + từ dễ sai,
   khoá nhân vật→giọng trong `vai.txt`, ghi đạo cụ cố định (xe lăn, kính, máy trợ thính) vào prompt mọi cảnh của nhân vật đó.
6. **Hai tập NGOẠI LỆ được anh duyệt** (18, 19): người nói câu cửa miệng là NGƯỜI NHÀ (em chồng / con trai), nhân viên là người chứng kiến.
   Vẫn giữ khung 3 lần leo thang + kết đổi nghĩa; người nhà không bị bêu riếu, có 1 nhịp vị tha; cụ già không vô lý.
7. **Transcript 5 video 千種 + 1 video 人には言えない話 là whisper chưa kiểm** (YouTube chặn phụ đề IP). `competitor.txt` có lỗi chữ; chỉ dùng để hiểu nhịp,
   không trích câu, không lấy số.

---

## §1. 12 TẬP

| STT | Slug | title.txt (dịch) | Video gốc | Hook gốc | Cơ sở trong truyện |
|---|---|---|---|---|---|
| 11 | ep11-buchou-dattanda | 【漫画】「俺は部長だったんだぞ」が口ぐせの新人介護士が、20年前の部下の母親を担当した結果… ("Tôi từng là trưởng phòng đấy" — nhân viên mới phụ trách mẹ của cấp dưới cũ 20 năm trước) | 千種テンカ https://www.youtube.com/watch?v=Dj1vmfkL7x4 · 25.159 view | H14+H22/K03 · 8/12 | 介護付き有料「ほのかの里」 |
| 12 | ep12-kiitenai | 【漫画】「聞いてないです」が口ぐせの介護士。8年間、毎朝言い直してくれた人が休んだ週に… ("Tôi không được báo" — tuần người 8 năm sáng nào cũng nhắc lại cho hắn nghỉ) | 白衣のうしろ姿 https://www.youtube.com/watch?v=3p51IRlTd5w · 46.927 | H22/K29 · 10/12 | 介護付き有料「あかつき苑」 |
| 13 | ep13-machigaenai | 【漫画】「私、間違えないんで」が口ぐせの介護士が、17回止められていた薬に気づいた日… ("Tôi không bao giờ sai" — ngày biết thuốc mình phát đã bị chặn 17 lần) | 白衣 https://www.youtube.com/watch?v=F1iEog9k3J8 · 13.852 | H22+H14/K29 · 10/12 | ユニット型特養「そよかぜ苑」 |
| 14 | ep14-mae-no-shisetsu | 【漫画】「前の施設ではこうでした」が口ぐせの介護士が、お風呂を一人6分にした結果… ("Ở viện cũ người ta làm thế này" — rút giờ tắm còn 6 phút/người) | 白衣 https://www.youtube.com/watch?v=UAbIF2VPkHQ · 9.247 (2 ngày) | H22+H14/K29+K19 · 8/12 | ユニット型特養「さざなみ荘」 |
| 15 | ep15-osoi-shinjin | 【漫画】「余裕っす」が口ぐせの新人介護士。遅い同期を笑った3か月後、退職代行から電話が来た ("Dễ ợt" — cười đồng kỳ chậm; 3 tháng sau, cuộc gọi từ dịch vụ báo nghỉ) | 千種 https://www.youtube.com/watch?v=uW0alVtJ5B8 · 13.687 (5 ngày) | H45/K04 · 8/12 | デイサービス「ななかまど」 |
| 16 | ep16-isogashii | 【漫画】「俺は忙しいんだよ」が口ぐせの介護士が、眼鏡ひとつを20分待たせた結果… ("Tôi bận lắm" — bắt cụ chờ cặp kính 20 phút) | 千種 https://www.youtube.com/watch?v=ljzDmb13xLQ · 10.972 | H14+H22 · 8/12 | ユニット型特養「はるかぜ荘」 |
| 17 | ep17-shinjin-no-shigoto | 【漫画】「新人の仕事でしょ」が口ぐせの介護士。翌年度、ユニットの新人は0人だった… ("Đó là việc của người mới" — năm sau, đơn vị có 0 người mới) | 白衣 https://www.youtube.com/watch?v=u08jrHrqsV4 · 30.102 | H22/K29+K19 · 10/12 | ユニット型特養「くるみの杜」 |
| 18 | ep18-beiju-shashin | 【漫画】「他人なんだから」が口ぐせの義妹が、米寿の写真から外した嫁。面会記録の96回が… ("Người ngoài mà" — em chồng gạt chị dâu khỏi ảnh mừng thọ 88; 96 lần trong sổ thăm) | 千種 https://www.youtube.com/watch?v=JkcoRdMJwGU · 5.934 (2 ngày) | H02+H41/K02 · 10/12 | ユニット型特養「やまぶき荘」 |
| 19 | ep19-haha-no-day | 【漫画】「今、忙しいから」が口ぐせの息子。雨の日もデイを休まなかった母の58回… ("Giờ con bận" — 58 lần mẹ không nghỉ デイ cả ngày mưa) | 千種 https://www.youtube.com/watch?v=Po7AuZopDng · 9.891 (4 ngày) | H41/K04 · 8/12 | デイサービス「やまびこ」 |
| 20 | ep20-saikin-no-wakai | 【漫画】「最近の若い子は」が口ぐせの夜勤介護士が、27回鳴ったセンサーを聞き流した結果… ("Bọn trẻ bây giờ…" — làm ngơ cảm biến kêu 27 lần) | 白衣 https://www.youtube.com/watch?v=bCWeaqwuffk · 15.801 | H22+H14/K29+K19 · 8/12 | 介護付き有料「しらさぎ」 |
| 21 | ep21-nattoku | 【漫画】「納得できないんですけど」が口ぐせの介護士が、会議を17回止めた結果… ("Tôi chưa thấy thuyết phục" — chặn cuộc họp 17 lần) | 人には言えない話 https://www.youtube.com/watch?v=m-YW2q02sXM · 78.112, 366 bình luận | H12+H14/K04 · 9/12 | ユニット型特養「わかたけの郷」 |
| 22 | ep22-sekinin-ore | 【漫画】「責任は俺が取る」が口ぐせの介護主任。ヒヤリハット11枚の聞き取りに、同じ一言が… ("Tôi chịu trách nhiệm" — 11 phiếu phỏng vấn ヒヤリハット cùng một câu) | 白衣 https://www.youtube.com/watch?v=Opg5WD4ltNM · 10.595 | H22/K29+K19 · 11/12 | ユニット型特養「かなえ苑」 |

Tên nhân vật + cơ sở của 12 tập đã dò chéo: không trùng nhau, không trùng danh sách cấm ep01–ep10 (mỗi series_ctx có dòng TÊN ĐÃ DÙNG nới thêm tên ep10).
Khi làm tập 12 trở đi, h2dev cộng dồn tên của các tập mới vào dòng cấm như vẫn làm.

---

## §2. TỪNG TẬP — cốt, hook của mình, tư liệu, rủi ro

### 11 · 俺は部長だったんだぞ
- **Cốt:** 蓮見 62 tuổi, cựu 営業部長 (部下百二十人), vào làm 介護職員 chưa bằng cấp; đùn hỗ trợ vệ sinh cho người trẻ. Lần 3: con gái một cụ bà (尚子) chính là cấp dưới cũ mà
  20 năm trước hắn không cho về khi mẹ cô ngã. Hậu quả: 面談 hết 試用期間, chức フロアリーダー về tay 早川 26 tuổi. Kết: hắn tự dẫn cụ đi vệ sinh, câu cửa miệng thành lời thú nhận.
- **Mâu thuẫn có số:** khoe 部下百二十人 ↔ 排泄チェック表 3 tháng 0 chữ ký.
- **Hook của mình:** góc 面会 Chủ nhật, 尚子 lễ phép nhờ đưa mẹ đi vệ sinh → 「俺は部長だったんだぞ」「下の世話をしに、ここへ来たんじゃない」 trước 2 gia đình.
- **[Dn]:** 初任者研修 130時間 (mới, n-helper + 石川労働局 PDF) · 認知症介護基礎研修 1年以内 (dùng lại ep04) · ヒヤリハット.
- **Rủi ro:** gần ep04 (cựu quản lý gặp cấp dưới cũ) — đã khoá: cấp dưới cũ là NGƯỜI NHÀ, không quyền gì, 施設長 không biết. Cấm 名刺/婚活 (dấu hiệu video gốc + video 197k).

### 12 · 聞いてないです
- **Cốt:** 加賀谷 12 năm chưa mở sổ bàn giao; パート 岡本 8 năm sáng nào cũng nói lại tận mặt lúc 8:20. 3 lần câu cửa miệng rơi đúng những sáng 岡本 nghỉ; lần 3 hắn đang
  chủ trì 申し送り tuần thử vai フロアリーダー, nói trước mặt giám đốc. Leader về tay 上野.
- **Mâu thuẫn có số:** đòi mọi thứ phải nói tận mặt, nhưng sau ca đêm chỉ bảo 「記録に全部書いたから読んで」 (A4 hai trang).
- **Hook của mình:** con gái thấy máy trợ thính của mẹ (lãng tai) vẫn nằm trong hộp; 14時 mẹ mới nghe được giọng con.
- **[Dn]:** cổng 生産性向上 của 厚労省 về chia sẻ thông tin · hướng dẫn テクノエイド協会 về hỗ trợ máy trợ thính.
- **Rủi ro:** gần ep09 (không đọc giấy tờ) — đã cấm dấu/chữ ký, cao trào dời về buổi 申し送り. series_ctx dài 16,7k ký tự (hơi quá 16k).

### 13 · 私、間違えないんで
- **Cốt:** 曽根 54 tuổi phát thuốc sáng mà không đọc to tên trên gói, dù chính bà dán tờ nhắc người khác đọc. パート 千葉 nói thẳng 1 lần rồi lặng lẽ chặn 17 lần,
  phiếu ヒヤリハット không có ô tên người đưa sai. Cao trào: 面談 chọn 副主任, 17 phiếu đặt cạnh bảng phân ca. Câu cuối 「私、間違えるんで」.
- **Hook của mình:** con gái đọc gói thuốc, phát hiện sai tên — 2 cụ cùng họ 高木.
- **[Dn]:** 医政発第0726005号 (nhân viên được hỗ trợ uống thuốc đã chia gói, dưới chỉ đạo y tá) · hướng dẫn phòng tai nạn 厚労省 11/2025 (đọc to tên, kiểm nhiều lớp) · ヒヤリハット.
- **Rủi ro:** ảnh phải phân biệt rõ 2 cụ cùng họ; không nêu tên thuốc.

### 14 · 前の施設ではこうでした
- **Cốt:** 田島 47 tuổi, 12 năm tổ tắm dây chuyền ở 清和園, bỏ bảng giờ tắm theo ý từng cụ của パート 坪井, đổi thành sáng/6 phút mỗi cụ. Cụ 谷 từng ở 清和園 nhận ra hắn;
  hồ sơ chuyển viện có dòng chính tay hắn viết "chiều, nước ấm thì cụ chịu tắm". 主任 về tay 角田.
- **Mâu thuẫn có số:** cụ 6 phút/người ↔ tối nào hắn cũng ngâm bồn 40 phút.
- **Hook của mình:** con trai cụ hỏi giờ tắm, cụ chỉ nói 「朝は、寒いんだ」.
- **[Dn]:** 基準省令 điều 39/42 (e-Gov) · ユニット型: cho tắm theo ý cụ, không xếp đồng loạt (giải thích của Bộ) · 従来型 1週間に2回以上.
- **Rủi ro:** gần ep09 (bỏ qua thói quen cụ) — đã cấm 生活歴シート; cảnh lộ được dời khỏi bàn phỏng vấn, cho chính cụ nói ra.

### 15 · 余裕っす
- **Cốt:** デイ「ななかまど」; 葉山 nhanh vì bỏ bước xác nhận: tắm (khoe 6 người 40 phút, パート mất thêm 25 phút làm nốt) → đưa đón (cụ bà chờ 25 phút dưới nắng) →
  suýt đưa nhầm gói thuốc giữa 2 cụ cùng họ 萩原. Tròn 3 tháng: cuộc gọi 退職代行. Đồng kỳ "chậm" 日比野 ở lại. 主任 lên tiếng từ lần 2.
- **Hook của mình:** 葉山 bước ra từ phòng tắm, khoe to với 主任 ở bảng trắng.
- **[Dn]:** 退職代行 (3 loại đơn vị; đơn vị tư nhân chỉ chuyển lời, không đàm phán — 弁護士法72条; nguồn văn phòng luật/社労士, không có nguồn nhà nước) · 民法627条 2週間 · ヒヤリハット.
- **Rủi ro:** thành quảng cáo 退職代行 hoặc chê "thế hệ Z" — đã cấm tên dịch vụ/giá/lời khuyên; người tốt cũng 22 tuổi. Lưu ý: chi tiết 2 cụ cùng họ giống tập 13 → nếu làm liền nhau, đổi tình huống lần 3 của tập 15.

### 16 · 俺は忙しいんだよ
- **Cốt:** 半田, giỏi tắm/chuyển chỗ nhất, cột 業務表 xong lúc 14時 nhưng mọi việc ngoài danh sách đều "bận". Con trai cụ ハル nổi giận CÓ LÝ vì mẹ chờ kính 20 phút; cụ tự với
  suýt ngã (ヒヤリハット). Anh con trai im khi gặp パート 林 — 15 năm trước bà là helper lau kính cho cha anh. 苦情記録 → chọn ユニットリーダー, về tay người 中途 cài từ tháng 4.
- **Mâu thuẫn có số:** cột của hắn tích xong 14時; cột パート xong 17時30分, ô 「その他」 kín việc vặt.
- **[Dn]:** đều dùng lại nguyên văn: 苦情 (ep03) · ヒヤリハット · ユニットリーダー (ep01).
- **Rủi ro:** gần ep06/ep07 — đã cấm điện thoại, từ chối ナースコール, lịch sử chuông gọi.

### 17 · 新人の仕事でしょ
- **Cốt:** 景山 đùn thay ga, phòng 汚物 cho người mới 青木, 2 lần kéo cậu khỏi buổi học kiểm soát nhiễm khuẩn bắt buộc. 委員会 3 tháng/lần phát hiện thiếu hồ sơ đào tạo,
  青木 được chuyển đơn vị; họp phân bổ năm sau: đơn vị bà 0 người mới, vai kèm cặp về 加藤, việc bẩn chia theo bảng có tên bà. Khác ep05: không mắng, không ai nghỉ.
- **Mâu thuẫn có số:** bảo 青木 「休憩は60分ちゃんと取って」 nhưng bữa trưa hôm hook của cậu 6 phút.
- **[Dn]:** 老企第43号 (đào tạo ≥2 lần/năm, bắt buộc khi tuyển mới, phải lưu hồ sơ) · 基準 第27条 (委員会 khoảng 3 tháng/lần).
- **Rủi ro:** một phần khán giả lớn tuổi đồng tình "việc bẩn là của người mới" — đã cân bằng bằng mâu thuẫn 60 phút + quá khứ của bà. Chữ 表 đánh dấu đọc ひょう.

### 18 · 他人なんだから (NGOẠI LỆ — người nhà)
- **Cốt:** tiệc 米寿 tại viện; em chồng みどり nói 「他人なんだから」 3 lần (quần áo → họp kế hoạch chăm sóc → chụp ảnh). Trong mọi tấm ảnh cụ ヨシ nhìn người cầm máy là
  chị dâu 万里子. Tháng 1, họp lập lại kế hoạch đọc số lượt thăm: 96/99, toàn chiều thứ Tư; cụ gọi chị dâu là 「水曜日の人」; chị thành người liên lạc chính.
  Vị tha: 30 năm ở nhà chồng みどり cũng bị gọi là "người ngoài". Nhân viên 山内 chứng kiến.
- **[Dn]:** 基準 điều 45 khoản 3 + điều 12 (e-Gov) · ヒヤリハット · 米寿 = 88 tuổi (quy định 2 địa phương).
- **Rủi ro:** ep03 đã dùng sổ thăm làm vật chứng → ở đây chỉ là con số đọc trong họp, không lật trang. Video gốc 2 ngày tuổi, chỉ 2 bình luận.

### 19 · 今、忙しいから (NGOẠI LỆ — tập ấm)
- **Cốt:** con trai 良一 nói 「今、忙しいから」 3 lần (tay vịn hỏng → báo ヒヤリハット sáng mưa → giữa họp kế hoạch chăm sóc). Nhân viên đi xe đón 目黒 kể: sáng mưa anh lái qua
  góc phố nhà mẹ lúc 8時32分; 6 năm trước anh từng dừng xe vẫy tay một lần. Từ đó mục tiêu tập của mẹ ở デイ là đứng được 10 phút ở cổng; 3 năm không bỏ sáng mưa nào (58 lần).
  Kết: "bận" giờ là bận đứng che ô cho mẹ. Mẹ vẫn sống.
- **[Dn]:** 基準 điều 99 (kế hoạch デイ) · điều 13 (họp/thăm nhà ≥1 lần/tháng) · hỗ trợ trong nhà khi đón tối đa 30 phút/ngày (2 trang chuyên ngành — chưa có nguồn chính thức, dùng định tính) · ヒヤリハット.
- **Rủi ro:** không có hậu quả từ cơ chế kiểu xét chọn → thay bằng anh tự xin ghi vai trò của mình vào kế hoạch chăm sóc. Mức giảm 47単位 đã kiểm nhưng KHÔNG dùng (video ハタジン mở bằng chính số này).

### 20 · 最近の若い子は
- **Cốt:** 滝本 58 tuổi, chuyên ca đêm, coi cảm biến là báo giả, khoe 15.000 bước/đêm (đồng hồ thông minh đếm). Người mới 瀬尾 22 tuổi chạy 30 m tới 27 lần. Họp kế hoạch có con gái cụ:
  cụ スズ nói 「…あなたじゃ、ないわ」, ghi chép hiện 27 dòng tên 瀬尾. Gia hạn hợp đồng: hắn sang ca ngày, 千田 56 tuổi làm 夜勤リーダー.
- **Hook của mình:** 申し送り sáng sau đêm cụ suýt ngã.
- **[Dn]:** 生産性向上推進体制加算 (3 loại thiết bị, 委員会 3 tháng/lần, hỏi ý cụ trước khi lắp) · hướng dẫn 厚労省 11/2025 (cảm biến rời giường, インカム; thiết bị chỉ là công cụ) · ヒヤリハット.
- **Rủi ro:** nhãn 老害 trong bình luận gốc → người thế chỗ 千田 cùng thế hệ, dùng thiết bị giỏi (không chê người già). Gần ep05/ep07 — đã cấm.

### 21 · 納得できないんですけど
- **Cốt:** 渡瀬 41 tuổi nói câu cửa miệng 3 lần: chặn đề xuất người mới → chặn thử cảm biến trong 委員会 → ngay trong buổi xét chọn ユニットリーダー. Khi giám đốc hỏi lý do việc anh tự đổi
  giờ tắm 3 cụ, anh buột 「それ、説明する必要あります？」 — 「今のが、理由です」. Vị tha: buổi tắm chiều ngày xưa không ai giải thích cho anh. Kết: người mới nói ngược câu đó với anh, anh trả lời.
- **Mâu thuẫn có số:** 17 lần trong biên bản họp ↔ 0 lần tự giải thích.
- **[Dn]:** 基準 điều 35-3 (委員会 nâng cao năng suất, 3 năm chuyển tiếp) · ban đêm 2 ユニット 1 người · ヒヤリハット.
- **Rủi ro:** khán giả có thể bênh anh ở chuyện cảm biến → phải cho thấy từng lo ngại đã được trả lời xong. TUYỆT ĐỐI không gán bệnh tâm lý (bình luận gốc gán ASD 152 like).
  Con số 17 trùng tập 13 → khi viết có thể đổi (ví dụ 14) miễn khớp toàn bài.

### 22 · 責任は俺が取る
- **Cốt:** chủ nhiệm 郷田 bắt cấp dưới bỏ bước an toàn (cho 2 cụ ăn cùng lúc — 1 cụ sặc; tắt cảm biến rời giường gia đình đã đồng ý — suýt ngã 3 giờ sáng); phiếu do cấp dưới viết,
  nguyên nhân luôn "nhân viên không kiểm". 委員会 phòng tai nạn: 浅野 đặt 11 phiếu phỏng vấn, tờ nào cũng 「責任は俺が取る、と言われました」. Nguyên nhân được sửa, tháng 4 hắn mất chức.
- **Mâu thuẫn có số:** ngày nào cũng về 17:30 ↔ cả 11 phiếu viết sau 18:00.
- **[Dn]:** 基準 điều 35 + 老企43号 (báo cáo được 委員会 thu thập phân tích, không để phạt) · ヒヤリハット.
- **Rủi ro:** video gốc view thấp nhất nhóm (đề tài giấy tờ) → hook dựng quanh con trai và nhân viên ca đêm đứng cạnh nhau ở quầy. Đã tránh 二人介助, lịch sử chuông (ep06/07).

---

## §3. ĐÃ KIỂM
- 12 thư mục đủ file; JSON đọc được; tiêu đề 39–46 ký tự (Python len); mọi URL trong [Dn] đã thử mở lại bằng máy (2 link chết `kaigoshoku.mynavi.jp/.../4340/` đã gỡ khỏi tập 16, 21 — link song song lashic-care còn sống; `biz.moneyforward.com` trả 403 với bot, mở bằng trình duyệt được).
- Tên nhân vật/cơ sở 12 tập: không trùng nhau, không trùng danh sách cấm.
- Hook 12 video gốc đã nạp `E:\CLAUDE\YOUTUBE\HOOK_LIBRARY\HOOK_LIBRARY.md` (+ mã mới K29 "định nghĩa câu cửa miệng + その一言で + 1 con số thiệt hại").
- Chưa ai trong research đọc lại toàn bộ 12 series_ctx bằng mắt người; em đọc kỹ tập 11 (đạt). h2dev soát như mọi tập.

## §4. VIỆC CỦA H2DEV
1. Ghi 12 dòng STT 11–22 vào tab `Lane-O` (dòng 12–23): cột B = `title.txt` + dịch Việt, cột C = thư mục tập, cột K = URL video gốc.
2. Chép `mau\<slug>\` sang `E:\CLAUDE\YOUTUBE\h2dev\assets\O-kaigo-sukatto\<slug>\` (không cần chép `PHAN_TICH.md`/`hook_record.json` nếu pipeline không dùng; nên giữ để tra).
3. Nạp LUẬT VIẾT hiện hành của lane vào cuối series_ctx như ep10; chạy `make_video.py --profile kaigo-sukatto --slug <slug> --den B3G` theo SOP_LANE_O.
4. Được sửa phần truyện trong `series_ctx.txt`; KHÔNG sửa [Dn] / SỐ ĐƯỢC PHÉP / mục TÌNH TIẾT CẤM CHÉP.
5. Báo cáo: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_H2DEV_LANE_O_TAP11-22_<ngày>.md`.

Dữ liệu gốc (research): `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_O_12tap_20261015\` (mỗi tập có `_src\` gồm meta, bình luận API, transcript, thumbnail) ·
nghiên cứu chọn đề tài + Studio: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_O_mo_rong_20261015\`.
