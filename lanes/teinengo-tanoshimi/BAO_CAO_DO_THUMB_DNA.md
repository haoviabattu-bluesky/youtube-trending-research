# BÁO CÁO ĐO DNA THUMBNAIL — LANE G `teinengo-tanoshimi` (定年後の楽しみ方)

Đo ngày 2026-09-22 · **20 thumbnail THẮNG + 5 THUA** · 5 kênh 漫画 hưu trí Nhật · quét 97 video. Toàn bộ số liệu do MÁY đo (OpenCV + rapidocr), không hỏi model ngôn ngữ; chỗ nào do mắt đối chiếu đều ghi rõ.

Kết quả: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-tanoshimi\thumb_dna.json` (hợp lệ 100 % theo `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\thumb_dna.schema.json`) + `thumbs\win\*.jpg` (20) + `thumbs\lose\*.jpg` (5).

## 1. Chọn mẫu (breakout theo TỪNG kênh)

THẮNG = view ≥ **2×** trung vị của CHÍNH kênh đó **và** ≥ 10.000 view (sàn tuyệt đối, để kênh tí hon không định hình DNA). THUA = ≤ 0,5× trung vị, ≥ 500 view, bỏ 3 video mới nhất (video vừa đăng chưa kịp chạy không phải mẫu thua).

| Kênh | ID | Video quét | Trung vị view | THẮNG | THUA |
|---|---|---|---|---|---|
| 老後のお金ストーリー | `UCI2cPqBmCPMxxKI4u2Gqs_Q` | 19 | 16,000 | 9 | 4 |
| 老後のゴローさん | `UCxD2Exs2Q4lf7x0Q28OuKvg` | 45 | 29,000 | 17 | 12 |
| 人生の果実【漫画】 | `UCjlh_Ko4lEpJIqftz5mxNXQ` | 12 | 37,000 | 5 | 2 |
| 老後の暮らし研究所 | `UCRkP44Mcw-K8IktdTqxC9dg` | 14 | 10,500 | 6 | 1 |
| 定年後の楽しみ図鑑 | `UCdN_h3ClY8tfQRfIBv2HZVw` | 7 | 1,000 | 0 | 0 |

Mẫu đã lấy (cân đều, tối đa 6 video/kênh):

| Nhóm | Video | View | ×median | Kênh | Tiêu đề |
|---|---|---|---|---|---|
| THẮNG | `Scnn76gZ8E8` | 956,000 | 32.97 | 老後のゴローさん | 【漫画】退職金で豪華クルーズ旅をした65歳夫婦のリアル…14日間で知った現実とは？ |
| THẮNG | `XbwqD2SktC0` | 310,000 | 29.52 | 老後の暮らし研究所 | 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました |
| THẮNG | `xxMKVprVh-I` | 836,000 | 28.83 | 老後のゴローさん | 【漫画】６０代・７０代夫婦の熟年離婚 VS 熟年家庭内別居、どっちが幸せなのか？ |
| THẮNG | `r4jNE1oTv8Q` | 544,000 | 18.76 | 老後のゴローさん | 【漫画】70歳でまだ働く男と、65歳で卒業した男。5年後、差がついた本当の理由とは？ |
| THẮNG | `K8tTrxijqEo` | 178,000 | 16.95 | 老後の暮らし研究所 | 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 |
| THẮNG | `O84L0zOtrxo` | 173,000 | 16.48 | 老後の暮らし研究所 | 【漫画】65歳で定年退職した男…2年後、貯金が67万円消えた本当の理由を知りました |
| THẮNG | `0YuPs8cbmMo` | 478,000 | 12.92 | 人生の果実【漫画】 | 【漫画】定年退職後に暇な男性必見…孤独を贅沢に楽しむ具体的な方法5選 |
| THẮNG | `bgUqNHYZbq0` | 199,000 | 12.44 | 老後のお金ストーリー | 【漫画】なぜか老けない50代男性が「毎日やっていること」7選…同年代と差がつく意外な共通点 |
| THẮNG | `gpVr3OYPA-E` | 349,000 | 12.03 | 老後のゴローさん | 【漫画】シニアの婚活バスツアーとは？熟年結婚は本当にあるのか？ |
| THẮNG | `VXlE3c0gqb0` | 417,000 | 11.27 | 人生の果実【漫画】 | 【漫画】他で語られていない、定年後に始める特別な趣味5選！60代から世界が広がります… |
| THẮNG | `hyLpBbmnvIA` | 322,000 | 11.1 | 老後のゴローさん | 【漫画】老後貧困のリアル、受け取る年金額による食生活の違い貧富の差がヤバ過ぎる・・・ |
| THẮNG | `BeIZhu1I4Tw` | 167,000 | 10.44 | 老後のお金ストーリー | 【漫画】一生に一度は参拝したい…定年後に行くべき格式の高い神社5選 |
| THẮNG | `_VXUim2J9QM` | 107,000 | 10.19 | 老後の暮らし研究所 | 【漫画】60歳で辞めるな！62歳で年金受給が最強な理由 |
| THẮNG | `AOe-E69mLzA` | 144,000 | 9.0 | 老後のお金ストーリー | 【漫画】定年後、最強の暇つぶし5選…実は1円もかからない楽しみ方がありました |
| THẮNG | `OIeZvtYreOg` | 233,000 | 8.03 | 老後のゴローさん | 【漫画】“脳が10歳若い”シニアが、こっそり楽しんでいる習慣とは？ |
| THẮNG | `_EhPtM6cRFk` | 112,000 | 7.0 | 老後のお金ストーリー | 【漫画】６０代から人生が驚くほど心地よくなる定年後に見つけたちょうどいい生き方５選 |
| THẮNG | `EANADckKWT4` | 71,000 | 6.76 | 老後の暮らし研究所 | 【漫画】65歳で退職した独身男…たった2か月で絶望しました |
| THẮNG | `ASBVa_H_leI` | 106,000 | 6.62 | 老後のお金ストーリー | 【漫画】夜行バスに2万円！？新幹線より高い豪華夜行バスに65歳で乗ってみた結果… |
| THẮNG | `_G9s-Ig6-E8` | 82,000 | 5.12 | 老後のお金ストーリー | 【漫画】定年後は一人旅が最高、60代から一度は行きた有名の温泉地5選 |
| THẮNG | `dY3HfjtmvXI` | 48,000 | 4.57 | 老後の暮らし研究所 | 【漫画】65歳、独身、年金生活…その先に待っていた衝撃の現実 |
| THUA | `YKjWwJZrKXY` | 1,100 | 0.07 | 老後のお金ストーリー | 【漫画】年金は何歳から受け取るべき？60歳、65歳、70歳、75歳、知らないと後悔する受給年齢の落とし穴 |
| THUA | `U5ygHCC7cSA` | 3,900 | 0.13 | 老後のゴローさん | 【漫画】持ち家35年ローン完済直後、65歳で待っていたのは？ |
| THUA | `8xEY-fMffys` | 4,100 | 0.14 | 老後のゴローさん | 【漫画】退職金2000万で"安泰"のはずが…年金開始まであと数年の58歳、貯金が消えた理由とは？ |
| THUA | `xpg0QU7V6IY` | 2,700 | 0.17 | 老後のお金ストーリー | 【漫画】「もっと早く知りたかった…」人生で本当に大事なこと |
| THUA | `PZnSNphOIrE` | 2,700 | 0.26 | 老後の暮らし研究所 | 【漫画】67歳で貯金216万円を失いました…老後のお金が消える「7つの習慣」 |

## 2. Đo từng ảnh (máy)

`cover` = tổng diện tích hộp chữ / khung · `ký tự` = max(OCR rapidocr, ước lượng hình học bề rộng÷chiều cao) · `panel` = số khung truyện đếm theo vạch trắng dọc · `Haar` = số mặt OpenCV bắt được (bộ dò mặt NGƯỜI THẬT).

| Nhóm | Video | cover | Băng trên: h/w/ký tự/màu | Nhãn vàng | Dòng chốt dưới | panel | Haar | Ô chủ thể |
|---|---|---|---|---|---|---|---|---|
| T | `Scnn76gZ8E8` | 0.510 | 0.232/0.986/8/#F6F7EC | 2 | 0.254/0.957/#F9EBE9 | 3 | 2 | giữa-giữa |
| T | `XbwqD2SktC0` | 0.309 | 0.189/0.774/7/#F7F6F9 | 3 | — | 4 | 6 | dưới-giữa |
| T | `xxMKVprVh-I` | 0.325 | 0.222/1.000/13/#F5F5F5 | 2 | — | 9 | 6 | dưới-phải |
| T | `r4jNE1oTv8Q` | 0.315 | 0.228/0.972/16/#F5F5EF | 4 | — | 2 | 5 | giữa-trái |
| T | `K8tTrxijqEo` | 0.317 | 0.190/0.785/7/#EEEEF0 | 2 | 0.100/0.524/#F6F4F3 | 4 | 3 | dưới-phải |
| T | `O84L0zOtrxo` | 0.434 | 0.188/1.000/9/#F5F4F6 | 3 | 0.181/0.868/#F0E3D3 | 3 | 2 | dưới-phải |
| T | `0YuPs8cbmMo` | 0.513 | 0.203/0.806/7/#EFD630 | 4 | 0.321/0.786/#F5E8E2 | 5 | 5 | giữa-phải |
| T | `bgUqNHYZbq0` | 0.215 | 0.190/0.623/6/#EFF13B | 2 | — | 4 | 2 | dưới-phải |
| T | `gpVr3OYPA-E` | 0.272 | 0.136/1.000/13/#F6F6F6 | 3 | 0.104/0.818/#F4DBD9 | 3 | 5 | giữa-phải |
| T | `VXlE3c0gqb0` | 0.210 | 0.196/0.921/13/#EFD633 | 4 | — | 4 | 4 | giữa-giữa |
| T | `hyLpBbmnvIA` | 0.323 | 0.212/0.986/12/#F7F7F7 | 5 | — | 4 | 6 | dưới-phải |
| T | `BeIZhu1I4Tw` | 0.322 | 0.190/0.407/4/#ECEE1D | 0 | 0.290/0.738/#EEDFDE | 1 | 3 | giữa-trái |
| T | `_VXUim2J9QM` | 0.262 | 0.190/0.774/7/#F7F6F9 | 4 | — | 4 | 3 | dưới-giữa |
| T | `AOe-E69mLzA` | 0.210 | 0.175/0.984/10/#EEEEEE | 5 | — | 1 | 3 | giữa-giữa |
| T | `OIeZvtYreOg` | 0.595 | 0.229/0.986/8/#F8F8F8 | 0 | 0.374/0.987/#F6E7E6 | 1 | 3 | giữa-trái |
| T | `_EhPtM6cRFk` | 0.238 | 0.190/0.986/10/#EDEDED | 0 | — | 1 | 0 | dưới-trái |
| T | `EANADckKWT4` | 0.262 | 0.183/0.787/8/#F7F7F7 | 0 | 0.157/0.377/#F3F43A | 1 | 2 | giữa-trái |
| T | `ASBVa_H_leI` | 0.282 | 0.168/0.969/10/#EFEFEF | 1 | — | 1 | 5 | giữa-giữa |
| T | `_G9s-Ig6-E8` | 0.446 | 0.192/0.769/7/#EBEBEB | 2 | 0.292/0.845/#F3E3E1 | 3 | 3 | giữa-giữa |
| T | `dY3HfjtmvXI` | 0.485 | 0.190/0.741/7/#F9F8FA | 1 | 0.200/0.812/#F5F1ED | 5 | 2 | dưới-trái |
| L | `YKjWwJZrKXY` | 0.314 | 0.189/0.831/8/#EEEEEE | 3 | 0.190/0.788/#EEEEED | 3 | 1 | giữa-giữa |
| L | `U5ygHCC7cSA` | 0.313 | 0.229/1.000/12/#F6F7F1 | 2 | — | 2 | 6 | dưới-trái |
| L | `8xEY-fMffys` | 0.330 | 0.226/1.000/18/#F7F7F1 | 4 | — | 4 | 4 | giữa-trái |
| L | `xpg0QU7V6IY` | 0.134 | 0.199/0.580/5/#F7F7F7 | 3 | — | 3 | 1 | giữa-giữa |
| L | `PZnSNphOIrE` | 0.349 | 0.182/0.746/7/#F1F1F1 | 3 | — | 6 | 1 | dưới-phải |

## 3. Gộp theo luật ≥70 % KHOÁ · 30–70 % tuỳ chọn · <30 % bỏ

| Đặc điểm | THẮNG | THUA | Kết luận |
|---|---|---|---|
| Băng chữ nền ĐEN đặc chạy hết chiều ngang phía trên | 20/20 | 4/5 | **KHOÁ** (băng trên có ở 20/20, cao trung vị 0.255 H) |
| Cụm chữ VÀNG trong băng trên (tô từ khoá) | 20/20 | — | **KHOÁ** — đặc trưng mạnh nhất của ngách |
| Nhãn nhỏ VÀNG trong tranh (第3位 / 2か月後…) | 18/20 | 4/5 | **KHOÁ** (nhưng không phân biệt thắng/thua) |
| Tranh chia ≥2 panel so sánh | 14/20 | 5/5 | **KHOÁ** (không phân biệt thắng/thua) |
| Dòng CHỐT lớn ở nửa dưới | 10/20 | 1/5 | tuỳ chọn theo luật (50 %) — nhưng THUA gần như không có → **nên có** |
| Ô tô nền ĐỎ | 12/20 | 2/5 | tuỳ chọn (60 % vs 40 %, không phân biệt) |
| Haar bắt được ≥1 mặt | 19/20 | 5/5 | KHÔNG dùng làm cổng — xem §5 |
| Chữ phủ ≥25 % khung | 16/20 | 4/5 | KHOÁ (q25–q75 = 0.262–0.446) |

## 4. Ba dòng chữ đã chốt vào `thumb_dna.json`

| role | seen_in | required | màu chữ | màu viền | cao (H) | rộng (W) | max ký tự | căn | ý nghĩa |
|---|---|---|---|---|---|---|---|---|---|
| `top` | 20/20 | True | `#F7F6F9` | `#0B0A05` | 0.19 | 0.945 | 13 | center | băng tiêu đề trên nền ĐEN đặc, chữ trắng + tô VÀNG đúng cụm từ khoá |
| `lead` | 16/20 | False | `#F0F23B` | `#0B0901` | 0.092 | 0.241 | 8 | left | nhãn nhỏ trong tranh (第3位 / 60歳で退職 / 2か月後…) — mốc thứ hạng hoặc mốc thời gian |
| `shock` | 10/20 | False | `#F9EBE9` | `#0E0E0E` | 0.227 | 0.815 | 9 | center | dòng CHỐT lớn ở nửa dưới (最高の娯楽5選 / ※1円もかからない) — 0/5 mẫu THUA có |

