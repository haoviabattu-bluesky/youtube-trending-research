# Lane Q — TẬP 3 & TẬP 5: từ khoá + tiêu đề + phong cách thumbnail

**Ngày đo:** 2026-10-18 · **Nguồn:** YouTube Suggest (keyless) + InnerTube search (cửa sổ 7 ngày / 30 ngày) + Google Trends RSS JP + Google web autocomplete
**Mẫu đối thủ:** 52 tiêu đề / 3 kênh cùng định dạng (ずんだ探検隊 · ニッポンすんだ村 · すんだ観察所) + 18 thumbnail video thắng
**Script đo:** `scratch_analysis/laneq_kw_suggest.py`, `laneq_kw_supply.py`, `laneq_winning_titles.py`, `laneq_rivals.py`, `laneq_title_structure.py`, `laneq_title_tokens.py`, `laneq_thumbs.py`, `laneq_kw_final.py`, `laneq_verify_pick.py`

---

## 1. CHẨN ĐOÁN — vì sao 2 tiêu đề hiện tại không thắng

| | ep03 hiện tại | ep05 hiện tại | Đối thủ thắng (trung vị 52 tiêu đề) |
|---|---|---|---|
| Độ dài phần **lõi** (bỏ 【】) | **78 ký tự** | 41 ký tự | **32,5 ký tự** (top 15: 34) |
| Câu khinh trong 「」 | 34 ký tự (2 mệnh đề) | 9 ký tự ✔ | 2–12 ký tự, **1 mệnh đề** |
| Từ khoá chính | `訪日客 過去最多` | `張本は口だけ` | — |
| Cầu của từ khoá đó | **cung 3 video/7d, 282 view, cầu 2 → yếu** | `張本 ブーイング` cầu **10** | — |

**Kết luận 1:** ep03 dài gấp **2,4×** đối thủ. Trên mobile YouTube cắt ở ~40 ký tự → người xem chỉ thấy `中国「日本行きの便を全部禁止しろ！日本の航空会社なんか…` — tức là thấy **câu khinh dài dòng**, KHÔNG thấy kết quả đảo chiều. Mất toàn bộ phần thưởng.

**Kết luận 2:** ep03 chọn đúng *ý* nhưng sai *từ khoá*. `訪日客 過去最多` gần như không ai search (cung 3 video/7 ngày, tổng 282 view). Trong khi `中国 航空会社` = 140.283 view/7 ngày, và `中国人観光客 減った` = cầu 8 nhưng cung chỉ 20k → **khoảng trống**.

**Kết luận 3 (quan trọng, ngược trực giác):** đối thủ thắng **KHÔNG dùng con số**. Tỷ lệ có số+đơn vị trong tiêu đề: ずんだ探検隊 **0/10**, ニッポンすんだ村 **2/10**, すんだ観察所 **1/10** — toàn mẫu 52 tiêu đề chỉ **12%**. Cái họ dùng là **động từ sụp đổ** (崩壊 9 lần, 赤字 3, 末路 3, 地獄 3, 撤退 3).

---

## 2. TỪ KHOÁ ĐO ĐƯỢC — bảng cầu × cung

Cầu = số gợi ý autocomplete. Cung = video + view trong 7 ngày (InnerTube `window=week`).

### Tập 3 — hãng bay TQ lỗ

| Từ khoá | Cầu | Video/7d | ≥10k | View 7d | Chấm |
|---|---|---|---|---|---|
| `中国 航空会社` | 4 | 10 | 2 | **140.283** | 🔥 dùng làm từ khoá chính |
| `中国人観光客 激減` | 2 | 10 | 2 | 64.142 | ✅ dùng được |
| `中国人観光客 減った` | **8** | 5 | 1 | 20.075 | 🟢 **khoảng trống tốt** |
| `中国 航空会社 赤字` | ✔ | 1 | 0 | 4.241 | ✅ cụm phụ |
| `中国人観光客 来なくていい` | 0 | 2 | 1 | **605.735** | 🔥 cầu ẩn cực lớn (xem cảnh báo) |
| `訪日客 過去最多` | 2 | 3 | 0 | **282** | ❌ **từ khoá chết — đang dùng trong ep03** |
| `訪日外国人 過去最多` | 2 | 3 | 0 | 307 | ❌ chết |
| `中国 航空会社 やばい` | ✔ | 0 | 0 | 0 | ❌ chết |

