# HỒ SƠ BÀN GIAO — Lane M `teinengo-anaba` · TẬP 16 · 19/10/2026

> Từ TRENDING-RESEARCH → h2dev (máy 1 Lane M). Mở đầu mọi báo cáo: `@lane:teinengo-anaba`
> Video gốc: **`VOx2qqJpEHQ`** — 【漫画】定年後、一流の人ほど欠かさない「小さな習慣」5選【誰でも出来る】
> *(Truyện tranh: Sau nghỉ hưu, người xuất sắc càng không bỏ qua "5 thói quen nhỏ" — ai cũng làm được)*
> kênh 人生の知らせ
>
> **Thứ tự ưu tiên khi mâu thuẫn:** lời anh > `youtube-kich-ban\BAI_HOC.md` > `youtube-kich-ban\SKILL.md` >
> `docs\SOP_LANE_M.md` (K1–K12) > `docs\CONG_THUC_WIN_LANE_M.md` > hồ sơ này.
>
> ⚠️ **Tập này KHÁC khuôn 7選 của lane.** Đọc §1 và §5 TRƯỚC KHI làm bất cứ gì. Nếu chỉ đọc `CONG_THUC_WIN_LANE_M.md`
> rồi viết theo 第7位→第1位 thì tập sẽ sai hoàn toàn.

---

## 0. TL;DR cho máy 1 (đọc 60 giây là làm được)

**Đây là video BÁN 5 THÓI QUEN.** Chiếc đồng hồ chỉ là **cách giảng**, không phải nội dung. Tiêu đề hứa
"5 thói quen nhỏ — ai cũng làm được"; khán giả bấm vào vì thói quen, không vì đồng hồ.

| Việc | Nội dung |
|---|---|
| **Món hàng** | **5 thói quen**, mỗi cái = 1 hành động làm được sáng mai, có 1 con số |
| **Cách giảng** | thợ già tháo 1 chiếc 腕時計 automatic ra 5 bộ phận, mỗi bộ phận minh hoạ 1 thói quen |
| Nhân vật | 田島誠 63 (giữ nguyên K10) · vợ 春江 61 · thợ **大隅源治 76 tuổi, 48 năm nghề** |
| Đồ vật neo | 腕時計 automatic, quà chia tay của **9 người**, khắc 裏蓋 「田島さんへ 総務一同」 |
| Độ dài | 23:00–23:30 · **~8.900 chữ** (gốc 8.969) |
| Phần dẫn trước mục 1 | **25% kịch bản** (gốc: mục 1 ở phút 5:39) — KHÔNG phải 13% |
| 5 thói quen | 10,4% · 14,6% · 15,2% · 11,5% · 5,8% → cộng **57,5%** (+ nhịp sẹo thợ 1,4% = 58,9%) |
| Câu lật nghĩa | 「一流ってのはね、沼田さん、止まらない人のことじゃない。巻き直しの早い人のことです。」 ở **79,2%** |
| KHÔNG có | `第N位` · A/B/C · 「俺の答えは、最後に言う」 · sổ xanh 緑のノート |
| Hook | khuôn mới **M-D** (§3), 17–25 giây, 4 nhịp — **KHÔNG nhắc "5 thói quen"** |
| `structure_block` | phải OVERRIDE bằng khối 5 thói quen (§7) |
| Máy kiểm `kiem_cong_thuc_win.py` | sẽ báo ❌ mốc 9+10 — **đúng thiết kế**, xem §5 |

**Năm thói quen — phải đọc thuộc trước khi viết (chi tiết §2):**

| # | Thói quen | Nguyên văn | Con số |
|---|---|---|---|
| 1 | Sáng dậy **cùng một giờ**, làm đúng **một việc nhỏ** | 毎朝同じ時刻に起きて小さなことを1つやる | 6:00 · 5 phút |
| 2 | **Nhận một việc người khác nhờ**, ngoài chức danh | 肩書きの外で頼まれ事を1つ引き受ける。回せば回される | 1 việc |
| 3 | **Đi bảo dưỡng mắt–tai–răng TRƯỚC khi mờ** | 曇りになる前に目も耳も歯も手入れに出す | 6 tháng/lần |
| 4 | **Chỉnh diện mạo mỗi sáng**, dù không gặp ai | 誰に会わなくても顔を整える。1番長く会う相手は自分だから | mỗi sáng |
| 5 | **Dừng thì lên dây lại ngay**, không tự trách | 止まったら焦らずにすぐ巻き直す | 20 vòng |

---

## 1. Vì sao tập 16 dùng khuôn này (và vì sao không dùng 7選)

Video gốc **là một danh sách 5 thói quen**, kể bằng một câu chuyện. Ba tầng phải tách rõ:

| Tầng | Nội dung | Ràng buộc |
|---|---|---|
| **BÁN** (tiêu đề + thumbnail) | 5 thói quen nhỏ · đối tượng sau nghỉ hưu · "ai cũng làm được" | 5 thói quen phải đọc ra được từ tiêu đề, không cần xem |
| **GIAO** (thân bài) | 5 thói quen, mỗi cái 1 hành động làm được sáng mai | 5 thói quen = **57,5%** kịch bản (+1,4% nhịp sẹo) |
| **GIỮ CHÂN** (cách giao) | câu chuyện 田島 + thợ 大隅 + chiếc đồng hồ | phần dẫn **25,0%** + phần kết **16,1%** |

Đồng hồ sống ở tầng 3. **Nó không được lấn sang tầng 1.** Tiêu đề không nhắc đồng hồ.

Điểm khác 7選 nằm ở **đơn vị giá trị**, không phải ở số lượng:

- 7選: 1 mục = **1 món / 1 địa điểm** → bán **thông tin** ("ồ, có chỗ này à").
- Tập 16: 1 mục = **1 hành động** → bán **một việc làm được sáng mai, kèm bằng chứng nó cứu được người**.