Dải đo thật từng dòng:
- `top`: h 0.136–0.232 H · w 0.407–1.000 W · ký tự 4–16 (trung vị 8)
- `lead`: h 0.035–0.179 H · w 0.084–0.422 W · ký tự 2–14 (trung vị 5)
- `shock`: h 0.100–0.374 H · w 0.377–0.987 W · ký tự 4–14 (trung vị 7)

## 5. Những chỗ máy đo KHÔNG tin được (và cách xử lý)

1. **Haar không đo được mặt tranh manga.** Bắt được ≥1 mặt ở 19/20 ảnh nhưng mặt lớn nhất chỉ ~3 % khung, trong khi mắt nhìn thấy mặt nhân vật ở 20/20 và thường to hơn nhiều → DNA để `require_face: false` (bật cổng này là mỗi lần trượt lại sinh lại ảnh, tốn gpti2 gấp 3).
2. **OCR đọc được ~83 % dòng chính.** Font manga nét dày + chữ chiếm trọn khung làm bộ dò trượt; đã chữa bằng cách chèn viền xám quanh vùng cắt (0 → 7 ký tự trên ảnh thử) và thử 3 cỡ. Số ký tự cuối cùng lấy max(OCR, ước lượng hình học).
3. **Đếm panel nhiễu** (có ảnh ra 9 panel do nền sáng): chỉ dùng ở mức 'có ≥2 panel hay không'.
4. **Tông màu KHÔNG phân biệt thắng/thua**: vùng tranh của THẮNG V=162 S=75, THUA V=161 S=75 — khác biệt nằm ở BIỂU CẢM nhân vật, không ở độ sáng/bão hoà. Đây là chỗ duy nhất tôi dùng mắt: THẮNG 20/20 có ít nhất một khung mặt tươi/bình thản; THUA 5/5 chỉ có mặt khổ (ôm đầu, gục xuống).