> ⚠️ `中国人観光客 来なくていい` có 1 video **603.559 view/72h** (`XEd5ey3TD00`, kênh 世界観測部) — nhưng nội dung video đó là *"TQ tự xưng vô địch du lịch → không ai đến, phố vắng"*, tức là **phố TQ vắng khách**, KHÔNG phải nội dung tập 3 (Nhật đón khách kỷ lục + hãng bay TQ lỗ). **Không bê cụm này vào tiêu đề ep03** — sẽ là tiêu đề sai nội dung, giữ chân kém và mất uy tín kênh.

### Tập 5 — bóng bàn TQ

| Từ khoá | Cầu | Video/7d | ≥10k | View 7d | Chấm |
|---|---|---|---|---|---|
| `松島輝空` | 10 | 40 | **40** | **2.399.793** | 🔥 cầu lớn nhất ngách |
| `張本智和 中国` | 10 | 40 | 9 | 587.686 | 🔥 |
| `卓球 世界1位` | 2 | 40 | 10 | 617.156 | 🔥 |
| `張本 ブーイング` | **10** | **0** | 0 | **0** | 🟢 **khoảng trống vàng** (cầu 10, cung 0) |
| `卓球 中国 日本` | ✔ | 40 | 5 | 239.118 | ✅ |
| `卓球 46年ぶり` | ✔ | 5 | 2 | 50.968 | ✅ cụm phụ |
| `中国 卓球 崩壊` | 0 | 0 | 0 | 0 | ❌ chết |
| `中国 卓球 弱くなった` | 0 | 0 | 0 | 0 | ❌ chết |

> 🎯 `張本 ブーイング`: **cầu 10 nhưng 0 video trong 7 ngày** → đúng nghĩa khoảng trống. Từ khoá này phải nằm trong tiêu đề.

### Google Trends JP — đối chiếu
RSS trending JP (`geo=JP`, HTTP 200) hôm nay **không có** 中国 / 訪日 / 観光 / 航空 / 卓球 / 張本 / 松島. → Hai đề tài này **không phải tin nóng toàn quốc**, chúng là **ngách có khán giả riêng ổn định** (view đều đặn 300k–800k/video ở kênh đối thủ). Đừng chờ trend, hãy đánh vào **từ khoá ngách**.

---

## 3. KHUÔN TIÊU ĐỀ ĐANG THẮNG — bóc từ 52 tiêu đề

| Đặc điểm | Toàn mẫu | Top 15 |
|---|---|---|
| Mở bằng `「câu khinh」` | **87%** | **87%** |
| Có `結果` | 69% | **93%** |
| Kết bằng `【海外の反応…】` | 90% | 87% |
| Có `ｗ` | 77% | 67% |
| Có `…` (gợi mở) | 40% | 40% |
| Có số + đơn vị | **12%** | 7% |
| Có tên công ty/thương hiệu | 27% | 20% |

**Khuôn chuẩn (đo được, không suy đoán):**

```
<chủ thể>「<câu khinh 4–12 chữ>」→結果、<hậu quả 8–16 chữ>ｗ【海外の反応・ゆっくり解説】
└────────────── lõi 30–36 ký tự ──────────────┘
```

15 câu khinh thắng nhất (nguyên văn): 「日本は謝罪しろ！」878k · 「日本人はクソ！」765k · 「ビザ代で報復してやる！」667k · 「日本を超えたぞ！」647k · 「日本はもう用済みだｗ」622k · 「日本を干上がらせてやる！」577k · 「トヨタは時代遅れｗ」491k · 「わーくにから出るなｗ」464k · 「上海が世界一！」424k.

→ **Câu khinh phải NGẮN và NGÔNG CUỒNG**, không cần đúng chi tiết chính sách. Đây là chỗ ep03 sai nặng nhất.

---

## 4. TIÊU ĐỀ ĐỀ XUẤT

### Tập 3 — hãng bay TQ lỗ

**① Ưu tiên `中国 航空会社` (cầu 4 · 140k view/7d)**
```
中国「日本便を全部止めろ！」→結果、自国の航空会社3社が赤字で沈むｗ【海外の反応・ゆっくり解説】
```
Lõi 36 ký tự. Đúng khuôn 87%/93%. Từ khoá `中国 航空会社` + `日本便` nằm trong 40 ký tự đầu.