Vì bán hành động nên **bắt buộc phải có nhân vật tái phát** (khủng hoảng ở 83,9%). Không có nó thì 5 thói quen
chỉ là 5 lời khuyên, và video chết. Đây là chỗ h2dev hay cắt nhầm nhất — xem §6.3.

Số thật của gốc (Data API, 19/10):

| | |
|---|---|
| Kênh | 人生の知らせ · **6.360 sub** · mở **28/08/2026** (52 ngày) · 7 video · 1.999.645 view tổng |
| Video | đăng 15/10/2026 · **168.196 view / 846 like / 54 comment** sau 4 ngày = **42.049 view/ngày** |
| Dài | 23:20 · 8.969 chữ · 448 segment |
| `ch_mult` | 168.196 / 6.360 = **26,4×** (kênh có công thức, không ăn may) |
| 7 video | 1.270.888 · 272.938 · 168.196 · 170.912 · 89.217 · 78.204 · 19.373 → trung vị **168.196** |

**Vì sao lấy:** khuôn này **rẻ hơn** khuôn 7選 (không cần 7 nghề có tin tuyển thật, không cần số liệu chế độ, không cần
tra 労働条件通知書) mà **giữ chân tốt hơn** (23 phút so với 17 phút). Và nó mở một trục đề tài mới cho lane M:
"thói quen / cách sống" thay vì "nghề nào".

**Vì sao không trộn:** xem §5. Hai khuôn có mốc % khác nhau, marker khác nhau, kết khác nhau.

---

## 2. NĂM THÓI QUEN — món hàng của cả video

Đoạn tổng kết ở 22:12 đọc lại đủ 5 câu, đúng thứ tự. Đây là bản phải thuộc:

> **Lưu ý ASR:** transcript tự động sai chính tả ở đúng 5 câu này — `前全朝`→毎朝 · `車肩書き`→肩書き ·
> `風貌母になれる前に`→曇りになる前に · `ズ止まったら攻めずに`→止まったら焦らずに · `先起こすも越されるもない`→先に始めるも追い越されるもない.
> Cột "Nguyên văn" là **bản đã sửa**; ASR thô ở `data/moc_chinh_xac.txt`.

| # | Thói quen (dịch trước) | Nguyên văn | Hành động làm được sáng mai | Vật neo | Con số | Vị trí |
|---|---|---|---|---|---|---|
| 1 | Sáng dậy **cùng một giờ**, làm đúng **một việc nhỏ** | 毎朝同じ時刻に起きて小さなことを1つやる | Đặt báo thức 1 giờ cố định + chọn 1 việc 5 phút làm mỗi ngày | ゼンマイ (dây cót) | **6:00** · 5 phút | 25,0–35,4% |
| 2 | **Nhận một việc người khác nhờ**, ngoài chức danh | 肩書きの外で頼まれ事を1つ引き受ける。回せば回される | Nhận 1 việc không ai muốn làm, không liên quan chức vụ | 歯車 (bánh răng) | **1 việc** | 35,4–50,0% |
| 3 | **Đi bảo dưỡng mắt–tai–răng TRƯỚC khi mờ** | 曇りになる前に目も耳も歯も手入れに出す | Đặt lịch khám mắt, đo tai, cạo vôi răng — dù chưa thấy đau | 風防 (kính mặt) | **6 tháng/lần** | 50,0–65,2% |
| 4 | **Chỉnh diện mạo mỗi sáng**, dù không gặp ai | 誰に会わなくても顔を整える。1番長く会う相手は自分だから | Cạo râu + áo có cổ + ủi, mỗi sáng, một mình | 文字盤 (mặt số) | **mỗi sáng** | 65,2–76,7% |
| 5 | **Dừng thì lên dây lại ngay**, không tự trách | 止まったら焦らずにすぐ巻き直す | Tái phát (ốm/bận/chán) thì làm lại việc nhỏ **ngay hôm sau**, không bỏ cả chuỗi | リューズ (núm lên dây) | **20 vòng** | 76,7–82,5% |

**Câu chốt của cả 5, ở 22:12 — câu quan trọng nhất của video:**

> 「どれも勤めていた頃は職場が勝手に回してくれていた歯車だ。」
> *(Cả 5 thứ này, hồi còn đi làm, công ty tự quay hộ mình: phòng vật tư tạo ra buổi sáng, có người nhờ thì mình có vai,
> khám sức khoẻ định kỳ kiểm tra thân thể, ngày nào cũng gặp người thì mặt mũi tự được chỉnh.)*

Đây là lý do 5 thói quen này **không phải lời khuyên chung**. Chúng là **5 thứ công ty từng làm hộ, và nghỉ hưu thì mất**.
Khi chuyển thể, câu này phải giữ đúng nghĩa — đổi nghề thì đổi danh sách "công ty từng làm hộ" cho khớp.

**Ba câu chốt nằm rải trong 5 thói quen — BẮT BUỘC giữ, đừng viết lại thành lời khuyên:**

| Ở thói quen | Nguyên văn | Dịch | Chức năng |
|---|---|---|---|
| 2 | 回せば回される | Mình quay nó thì nó quay lại mình | trả lời "nhận việc thì được gì" — cơ chế ăn khớp, không phải lòng tốt |
| 4 | 1番長く会う相手は自分だから | Vì người mình gặp lâu nhất là chính mình | trả lời "không ai nhìn thì chỉnh làm gì" |
| 5 → luận đề | 定年後の一流に、先に始めるも追い越されるもない | Sau nghỉ hưu, "hạng nhất" không còn chuyện khởi đầu trước hay bị vượt qua | mở cửa cho khán giả: hết đi làm thì ai cũng làm 一流 được từ sáng mai |