## 6. Dùng tiếp

```
py -3.13 -X utf8 cli.py lane-pilot --profile teinengo-tanoshimi ^
  --slug E:\CLAUDE\YOUTUBE\h2dev\assets\teinengo-tanoshimi\ep09-toshokan ^
  --dna E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-tanoshimi\thumb_dna.json --use-title-txt
```
DNA này `measured: true` → sau khi anh chọn ảnh và `thumb-publish`, lane **khoá được** bằng `lane-lock`.

Công cụ đo: `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\tools\thumb_dna_measure\` (`fetch_thumbs.py` · `measure_image.py` · `measure_layout.py` · `aggregate_dna.py` · `build_dna.py`) — dữ liệu thô `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\data\thumb_dna\teinengo-tanoshimi\` (`manifest.json`, `measures.json`, `summary.json`, `contact_win.jpg`, `contact_lose.jpg`).

---

# BẢN ĐO LẠI 2026-09-23 — VÀO ĐÚNG KÊNH GỐC (19/19 thumbnail của `UCI2cPqBmCPMxxKI4u2Gqs_Q`)

Anh chỉ ra bản 22/09 sai (chữ nhỏ, xấu, sai màu). Đo lại toàn bộ kênh gốc và tìm ra **3 lỗi đo**:

| Lỗi bản 22/09 | Vì sao sai | Số đúng (đo lại) |
|---|---|---|
| Ghi dòng dưới là chữ TRẮNG | Thuật toán lấy cụm màu SÁNG nhất làm "màu chữ" → chữ ĐỎ **viền trắng dày** bị đọc thành trắng | Ruột chữ **93 % pixel ĐỎ** (`#E01010`), viền TRẮNG — đo bằng biến đổi khoảng cách + tô loang trong viền |
| Không thấy THANH ĐEN ĐẶC trên | Hàng nào có chữ sáng thì tỉ lệ pixel tối tụt dưới ngưỡng → bộ dò cắt sớm | Thanh đen đặc **19/19 ảnh**, cao **0,21 H** |
| Chữ quá nhỏ | Chỉ đo hộp bao, không đo nét chữ thật | Nét chữ dòng trên **0,164–0,189 H**, dòng dưới **0,20–0,29 H**, mỗi dòng chỉ **4–11 ký tự** |

Thêm 2 chi tiết mô-típ trước đây bỏ sót: **cụm từ khoá tô VÀNG ngay trong dòng trên (19/19)** và **bong bóng thoại trắng
trong tranh (12/19)**.

## Đã áp dụng vào dự án
- Layout mới `bands_manga` + renderer riêng `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\thumbnail_engine\bands_manga.py`
  (thanh đen đặc · một dòng NHIỀU MÀU bằng cú pháp `{cụm}` tô vàng · dòng đỏ viền trắng · nhãn vàng · bong bóng thoại
  tự né mặt). `bands.py` / `panel.py` / `engine.py` KHÔNG đổi → 3 lane cũ giữ nguyên, 118 test xanh.
- Luật chữ mới cho Fable: dòng trên 7–11 ký tự (kèm `{}`), nhãn ≤7, lời thoại ≤8, dòng đỏ 5–9 ký tự.
- Sửa lỗi ảnh nền: layout mới trước đó rơi vào nhánh prompt của satori, trong đó có câu *"compatible with a strong red
  banner"* → gpti2 vẽ hẳn một DẢI ĐỎ ở đáy 3/3 ảnh. Nay `bands_manga` dùng `art_style` của lane và cấm vẽ dải màu.