**② Ưu tiên `中国人観光客 減った` (cầu 8 · khoảng trống)**
```
中国「日本へ行くな！」→結果、中国人観光客だけ消えて日本は過去最多ｗ【海外の反応・ゆっくり解説】
```
Lõi 38. Đánh vào khoảng trống cầu 8/cung 20k. Giữ được cả 2 vế đảo chiều.

**③ Ưu tiên `中国人観光客 激減` (cầu 2 · 64k view/7d)**
```
中国「日本へ行くな！」→結果、中国人観光客が激減して自国が大赤字ｗ【海外の反応・ゆっくり解説】
```
Lõi 37. Ngắn nhất, dễ đọc nhất trên mobile.

> Cả 3 đều đúng nội dung: khách TQ giảm 56% (thật), tổng khách vào Nhật tháng 7 kỷ lục (thật), 3 hãng bay TQ lỗ gần 2000 tỷ yên nửa năm (thật). Không có vế nào sai.

### Tập 5 — bóng bàn TQ

**① Ưu tiên `張本 ブーイング` (cầu 10 · cung 0 = khoảng trống vàng)**
```
中国「張本は口だけｗ」→結果、ブーイングした中国が世界ランクから消えるｗ【海外の反応・ゆっくり解説】
```
Lõi 41. Giữ câu khinh gốc (D2 thật) + nhét đúng cụm cầu-10-cung-0.

**② Ưu tiên `松島輝空` (cầu 10 · 2,4 triệu view/7d — lớn nhất ngách)**
```
中国「日本人はリーグに入れるな！」→結果、8年後その日本に世界1位を奪われるｗ【海外の反応・ゆっくり解説】
```
Lõi 43. Câu khinh thật (D40, giải VĐQG TQ 2017 từ chối tuyển thủ Nhật). Thêm `松島輝空` vào tag + mô tả.

**③ Ưu tiên `卓球 世界1位` (cầu 2 · 617k view/7d)**
```
中国「負けたのはポイント制度のせい」→結果、金も世界1位も日本に持っていかれるｗ【海外の反応・ゆっくり解説】
```
Lõi 43. Câu khinh thật (D26).

> Cả 3 dùng câu khinh **có nguồn [Dn] thật**, không bịa phát ngôn — đúng LUAT §0.

### 4b. DỊCH TIẾNG VIỆT — 6 tiêu đề đã chọn

Đuôi chung `【海外の反応・ゆっくり解説】` = **"Phản ứng từ nước ngoài・giải thích kiểu Yukkuri"** (giữ nguyên tiếng Nhật khi đăng, chỉ dịch để anh đọc).

**TẬP 3 — hãng bay TQ lỗ**

| # | Tiêu đề Nhật | Dịch nghĩa |
|---|---|---|
| ① | 中国「日本便を全部止めろ！」→結果、自国の航空会社3社が赤字で沈むｗ | TQ: **"Cấm sạch mọi chuyến bay sang Nhật đi!"** → kết quả: **3 hãng hàng không của chính nó chìm nghỉm trong thua lỗ** ｗ |
| ② | 中国「日本へ行くな！」→結果、中国人観光客だけ消えて日本は過去最多ｗ | TQ: **"Đừng có đến Nhật nữa!"** → kết quả: **chỉ khách du lịch TQ là biến mất, còn Nhật thì đạt mức cao nhất lịch sử** ｗ |
| ③ | 中国「日本へ行くな！」→結果、中国人観光客が激減して自国が大赤字ｗ | TQ: **"Đừng có đến Nhật nữa!"** → kết quả: **khách du lịch TQ giảm sâu, chính nước nó lỗ nặng** ｗ |

**TẬP 5 — bóng bàn TQ**

| # | Tiêu đề Nhật | Dịch nghĩa |
|---|---|---|
| ① | 中国「張本は口だけｗ」→結果、ブーイングした中国が世界ランクから消えるｗ | TQ: **"Harimoto chỉ được cái miệng thôi ｗ"** → kết quả: **chính TQ — nước đã la ó — biến mất khỏi bảng xếp hạng thế giới** ｗ |
| ② | 中国「日本人はリーグに入れるな！」→結果、8年後その日本に世界1位を奪われるｗ | TQ: **"Cấm không cho người Nhật vào giải!"** → kết quả: **8 năm sau, chính nước Nhật đó cướp mất ngôi số 1 thế giới** ｗ |
| ③ | 中国「負けたのはポイント制度のせい」→結果、金も世界1位も日本に持っていかれるｗ | TQ: **"Thua là tại cái cách tính điểm đấy"** → kết quả: **cả HCV lẫn ngôi số 1 thế giới đều bị Nhật lấy đi** ｗ |