**Phát hiện cấu trúc (quan trọng cho người viết):** đoạn chốt 22:12 liệt kê **chỉ 4 thói quen đầu**.
**Thói quen 5 KHÔNG nằm trong danh sách "công ty từng làm hộ"** — vì nó là thứ duy nhất công ty
không bao giờ làm hộ được. Đó là lý do nó đứng cuối, ngắn nhất, và mang câu lật nghĩa.

**Thứ tự 5 thói quen là cung cảm xúc, không phải logic:** bản thân → người khác → thân thể → diện mạo → bản lĩnh.
Thói quen 5 là **luận đề** của cả video nhưng đứng **cuối và ngắn nhất** (5,8%) vì luận đề phải để dành.
Thói quen 4 là **khó nhất** (phải thừa nhận mình đã buông) nên đặt ở 65–77%, lúc người xem đã đủ tin.

---

## 3. Cấu trúc đo được của gốc (mốc = % SỐ CHỮ)

| Khối | % | Nội dung |
|---|---|---|
| A. HOOK | **1,4%** (123 chữ / 17s) | châm ngôn của thợ + chia 2 loại người + tự chiếu |
| B. TỰ GIỚI THIỆU + NỖI ĐAU | 1,4 → 8,6 | tên·tuổi·nghề · tự hạ · tiệc 11 người · quà · đồng hồ dừng · cất hộp |
| C. ĐỜI SỐNG MẤT NHỊP | 8,6 → 12,3 | mất thứ/ngày · 年賀状 17→8 · vợ thúc đi sửa |
| D. GẶP THẦY (khối giảng cơ chế) | 12,3 → 24,3 (**12,0%**) | vào tiệm · "không hỏng" · **giảng máy tự lên dây 4,3%** · 2 loại khách · định nghĩa 一流 · lời mời |
| **E. 5 THÓI QUEN** | 25,0 → 83,9 (**58,9%**) | 10,4 · 14,6 · 15,2 · 11,5 · 5,8 → cộng 57,5% + **nhịp sẹo 1,4%** |
| F. KHỦNG HOẢNG | 83,9 → 87,4 | ốm 38° 2 ngày → nghỉ 5 ngày → giọng cũ trong đầu → tự lên dây 20 vòng |
| G. NỬA NĂM SAU | 87,4 → 90,8 | montage 6 dòng, mỗi dòng 1 thói quen + 1 số nhỏ |
| H. VÒNG TRÒN | 90,8 → 94,7 | khách mới y hệt mình ở phút 0 → mình thành người trao lại |
| I. TỔNG KẾT 5 THÓI QUEN | 94,7 → 97,3 | đọc lại 5 câu |
| J. LUẬN ĐỀ + CTA | 97,3 → 100 | "khác nhau ở sáng hôm sau" + mất mát + mời bình luận |

Ba con số phải nhớ: **phần dẫn = 25,0%** · **5 thói quen = 58,9% (không đều; 5 thân bài cộng 57,5% + nhịp sẹo thợ 1,4%)** ·
**phần kết = 16,1%** (video KHÔNG kết ở thói quen 5).

Mốc chi tiết từng thói quen (giây thật): 5:39 · 8:08 · 11:42 · 15:07 · 17:42. Khủng hoảng 19:27. Vòng tròn 21:07.
Tổng kết 22:00. Luận đề 22:42. CTA 23:12.

---

## 4. HOOK — khuôn mới `M-D` (cần anh duyệt để ghi vào `M_teinengo-anaba.md`)

Hook gốc không khớp M-A / M-B / M-C. Theo `00_CHUNG.md` §1.4 → **sườn hook gốc thắng**. Đây là khuôn thứ 4 của lane.

### 4.1 Sườn 4 nhịp (gốc 17 giây / 123 chữ)

| Nhịp | % hook | Việc | Nguyên văn gốc | Dịch |
|---|---|---|---|---|
| 1 | 16% | câu khẳng định như chân lý, về **một ĐỒ VẬT**, không nói về người | 「定年した男の時計は1度止まるんです。」 | Đồng hồ của người đàn ông nghỉ hưu, kiểu gì cũng dừng một lần. |
| 2 | 23% | ai nói + tuổi + số năm nghề (uy tín bằng số, không bằng tính từ) | 商店街の外れの小さな時計屋で74歳の店主はそう言った。 | Ở tiệm đồng hồ nhỏ cuối phố chợ, ông chủ 74 tuổi nói vậy. |
| 3 | **57%** | **chia thế giới làm 2** → **mốc thời gian** → **đặt tên cho 1 nửa** | そのまま止めておく人と自分の指で巻き直す人がいる。5年経つと顔つきまで別人ですよ。巻き直す方の人を私は一流と呼んでます。 | Có người để nguyên cho dừng, có người tự tay lên dây lại. 5 năm sau mặt mũi khác hẳn. Người lên dây lại, tôi gọi là hạng nhất. |
| 4 | 14% | **tự chiếu vào mình — nửa XẤU** (mua thiện cảm, không dạy khán giả) | 俺の時計も3年前から止まったままだ。 | Đồng hồ của tôi cũng dừng từ 3 năm trước. |

### 4.2 Thông số

- **Động cơ chính: `TO_MO`** (so sánh 2 người + kết cục ra sao). **Phụ: `BI_AN`** (đồ vật "không hỏng mà vẫn dừng").
- **Cách mở giây 0:** trích lời người khác trong ngoặc kép — KHÔNG tả cảnh, KHÔNG câu hỏi người dẫn, KHÔNG tự giới thiệu.
- **Hook kết thúc ở giây 17** → vào tuyến tính (tên/tuổi/nghề/tiệc chia tay).
- **CẤM trong hook:** nhắc 65歳 bị cắt hợp đồng bằng lời · **nhắc "5 thói quen"** · nhắc tên bộ phận nào · xin đăng ký.
- Độ dài tập 16: **17–25 giây**.