**Vì sao chọn câu khinh đó (dịch nghĩa là hiểu ngay cơ chế click):**
- `日本便を全部止めろ` — mệnh lệnh tuyệt đối, nghe như TQ nắm quyền sinh sát. Đọc xong là muốn xem TQ sụp.
- `日本へ行くな` — 4 chữ, ai cũng hiểu trong 0,5 giây. Đây là câu khinh ngắn nhất trong 6 phương án.
- `張本は口だけｗ` — có `ｗ` ngay trong câu khinh = TQ vừa khinh vừa tự tin, càng đau khi thua.
- `リーグに入れるな` — "cấm cửa", đúng sự thật D40, và tạo khoảng lùi 8 năm để bõ tức.
- `ポイント制度のせい` — câu chối tội hèn nhất, khán giả ghét nhất → click mạnh nhất.

---

## 5. PHONG CÁCH THUMBNAIL ĐANG THẮNG

Bóc từ 18 thumbnail thật + zoom 1 ca vàng (`XEd5ey3TD00`, 603k/72h).

### 6 luật lặp ở gần như TẤT CẢ ảnh thắng

1. **Bố cục bánh kẹp 3 tầng:** chữ to TRÊN (1 dòng) → ảnh cảnh ở GIỮA → chữ to DƯỚI (1 dòng). Không phải 5 dòng như thumb ep03 hiện tại.
2. **Chữ tối đa 2 dòng chính + 1 bubble thoại.** Cỡ chữ lớn chiếm ~1/3 khung. Font đậm, viền đen dày.
3. **Màu chữ:** vàng trên (viền đen) + xanh dương hoặc hồng/tím dưới (viền trắng + bóng đen). Nền tối để chữ bật.
4. **Một nhân vật hoạt hình phản ứng ở góc phải:** mặt toát mồ hôi, ôm đầu, mắt nhắm, cười gượng. Nhân vật này = "phía thua".
5. **Cảnh nền là HIỆN TRƯỜNG của hậu quả**, không phải biểu tượng trừu tượng: phố vắng tanh, cửa cuốn kéo hết, cờ đỏ bạc màu, rác, cỏ mọc. Có bảng hiệu tiếng Nhật/Trung để định vị quốc gia.
6. **Bubble thoại ngắn 3–5 chữ** cạnh mặt nhân vật: 「誰も来ない…」.

### Không bắt buộc (đã kiểm, đừng máy móc)
- Cờ Trung Quốc: có ở nhiều ảnh nhưng **không có** ở ca 603k view.
- Mũi tên đỏ / X đỏ / khoanh đỏ: chỉ một phần ảnh có. Không phải yếu tố quyết định.
- ゆっくり: mô tả ban đầu nói "gần như tất cả", nhưng ca vàng 603k **không có** ゆっくり — dùng nhân vật hoạt hình thường (doanh nhân vest + cà vạt đỏ). → Nhân vật phản ứng quan trọng hơn loại nhân vật.

### Thumbnail ep03 hiện tại sai 4/6 luật

| Luật | Thắng | ep03 hiện tại |
|---|---|---|
| 2 dòng chữ chính | ✔ | ❌ **5 dòng** chữ cỡ khác nhau |
| 1 nhân vật phản ứng góc phải | ✔ | ✔ có, nhưng tranh chấp với 4 yếu tố khác |
| Cảnh hiện trường hậu quả | ✔ | ❌ nền gradient xanh xám trừu tượng + máy bay |
| Tương phản cao | ✔ | ❌ chữ tím-hồng trên nền tối, chữ trắng trên trời xám → khó đọc |
| Định vị quốc gia bằng bảng hiệu | ✔ | ❌ không có |
| Chủ thể rõ | ✔ | ❌ 5 yếu tố tranh nhau (biển cấm, nhãn đỏ, mũi tên, máy bay, mặt sốc) |

**Đề xuất dựng lại ep03:** nền = **sân bay vắng / quầy vé đóng cửa cuốn**, bảng hiệu tiếng Trung mờ; chữ trên vàng 「日本便が消えた中国」; chữ dưới xanh 「航空3社が赤字で沈む」; góc phải mặt doanh nhân ôm đầu + bubble 「便が飛ばない…」. Bỏ hẳn 2000億円 khỏi ảnh (số liệu chỉ 12% ở tiêu đề thắng, và trên ảnh còn khó đọc hơn).

**ep05 chưa có thumbnail** (cột thumbnail trong Sheet trống) → dựng theo: nền sân đấu bóng bàn tối, chữ trên vàng 「口だけｗ」, chữ dưới xanh 「世界1位は日本」, góc phải mặt sốc + bubble 「ありえない…」. **Không dùng mặt VĐV thật** (HO_SO §1: quyền hình ảnh) — dùng nhân vật hư cấu.

### 5b. GIẢI THÍCH CHỮ TRÊN THUMBNAIL (dịch từng dòng)

#### A. Thumbnail VÀNG đang thắng — `XEd5ey3TD00` (603.559 view / 72h)

| Vị trí | Chữ Nhật | Dịch nghĩa | Vai trò |
|---|---|---|---|
| Trên (vàng, viền đen) | 旅行客が消えた中国 | **"Trung Quốc nơi du khách biến mất"** | Câu dẫn — định vị quốc gia + nêu hiện tượng |
| Dưới (xanh, viền trắng) | 観光地がガラガラで終了 | **"Điểm du lịch vắng tanh → hết cứu"** | Câu kết — phán quyết sụp đổ (`終了` = "xong rồi/hết") |
| Bubble cạnh mặt | 誰も来ない… | **"Chẳng ai đến cả…"** | Tiếng lòng phía thua |
| Bảng hiệu nền trái | 中国特産 / 土産物 | **"Đặc sản TQ" / "Đồ lưu niệm"** | Chi tiết định vị — cửa hàng đã đóng |
| Bảng hiệu nền phải | 観光 | **"Du lịch"** | Cùng mục đích |
| Cổng vòm xa | 観光街 | **"Phố du lịch"** | Cùng mục đích |

**Cơ chế:** `ガラガラ` (vắng tanh, tiếng lon lăn) + `終了` (hết) là 2 từ tiếng Nhật rất mạnh — không cần con số, chỉ cần 2 từ này là người xem hiểu "phe kia đã sụp". Đây là lý do thumb này ăn 603k dù không có 2000億円 nào trên ảnh.

#### B. Thumbnail ep03 HIỆN TẠI (đang thất bại)

| Vị trí | Chữ Nhật | Dịch nghĩa |
|---|---|---|
| Banner đen trên | 「日本の航空会社を潰せ！」 | **"Đè bẹp hãng bay Nhật đi!"** |
| Nhãn đỏ trái | 全便禁止！ | **"Cấm toàn bộ chuyến bay!"** |
| Trắng giữa | → 自国の航空3社が | **"→ 3 hãng bay của chính nước nó thì…"** |
| Vàng giữa | 2000億円近い赤字 | **"lỗ gần 2000 tỷ yên"** |
| Hồng-tím dưới | 日本は7月過去最多w | **"Nhật tháng 7 cao nhất lịch sử w"** |

→ 5 dòng, mỗi dòng một cỡ chữ, 3 tông màu khác nhau. Trên điện thoại thu nhỏ còn ~1/6 → **không đọc được dòng nào trọn vẹn**. So với thumb thắng chỉ 2 dòng chính.

#### C. Thumbnail ep03 ĐỀ XUẤT (bố cục mới)

| Vị trí | Chữ Nhật | Dịch nghĩa | Ghi chú |
|---|---|---|---|
| Trên (vàng, viền đen) | 日本便が消えた中国 | **"Trung Quốc nơi chuyến bay sang Nhật biến mất"** | 9 chữ, 1 dòng, đọc trong 1 giây |
| Dưới (xanh, viền trắng) | 航空3社が赤字で沈む | **"3 hãng bay lỗ nặng chìm nghỉm"** | Kết quả sụp đổ, có số `3` |
| Bubble cạnh mặt | 便が飛ばない… | **"Chuyến bay không cất được…"** | Tiếng lòng phía thua |
| Bảng hiệu nền | 出発 / 欠航 | **"Khởi hành" / "Hủy chuyến"** | Định vị sân bay, chi tiết đắt |