**Vì sao hook KHÔNG nhắc "5 thói quen":** tiêu đề bán danh sách, hook bán câu chuyện. Nếu hook nói "hôm nay tôi có
5 thói quen" thì video tụt về listicle ngay giây 5 và mất toàn bộ lợi thế 23 phút. Hai thứ khác nhau, không được trộn.

### 4.3 Bản đồ thay chữ cho tập 16

| Nhịp | Tập 16 |
|---|---|
| 1 | 「定年した男の時計は1度止まるんです。」(Đồng hồ của người đàn ông đã nghỉ hưu, kiểu gì cũng dừng một lần.) — **giữ nguyên câu gốc**, đừng viết lại thành "腕時計", đừng thêm "một ngày nào đó" |
| 2 | tiệm đồng hồ cuối phố chợ · thợ **大隅源治 76 tuổi · 48 năm nghề** |
| 3 | chia 2 (「そのままの人」/「巻き直す人」) + mốc **5 năm** + đặt tên (KHÔNG dùng chữ 一流 ở nhịp này để dành cho câu lật nghĩa ở 79,2%) |
| 4 | 「俺の時計も3年前から止まったままだ。」(gốc 3 năm; bản ta đổi thành 4 năm cho khớp 田島 63 / 定年 60) |

---

## 5. CÔNG THỨC KỊCH BẢN — 7 quy tắc (chi tiết: `phan_tich\ep16_cong_thuc_va_hook.md`)

1. **Món hàng là 5 thói quen, không phải đồ vật.** Mỗi thói quen phải viết được thành **1 câu mệnh lệnh ≤ 20 chữ**,
   đọc lên là làm được sáng mai. Nếu một "thói quen" không viết được thành mệnh lệnh → nó là nhận xét, bỏ.
2. **Đồng hồ chỉ làm 1 việc: biến thói quen trừu tượng thành cơ chế cầm được trên tay.** Bài kiểm tra cho mỗi bộ phận:
   *"Bộ phận này làm X về mặt cơ khí, **vì thế** trong đời sống ông phải làm Y."* Không nói được câu đó → bỏ vật neo.
3. **Mỗi thói quen = đúng 5 nhịp:** ① vật + cơ chế (1–2 câu) → ② thợ **hỏi ngược** nhân vật 1 câu về **đời sống** →
   ③ **mệnh lệnh** (1 câu ngắn) → ④ **1 ví dụ thuận + 1 phản ví dụ** (người thật: tuổi + nghề cũ + 1 chi tiết lạ) →
   ⑤ **nhân vật tự làm ngay**, có 1 chi tiết hài hoặc 1 câu của vợ.
4. **Mỗi thói quen đúng 1 con số nhỏ làm được ngay hôm sau** (5 phút · 1 việc · 6 tháng · 20 vòng). Số nhục để phần B,
   số thân phận phần C, số nghề phần D, số trả giá phần F.
5. **Mục 5 cố tình THIẾU nhịp ⑤** — nhịp "làm ngay" của nó bị dời xuống **khủng hoảng ở 83,9%** (xem §6.3).
   Đây là thiết kế, không phải lỗi.
6. **Tự hạ bằng giọng hài, không bi thảm.** Gốc: 「容量の悪い男は諦めだけは容量がいい」(thằng não kém thì riêng khoản
   bỏ cuộc là rộng lượng). Cả video gần như không có từ 寂しい/悲しい — cảm xúc đi qua hành vi (cất hộp, không lật lịch,
   hỏi vợ thứ mấy).
7. **Kết 3 tầng không được rút gọn:** khủng hoảng (tự cứu, không ai cứu) → montage nửa năm (6 dòng có số) →
   **vòng tròn** (người mới bước vào y hệt mình ở phút 0, mình lặp lại câu của thầy). Cộng 1 mất mát không lấy lại.

**Câu lật nghĩa đổi nghĩa từ khoá tiêu đề, đặt 79,2%:** 「一流ってのはね、沼田さん、止まらない人のことじゃない。
巻き直しの早い人のことです。」 — đây là câu được trích nhiều nhất trong bình luận.

---

## 6. CHUYỂN THỂ — đổi gì, giữ gì

### 6.0 Giữ nguyên (là cấu trúc, KHÔNG được đổi)

- **5 thói quen, đúng thứ tự, đúng nội dung, đúng con số.**
- **5 nhịp trong mỗi thói quen.**
- Vật neo = đồng hồ cơ, 5 bộ phận, thợ già (chỉ để giảng, KHÔNG phải món hàng).
- Nhịp dẫn 25% trước thói quen 1.
- Khủng hoảng ở ~84% (nhịp ⑤ của thói quen 5).
- Kết vòng tròn ở ~91%.
- Câu chốt 22:12: *cả 5 thứ này hồi đi làm công ty tự quay hộ mình*.

### 6.1 Ba yếu tố lane M phải bơm vào (gốc KHÔNG có)

Bơm vào chỗ **đã có sẵn** để không đổi nhịp: phần B (7,2%) và phần F/G.

| Yếu tố | Cách bơm | Đặt ở % |
|---|---|---|
| **Bị hạ giá vì tuổi, có người có quyền** | 田島 63, 定年 60, làm 再雇用 3 năm ở công ty cũ; **tháng 9 vừa rồi 課長 三上 41 tuổi báo qua màn hình: 「65歳で、更新は終わりです」** — lịch sự, không nhìn mặt, không xúc phạm, không パワハラ | ~5,5% (thay chỗ "đồng hồ dừng") |
| **Mất mát bằng con số** | 再雇用 18万円 → 年金 14万円 = hụt **4万円/tháng**, 3 năm hụt **144万円**. 年賀状 **21→9**. Tiệc chia tay **9 người** (sếp cùng đợt: **40 người**) | 3,8–8,6% |
| **Quyết định tự trọng** | ~62%: 三上 gọi mời quay lại 3 tháng hợp đồng ngắn, điều kiện 「前と同じで」 → 田島 từ chối **bình tĩnh**, để lại cuốn sổ bàn giao ở **ngăn kéo thứ ba** | ~62% (trong thói quen 3) |

Ba thứ này **thay thế** chi tiết kịch tính của gốc (tiệc 11→9 người · 年賀状 17→8 thành 21→9 · ốm 38° thành 帯状疱疹)
chứ không cộng thêm → tổng độ dài và nhịp không đổi.

### 6.2 Bảng đổi

| Hạng mục | Gốc | Tập 16 | Vì sao |
|---|---|---|---|
| Nhân vật chính | 沼田豊 63 · 資材課 42 năm · 平社員 | **田島誠 63 · 総務 38 năm · 平社員** | K10; 総務 khớp chi tiết "ngày tháng trên giấy tờ chưa sai lần nào" → cộng hưởng với đồng hồ |
| Vợ | 静 | **春江 61** (part-time siêu thị) | K10 |
| Thợ | 片岡 74 tuổi · 50 năm | **大隅源治（おおすみ げんじ）76 tuổi · 48 năm** | đổi tên/tuổi/số năm |
| Đồ vật | 腕時計 automatic, quà của 11 người | **腕時計 automatic, quà của 9 người**, khắc 裏蓋 「田島さんへ 総務一同」 | giữ đồ vật (cách giảng), đổi người tặng |
| Nghề thợ | 時計店 | 時計店 (**giữ**) | đổi nghề thợ = mất 5 vật neo |
| Khủng hoảng | 風邪 38° 2 ngày · nghỉ 5 ngày | **帯状疱疹 3 ngày không ngồi dậy** · nghỉ 5 ngày | bệnh thật tuổi 60, đau hơn, không cần số y khoa |
| Khách vòng tròn | 60代 giữa · 3 ngày râu | **58 tuổi** (trẻ hơn 田島 — đau hơn) · 2 ngày râu | câu chốt sắc hơn |
| Số | 42年 · 11人 · 50人 · 17→8 · 100点 · 半月 · 450円 · 3000円 | 38年 · 9人 · 40人 · 21→9 · 90点 · 10日 · 480円 · 2.400円 | |

### 6.3 Năm thói quen — bản chuyển thể (thói quen đứng trước, bộ phận chỉ là vật neo)

| # | **THÓI QUEN** (mệnh lệnh) | Con số | Vật neo | Cơ chế 1 câu | Ví dụ thuận / phản ví dụ | Cảnh 田島 tự làm | Chữ |
|---|---|---|---|---|---|---|---|
| 1 | **6 giờ sáng dậy, làm đúng 1 việc nhỏ cố định** (đi bộ 5 phút tới góc phố rồi về) | 6:00 · 5 phút | ゼンマイ (dây cót) | Cót chỉ lên khi chủ nhân cử động; nghỉ hưu = ngừng cử động | **Thuận:** 元・給食調理員 79 — 5 giờ rưỡi nấu 1 bát canh cho mình, 12 năm chưa bỏ. **Phản:** 元・運転手 — quyết chạy 5km mỗi sáng → 3 tuần đau khớp → bỏ luôn | đặt báo thức 6 giờ; hôm đầu 5 phút, hôm thứ 3 bà hàng xóm gật đầu chào; vợ: 「朝の声が大きくなったわね」 | 930 |
| 2 | **Nhận 1 việc người khác nhờ, ngoài chức danh** | 1 việc | 歯車 (bánh răng) | 1 bánh quay không tải; phải ăn khớp bánh bên cạnh mới đẩy được kim | **Thuận:** 元・食品会社社長 75 — tự nhận việc ai cũng ngại (dọn kho, trực nhật). **Phản:** 元・工場長 78 — vẫn đòi gọi "giám đốc" → không ai nhờ nữa | mang hộ đồ cho bà Yae 88 tuổi ở chung cư trên dốc; tháng sau bà dúi hộp khoai, 「受け取るのも仕事のうち」 | 1.300 |
| 3 | **Đi khám mắt/tai/răng TRƯỚC khi thấy mờ, đau** | 6 tháng/lần | 風防 (kính mặt) | Kính mờ chậm nên chủ nhân không biết mình nhìn mờ | **Thuận:** 元・魚屋の大将 — biết nghe kém là lắp máy trợ thính ngay tháng đó, 10 năm vẫn giữa câu chuyện. **Phản:** anh trai thợ — giả vờ nghe được → nửa năm sau không ai rủ | đi tiệm kính ("sao giờ mới đến"); về mở hộp đồng hồ, đọc được tấm 寄せ書き 3 năm không đọc | 1.360 |
| 4 | **Không gặp ai vẫn chỉnh mặt mũi mỗi sáng** (cạo râu, áo có cổ) | mỗi sáng | 文字盤 (mặt số) | Mặt số là "bộ mặt"; nhìn là biết chủ. Mặt bẩn thì máy tốt cũng bị coi là rẻ | **Thuận:** 元・理容師 85 — đến lấy đồng hồ vẫn sơ mi là phẳng, tự giặt tự phơi. **Phản:** 元・営業 76 — từ ngày vợ mất mặc đồ ngủ cả ngày, không mở cửa | cạo râu trước khi đi bộ; lôi sơ mi cũ ra là, 春江 cười rồi là hộ, 「貸しなさい」 | 1.030 |
| 5 | **Dừng thì lên dây lại ngay, không tự chửi** | 20 vòng | リューズ (núm lên dây) | Đồng hồ tự động vẫn có ngày dừng; sách hướng dẫn ghi rõ phải lên tay | **Thuận:** 元・国鉄機関士 80 — mổ lưng xong, xuống viện ghé thẳng tiệm, tự lên dây: 「1月の遅れだ。ダイヤは戻せる」. **Phản:** chính 田島 trong khủng hoảng | **KHÔNG có nhịp ⑤ ở đây** → dời xuống khủng hoảng 83,9%: ốm 5 ngày, nghe lại giọng cũ trong đầu, tự lên dây 20 vòng rồi mới dậy | 520 |