**Đã cắt khỏi ảnh:** `2000億円近い赤字` (quá dài, khó đọc trên mobile) và `日本は7月過去最多` (đưa vào tiêu đề + mô tả là đủ). Ảnh chỉ giữ **1 câu dẫn + 1 câu kết**.

#### D. Thumbnail ep05 ĐỀ XUẤT (chưa có thumb nào)

| Vị trí | Chữ Nhật | Dịch nghĩa | Ghi chú |
|---|---|---|---|
| Trên (vàng, viền đen) | 「口だけｗ」 | **"Chỉ được cái miệng ｗ"** | Nguyên văn câu khinh của TQ — 4 chữ, cực mạnh |
| Dưới (xanh, viền trắng) | 世界1位は日本 | **"Số 1 thế giới là Nhật"** | Đảo chiều, có số `1` |
| Bubble cạnh mặt | ありえない… | **"Không thể nào…"** | Sốc, phía thua |
| Bảng hiệu nền | 世界ランキング / 中国圏外 | **"BXH thế giới" / "TQ ngoài top"** | Chi tiết định vị môn bóng bàn |

**Cấm:** không dùng mặt 張本 / 松島 thật (quyền hình ảnh, HO_SO §1) — dùng nhân vật hoạt hình hư cấu mặc vest, mặt tái, ôm đầu.

---

## 6. ĐÃ THỰC HIỆN (anh duyệt 18/10/2026 — chọn tiêu đề ①, cho phép vẽ thumb + thay)

### 6a. Tiêu đề đã thay LIVE (verify bằng HTTP đọc lại trang watch)

| Tập | Video | Tiêu đề LIVE | Verify |
|---|---|---|---|
| ep03 | `f7xhMrUmFug` | 中国「日本便を全部止めろ！」→結果、自国の航空会社3社が赤字で沈むｗ【海外の反応・ゆっくり解説】 | ✅ khớp 100% |
| ep05 | `ZJauO_vPW9E` | 中国「張本は口だけｗ」→結果、ブーイングした中国が世界ランクから消えるｗ【海外の反応・ゆっくり解説】 | ✅ khớp 100% |

Đã xoá sạch tiêu đề cũ (ep03 cũ 87 ký tự không có đuôi kênh; ep05 cũ 76 ký tự).

### 6b. Thumbnail đã thay LIVE (verify bằng pixel-diff ảnh tải từ YouTube)

| Tập | Ảnh | Dải trên | Dải dưới | Pixel-diff |
|---|---|---|---|---|
| ep03 | `thumb_v2/thumb.png` (808.829 B) | 「日本便を全部止めろ！」 | 自国の航空会社3社が赤字で沈む | **0,46** → KHỚP |
| ep05 | `thumb_v2/thumb.png` (615.850 B) | 「口だけｗ」の中国 | 世界1位は日本 | **0,54** → KHỚP |

Diff < 1/255 = ảnh trên YouTube chính là ảnh mình dựng (không phải cache ảnh cũ).
URL công khai: `https://files.catbox.moe/9s3zuk.png` · `https://files.catbox.moe/tbdjv7.png`

### 6c. Sheet `Lane-Q` đã ghi

- Dòng 4 (ep03): E = tiêu đề mới, G = URL thumb, K = `ĐÃ THAY TIÊU ĐỀ + THUMB 18/10/2026`, tô xanh A→S
- Dòng 6 (ep05): E = tiêu đề mới, G = URL thumb, K = `ĐÃ THAY TIÊU ĐỀ + THUMB 18/10/2026`, tô xanh A→S
- **Giữ nguyên:** dòng 2+ cột E (mô tả + mục lục), cột F (tag: ep03 22 tag, ep05 0 tag như cũ)
- **Không đụng:** `GMAIL` (112 dòng) · `NOTE` (27 dòng)

### 6d. Việc còn lại (không thuộc lượt này)
- ep05 vẫn lỗi render QC `C3 nhay 1 khung o 620.70s` — thumb/tiêu đề đã cứu được phần hiển thị, nhưng video chưa render lại được.
- Theo dõi CTR 24h sau 18/10; nếu vẫn "—" thì vấn đề nằm ở nội dung/khung giờ đăng, không phải tiêu đề.

*Cập nhật 18/10/2026 — đã thay thật trên YouTube + Sheet.*