**Câu lật nghĩa (79,2%, cuối thói quen 5):**
「一流ってのはね、沼田さん、止まらない人のことじゃない。**巻き直しの早い人**のことです。」
*(Hạng nhất không phải người không bao giờ dừng — mà là người lên dây lại nhanh.)*

---

## 7. `structure_block` OVERRIDE cho tập 16 (dán vào `promise.txt` + profile tạm)

```
KHUÔN TẬP 16 — 5 THÓI QUEN (KHÔNG dùng khuôn 7選).
MÓN HÀNG = 5 THÓI QUEN. Đồng hồ chỉ là CÁCH GIẢNG. Tiêu đề không nhắc đồng hồ.
MANGA CHIBI ngôi 1「俺」田島誠 63 (38 năm 総務, 平社員, 定年 60, 再雇用 3 năm) + vợ 春江 61.
ĐỒ VẬT NEO: 1 chiếc 腕時計 automatic (quà chia tay 9 người) — thợ 大隅源治 76 (48 năm) tháo ra 5 bộ phận.
5 THÓI QUEN (đúng thứ tự, mỗi cái 1 mệnh lệnh ≤20 chữ):
  1. 6 giờ sáng dậy, làm đúng 1 việc nhỏ cố định (5 phút)          ← ゼンマイ
  2. Nhận 1 việc người khác nhờ, ngoài chức danh                    ← 歯車
  3. Đi khám mắt/tai/răng TRƯỚC khi thấy mờ, đau (6 tháng/lần)      ← 風防
  4. Không gặp ai vẫn chỉnh mặt mũi mỗi sáng (cạo râu, áo có cổ)    ← 文字盤
  5. Dừng thì lên dây lại NGAY, không tự chửi (20 vòng)             ← リューズ
MỖI THÓI QUEN = 5 NHỊP CỐ ĐỊNH:
  ① vật + cơ chế (1–2 câu) → ② thợ HỎI NGƯỢC 田島 1 câu về ĐỜI SỐNG → ③ mệnh lệnh (1 câu ngắn)
  → ④ 1 ví dụ THUẬN + 1 PHẢN VÍ DỤ (người thật: tuổi + nghề cũ + 1 chi tiết lạ) → ⑤ 田島 TỰ LÀM ngay
  (1 chi tiết hài hoặc 1 câu của 春江).
THÓI QUEN 5 CỐ TÌNH THIẾU NHỊP ⑤ — nhịp "làm ngay" của nó nằm ở KHỦNG HOẢNG 83,9%. KHÔNG được cắt khủng hoảng.
KHÔNG có 第N位. KHÔNG có A/B/C. KHÔNG có 「俺の答えは、最後に言う」. KHÔNG có 緑のノート.
MỐC % (số chữ):
  hook 0–1,4 · tên/tuổi/nghề/tự hạ 1,4–3,0 · tự hào + tiệc 9 vs 40 người 3,0–4,9 · quà + khắc 裏蓋 4,9–6,9
  · đồng hồ dừng + 三上 41 tuổi báo 65歳で更新終わり (~5,5%) 6,9–8,6 · 4 năm sau mất thứ + 年賀状 21→9 8,6–10,4
  · 春江 「時計、見てもらったら?」 10,4–12,3 · vào tiệm + 「どこも壊れちゃいませんよ」 12,3–16,2
  · GIẢNG CƠ CHẾ TỰ LÊN DÂY (4,3%, KHÔNG được cắt) 16,2–20,5 · 2 loại khách + định nghĩa + lời mời 20,5–23,6
  · 3 ngày sau, 90 linh kiện 24,3–25,0
  · THÓI QUEN 1 25,0–35,4 · THÓI QUEN 2 35,4–50,0 · THÓI QUEN 3 50,0–65,2 (NÚT: 三上 gọi lại ~62%)
  · THÓI QUEN 4 65,2–76,7 · THÓI QUEN 5 76,7–82,5 (CÂU LẬT NGHĨA ở 79,2%) · vết sẹo của thợ 82,5–83,9
  · KHỦNG HOẢNG 帯状疱疹 83,9–87,4 · NỬA NĂM SAU montage 6 dòng 87,4–90,8
  · KHÁCH 58 TUỔI bước vào + vòng tròn 90,8–94,7 · TỔNG KẾT 5 câu 94,7–97,3
  · LUẬN ĐỀ + mất mát 3 năm không lấy lại + CTA 97,3–100
CÂU CHỐT BẮT BUỘC (22:12): cả 5 thói quen này hồi đi làm công ty tự quay hộ mình — nay phải tự quay.
  (Chỉ 4 thói quen đầu nằm trong danh sách "công ty làm hộ"; thói quen 5 là thứ công ty KHÔNG BAO GIỜ làm hộ.)
BA CÂU CHỐT KHÔNG ĐƯỢC BỎ: ② 「回せば回される」 · ④ 「1番長く会う相手は自分だから」
  · ⑤→luận đề 「定年後の一流に、先に始めるも追い越されるもない」
LUẬT: 三上 lạnh, bận, làm theo quy trình — KHÔNG ác, KHÔNG パワハラ. 田島 không giận, không đắc thắng.
春江 nói thẳng, câu ngắn, có chính kiến; 田島 KHÔNG quát vợ. Thoại trong「」. Cấm chữ trên hình.
```

---

## 8. Đồ vật & bối cảnh (máy 1 dựng ảnh)

| Đồ vật | Chi tiết phải đúng | Xuất hiện ở % |
|---|---|---|
| 腕時計 automatic | mặt tròn 3 kim, dây da nâu, **không thương hiệu**, 裏蓋 khắc chữ mờ 「田島さんへ 総務一同」 | 4,9 → hết |
| Hộp đồng hồ | hộp giấy nhỏ, có tấm thiệp 寄せ書き gấp trong nắp | 6,9 · 62 · 90,8 |
| Kính lúp + nhíp + khay | bàn thợ: khăn xanh, khay nhựa trắng, 90 linh kiện | 12,3 → 83,9 |
| Ảnh cũ | 田島 hồi 35 tuổi mặc sơ mi, chụp ở kho | 62 |
| 5 bộ phận tả kỹ | ゼンマイ (lò xo thép mảnh) · 歯車 (bánh răng vàng, có "răng") · 風防 (kính tròn mờ) · 文字盤 (mặt trắng số 12) · リューズ (núm nhỏ bên hông) | mỗi mục |

Bối cảnh: tiệm đồng hồ phố chợ (tường treo đồng hồ treo giá, tủ kính, bàn phủ khăn xanh) · nhà 田島 (炬燵, TV, chồng báo) ·
chung cư trên dốc (bà Yae) · tiệm kính · phòng khám.

---

## 9. Gói đăng (để TITLE-RESEARCH dùng — h2dev vẫn TẮT tiêu đề/thumbnail theo lệnh 01/10)

**Tiêu đề** — phải bán **5 thói quen**, không bán đồng hồ:
1. 【漫画】定年後、一流の人ほど欠かさない「小さな習慣」5選｜止まった時計を巻き直せない63歳 ← **khuyên dùng**
   *(Sau nghỉ hưu, người hạng nhất không bao giờ bỏ 5 "thói quen nhỏ" | Người đàn ông 63 tuổi không lên dây lại được chiếc đồng hồ đã dừng)*
2. 【漫画】定年後、時計が止まったままの男が変わるまで｜50代・60代が知らない5つの習慣
   *(Sau nghỉ hưu, cho tới khi người đàn ông có chiếc đồng hồ dừng hẳn thay đổi | 5 thói quen người 50–60 không biết)*
3. 【漫画】定年後、一流と二流を分ける5つの習慣｜再雇用を切られた63歳、4年ぶりに時計を巻く
   *(Sau nghỉ hưu, 5 thói quen phân biệt hạng nhất và hạng nhì | 63 tuổi bị cắt tái tuyển, 4 năm mới lên dây lại đồng hồ)*

**Thumbnail — khuôn KHOẢNG CÁCH 2 panel** (đúng `HO_SO_BAN_GIAO_LANE_M_5TAP.md` §2.2):
- băng trên 「定年後の過ごし方」 chữ vàng viền đen
- **trái:** 田島 ngồi 炬燵, samue, nhìn điện thoại, mặt bơ phờ · nhãn đen 「そのままの人」
- **phải:** 田島 áo sơ mi trắng + gile, cầm nhíp, mặt tập trung · nhãn đen 「巻き直す人」
- mũi tên đỏ phải→trái chỉ người bên phải
- băng dưới 「5年で顔つきが変わる」 chữ đỏ viền trắng
- **CẤM:** 1 mặt lo âu + chữ to · chữ che mặt · ghi "5選" nếu kịch bản không đủ 5 thói quen.

**Mô tả:** 4 đoạn theo gốc — (1) hoàn cảnh có số, (2) gặp thợ + câu chẩn đoán, (3) **5 thói quen nêu nhóm**, (4) lời mời cho
người đang "kim đồng hồ dừng". Hashtag `#定年後 #老後 #シニアライフ`.
**Tags:** 老後 · 定年退職 · シニアライフ · 漫画 · 60代 · 定年後 · 漫画動画 · 習慣 · 70代 · シニア.

---

## 10. Quy trình h2dev cho tập này

1. **Sheet:** tab `M-teinengo-anaba` — dòng tiếp theo sau STT 15. Research **KHÔNG** ghi tab lane; h2dev báo anh rồi ghi
   (B = tiêu đề làm việc, K = `VOx2qqJpEHQ`). **Không xoá dòng nào.**
2. `pipeline\video_goc.py` ghi `video_goc.json` với `id = VOx2qqJpEHQ` (cấm bịa ID). Thông tin kênh:
   `人生の知らせ` · `UCvAasPu0eaWHn2AU_vvk7og` · 168.196 view · 1.400 s.
3. `competitor.txt` = ASR đã có: `transcripts\VOx2qqJpEHQ.txt` (**chưa kiểm** — ASR sai: はれ→外れ · 天手→店主 ·
   裏豚→裏蓋 · 容量→要領 · 相別会→送別会 · 特計→時計 · 所斎→引き出し). Không chép nguyên văn ASR.
4. `series_ctx.txt` = danh sách CẤM nghề ep01–15 (`phan_tich\ep15_anaba_70dai.md` mục 6) + số được phép (§11) +
   **dòng miễn trừ A/B/C** (§5 hồ sơ).
5. `promise.txt` = §6.1 + §6.3 + §7 (structure_block override).
6. Chạy `--den B3G` → máy 3 → máy 2 theo `assets\M-teinengo-anaba\HUONG_DAN_TAP_TIEP_THEO.md`.

---

## 11. Số được phép (draft `series_ctx` — chưa có nguồn ngoài, đều là số hư cấu nội truyện)

**Số hư cấu của truyện (giữ đúng, cộng khớp):**
- 田島誠 63 · 定年 60 · 38 năm 総務 · 再雇用 3 năm · lương 再雇用 18万円/tháng · 年金 14万円 → hụt **4万円/tháng**
  → 3 năm hụt **144万円** (không lấy lại được).
- Tiệc chia tay **9 người** · sếp cùng đợt **40 người** · 年賀状 **21 → 9**.
- 大隅源治 76 · **48 năm** nghề · sửa **10 ngày** · **90 linh kiện**.
- 三上 41 tuổi (課長) · báo "65歳で更新終わり" tháng 9 · gọi lại mời 3 tháng ở ~62%.
- 春江 61 · part-time siêu thị.
- **5 thói quen + số nhỏ:** **6 giờ sáng** · **5 phút** đi bộ · **1 việc** được nhờ · khám mắt/tai/răng **6 tháng/lần** ·
  cạo râu mỗi sáng · **20 vòng** lên dây.
- Montage nửa năm: cà phê sáng **480円** · khám răng **2.400円** (bảo hiểm) · **tháng 1 lần** lên dây hộ bà Yae 88 tuổi ·
  **tuần 1 lần** ghé tiệm.
- 帯状疱疹: **3 ngày** không ngồi dậy · nghỉ **5 ngày**.
- Khách vòng tròn: **58 tuổi** · **2 ngày** râu.

**Số cần nguồn nếu đưa vào (K9):** tuổi nghỉ hưu 60/65 · tỉ lệ người 60+ bị 帯状疱疹 · lương hưu trung bình.
→ **Khuyến nghị: KHÔNG đưa số chế độ nào vào tập này.** Gốc không có, và bỏ đi thì kịch bản sạch hơn.

---

## 12. Không làm

- **Không** dùng `第N位` / A/B/C / 「俺の答えは、最後に言う」 / 緑のノート (khuôn khác).
- **Không** biến tập này thành video về **cấu tạo đồng hồ**. Đồng hồ là cách giảng; nếu mở đầu bằng "hôm nay tôi sẽ
  giới thiệu 5 bộ phận của đồng hồ" là sai món hàng.
- **Không** đổi 5 thói quen sang bộ thói quen khác. Đổi là đổi cả video.
- **Không** đổi đồ vật khỏi 腕時計 — đổi là mất cả 5 bộ phận.
- **Không** đổi nghề của thợ khỏi 時計店.
- **Không** cắt khủng hoảng 83,9% — đó là nhịp "làm ngay" của thói quen 5.
- **Không** chép tên nhân vật gốc (沼田/片岡/静) · không chép câu thoại gốc · không dùng số gốc (42年/11人/17→8/450円).
- **Không** đổi nhân vật chính 田島誠 63 + 春江 (K10).
- **Không** nêu tên thương hiệu đồng hồ thật (SEIKO/ROLEX…) dù bình luận gốc nhắc nhiều.
- **Không** đưa 帯状疱疹 kèm tỉ lệ/tên thuốc — chỉ "đau, 3 ngày không ngồi dậy".
- **Không** chạy `channel_analyzer.py` cho kênh 人生の知らせ.

---

## 13. Rủi ro / chưa làm (nói thẳng)

1. **Chưa có bản dịch chính thức** — toàn bộ dựa trên ASR tiếng Nhật. Đã sửa lỗi ASR khi trích, nhưng **không** dùng
   nguyên văn ASR để chép câu.
2. **Chưa xác minh 帯状疱疹** bằng nguồn y khoa → chỉ dùng định tính.
3. **Chưa kiểm 10 nhân vật ví dụ mới** có trùng danh sách CẤM nghề ep01–15 không (đây là *nhân vật ví dụ*, không phải
   mục xếp hạng, nhưng vẫn nên soát trước khi viết).
4. **Xung đột công thức §5 là rủi ro lớn nhất** — nếu máy 1 chạy máy kiểm mặc định rồi sửa kịch bản cho đạt, tập sẽ hỏng.
5. **Khối giảng cơ chế 4,3% (382 chữ liền không có cảnh hành động)** là chỗ dễ mất người xem nhất. Gốc vẫn thắng nên
   giả định giữ được, nhưng nếu bản của mình tụt giữ chân thì đây là chỗ cắt đầu tiên — và cắt thì mất luôn vật neo của cả 5 thói quen.
6. **Chưa thử** khuôn M-D trên kênh mình lần nào. Đây là tập đầu → nên xem giữ chân 30 giây đầu sau khi đăng.
7. **Bản phân tích đầu tiên của tôi sai** (lấy "đồ vật 5 bộ phận" làm món hàng thay vì 5 thói quen) — anh đã bắt.
   Bản này sửa lại; số đo giữ nguyên vì số đo vốn đúng, chỉ cách đọc sai.

---

## 14. Thư mục hồ sơ

```
E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneM_tap16_2026-10-19\
├── HO_SO_BAN_GIAO_LANE_M_TAP16.md          (file này)
├── GIAO_VIEC_LANE_M_TAP16_2026-10-19.md    phiếu việc cho máy 1
├── BAO_CAO_TAP16.html                      bản có ảnh cho anh duyệt
├── phan_tich\ep16_cong_thuc_va_hook.md     công thức 7 quy tắc + hook + 5 thói quen chi tiết
├── transcripts\
│   ├── VOx2qqJpEHQ.txt                     ASR có timestamp 0–150s (chưa kiểm)
│   └── VOx2qqJpEHQ.full.json               448 segment có start/dur (dùng để đo %)
├── thumbs\VOx2qqJpEHQ.jpg                  thumbnail gốc
└── data\
    ├── video.json                          metadata Data API (view/like/comment/duration/tags)
    ├── channel_videos.json                 7 video kênh + about (sub/ngày mở/tổng view)
    ├── comments.json · comments_doc.txt    29 bình luận (đọc được)
    ├── cau_truc_do_duoc.txt                đo cấu trúc theo % chữ
    ├── moc_chinh_xac.txt                   mốc % đo bằng chuỗi ký tự (bản chính xác)
    ├── moc_va_so_lieu.txt                  mốc % + nhân vật ví dụ + số lặp
    └── hook_0_150s.txt                     hook 0–150s bản ASR có timestamp
```

Bản sao trong repo nghiên cứu:
`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\LANE_M_TAP16_HANDOFF.md` ·
`E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\LANE_M_TAP16_BAO_CAO.html` ·
dữ liệu thô `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\lane_M_tap16\`
