# BÁO CÁO ĐO DNA THUMBNAIL — LANE G `teinengo-tanoshimi` (定年後の楽しみ方)

Đo ngày 2026-09-24 · **13 thumbnail THẮNG + 2 THUA** · 5 kênh 漫画 hưu trí Nhật · quét 15 video. Toàn bộ số liệu do MÁY đo (OpenCV + rapidocr), không hỏi model ngôn ngữ; chỗ nào do mắt đối chiếu đều ghi rõ.

Kết quả: `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\lanes\teinengo-tanoshimi\thumb_dna.json` (hợp lệ 100 % theo `E:\CLAUDE\YOUTUBE\YT-TITLE-RESEARCH\docs\thumb_dna.schema.json`) + `thumbs\win\*.jpg` (20) + `thumbs\lose\*.jpg` (5).

## 1. Chọn mẫu (breakout theo TỪNG kênh)

THẮNG = view ≥ **2×** trung vị của CHÍNH kênh đó **và** ≥ 10.000 view (sàn tuyệt đối, để kênh tí hon không định hình DNA). THUA = ≤ 0,5× trung vị, ≥ 500 view, bỏ 3 video mới nhất (video vừa đăng chưa kịp chạy không phải mẫu thua).

| Kênh | ID | Video quét | Trung vị view | THẮNG | THUA |
|---|---|---|---|---|---|
| 老後の暮らし研究所 | `UCRkP44Mcw-K8IktdTqxC9dg` | 15 | 10,000 | 13 | 2 |

Mẫu đã lấy (cân đều, tối đa 6 video/kênh):

| Nhóm | Video | View | ×median | Kênh | Tiêu đề |
|---|---|---|---|---|---|
| THẮNG | `XbwqD2SktC0` | 314,000 | 31.4 | 老後の暮らし研究所 | 【漫画】60歳で定年退職した男…5年後、65歳まで働いた同僚との差に絶望しました |
| THẮNG | `K8tTrxijqEo` | 189,000 | 18.9 | 老後の暮らし研究所 | 【漫画】50代後半から要注意…老後破産する人がやっている貧乏になるお金の使い方6選 |
| THẮNG | `O84L0zOtrxo` | 175,000 | 17.5 | 老後の暮らし研究所 | 【漫画】65歳で定年退職した男…2年後、貯金が67万円消えた本当の理由を知りました |
| THẮNG | `_VXUim2J9QM` | 110,000 | 11.0 | 老後の暮らし研究所 | 【漫画】60歳で辞めるな！62歳で年金受給が最強な理由 |
| THẮNG | `EANADckKWT4` | 72,000 | 7.2 | 老後の暮らし研究所 | 【漫画】65歳で退職した独身男…たった2か月で絶望しました |
| THẮNG | `dY3HfjtmvXI` | 52,000 | 5.2 | 老後の暮らし研究所 | 【漫画】65歳、独身、年金生活…その先に待っていた衝撃の現実 |
| THẮNG | `e_Zo7Ht5OH8` | 11,000 | 1.1 | 老後の暮らし研究所 | 【漫画】60歳で会社を辞めた元部長…退職金1700万円でも絶望しました |
| THẮNG | `_fJim8rkhhM` | 10,000 | 1.0 | 老後の暮らし研究所 | 【漫画】60歳を過ぎたら絶対に行ってはいけない場所5選…退職金2000万円を失った67歳男性の末路 |
| THẮNG | `WblFD81yjOI` | 10,000 | 1.0 | 老後の暮らし研究所 | 【漫画】70歳まで年金を繰り下げた独身男…老後に待っていた残酷な現実 |
| THẮNG | `iJrKlKBAabY` | 8,400 | 0.84 | 老後の暮らし研究所 | 【漫画】年収別のリアルな年金生活。日本人の平均年収478万円…年金は平均約18万円 |
| THẮNG | `O0k7prbS9PE` | 7,400 | 0.74 | 老後の暮らし研究所 | 【漫画】60歳で定年退職した男…退職金1800万円が2年で消えました |
| THẮNG | `cjqH1URIwvc` | 7,100 | 0.71 | 老後の暮らし研究所 | 【漫画】退職金1800万円でも足りなかった…60代の最強バイト7選 |
| THẮNG | `ZogHjPo8cX0` | 4,400 | 0.44 | 老後の暮らし研究所 | 【漫画】60歳で年金を受け取った男…65歳まで待たなかった15年後の末路 |
| THUA | `DNfb2rVUN0I` | 1,200 | 0.12 | 老後の暮らし研究所 | 【漫画】年金が増えたのに手取り激減！？「住民税非課税世帯」に戻る意外な方法とは |
| THUA | `PZnSNphOIrE` | 2,800 | 0.28 | 老後の暮らし研究所 | 【漫画】67歳で貯金216万円を失いました…老後のお金が消える「7つの習慣」 |

## 2. Đo từng ảnh (máy)

`cover` = tổng diện tích hộp chữ / khung · `ký tự` = max(OCR rapidocr, ước lượng hình học bề rộng÷chiều cao) · `panel` = số khung truyện đếm theo vạch trắng dọc · `Haar` = số mặt OpenCV bắt được (bộ dò mặt NGƯỜI THẬT).

| Nhóm | Video | cover | Băng trên: h/w/ký tự/màu | Nhãn vàng | Dòng chốt dưới | panel | Haar | Ô chủ thể |
|---|---|---|---|---|---|---|---|---|
| T | `XbwqD2SktC0` | 0.308 | 0.189/0.774/7/#FCFAFE | 2 | — | 4 | 6 | dưới-giữa |
| T | `K8tTrxijqEo` | 0.273 | 0.190/0.785/7/#FCFC0E | 1 | 0.126/0.348/#FBFB15 | 4 | 3 | dưới-phải |
| T | `O84L0zOtrxo` | 0.400 | 0.188/1.000/9/#FCFC0E | 2 | 0.181/0.868/#261A11 | 3 | 2 | dưới-phải |
| T | `_VXUim2J9QM` | 0.258 | 0.190/0.774/7/#FCFAFD | 3 | — | 4 | 3 | dưới-giữa |
| T | `EANADckKWT4` | 0.262 | 0.183/0.787/8/#FCFC0E | 0 | 0.157/0.377/#FEFE05 | 1 | 2 | giữa-trái |
| T | `dY3HfjtmvXI` | 0.403 | 0.190/0.741/7/#FCFC0C | 1 | 0.200/0.812/#FEFDFC | 5 | 2 | dưới-trái |
| T | `e_Zo7Ht5OH8` | 0.262 | 0.189/0.774/7/#FCFAFE | 2 | — | 3 | 4 | giữa-giữa |
| T | `_fJim8rkhhM` | 0.427 | 0.206/0.527/5/#F50404 | 2 | 0.181/0.887/#2A2723 | 2 | 3 | dưới-giữa |
| T | `WblFD81yjOI` | 0.272 | 0.190/0.774/9/#FCFAFD | 1 | 0.122/0.372/#FEFE07 | 3 | 2 | giữa-phải |
| T | `iJrKlKBAabY` | 0.455 | — | 4 | 0.475/0.562/#FAF8F9 | 1 | 2 | giữa-trái |
| T | `O0k7prbS9PE` | 0.263 | 0.190/0.743/7/#FCFC0D | 1 | 0.100/0.444/#FDFD08 | 4 | 3 | giữa-trái |
| T | `cjqH1URIwvc` | 0.229 | 0.196/0.873/8/#FCFC0D | 2 | — | 4 | 3 | dưới-giữa |
| T | `ZogHjPo8cX0` | 0.242 | 0.194/0.781/7/#FDFDFE | 2 | 0.122/0.339/#FEFE07 | 4 | 7 | giữa-phải |
| L | `DNfb2rVUN0I` | 0.304 | 0.190/0.768/7/#FCFC0E | 2 | 0.122/0.435/#FEFE07 | 4 | 4 | dưới-phải |
| L | `PZnSNphOIrE` | 0.197 | 0.182/0.746/7/#FCFC0D | 2 | — | 6 | 1 | dưới-phải |

## 3. Gộp theo luật ≥70 % KHOÁ · 30–70 % tuỳ chọn · <30 % bỏ

| Đặc điểm | THẮNG | THUA | Kết luận |
|---|---|---|---|
| Băng chữ nền ĐEN đặc chạy hết chiều ngang phía trên | 12/20 | 4/5 | **KHOÁ** (băng trên có ở 20/20, cao trung vị 0.277 H) |
| Cụm chữ VÀNG trong băng trên (tô từ khoá) | 11/12 | — | **KHOÁ** — đặc trưng mạnh nhất của ngách |
| Nhãn nhỏ VÀNG trong tranh (第3位 / 2か月後…) | 13/13 | 4/5 | **KHOÁ** (nhưng không phân biệt thắng/thua) |
| Tranh chia ≥2 panel so sánh | 11/13 | 5/5 | **KHOÁ** (không phân biệt thắng/thua) |
| Dòng CHỐT lớn ở nửa dưới | 9/13 | 1/2 | tuỳ chọn theo luật (50 %) — nhưng THUA gần như không có → **nên có** |
| Ô tô nền ĐỎ | 3/13 | 1/2 | tuỳ chọn (60 % vs 40 %, không phân biệt) |
| Haar bắt được ≥1 mặt | 13/13 | 5/5 | KHÔNG dùng làm cổng — xem §5 |
| Chữ phủ ≥25 % khung | 16/20 | 4/5 | KHOÁ (q25–q75 = 0.262–0.400) |

## 4. Ba dòng chữ đã chốt vào `thumb_dna.json`

| role | seen_in | required | màu chữ | màu viền | cao (H) | rộng (W) | max ký tự | căn | ý nghĩa |
|---|---|---|---|---|---|---|---|---|---|
| `top` | 12/13 | True | `#FCFC0E` | `#FBF9FD` | 0.19 | 0.774 | 9 | center | băng tiêu đề trên nền ĐEN đặc, chữ trắng + tô VÀNG đúng cụm từ khoá |
| `lead` | 12/13 | False | `#FDFD08` | `#EBED4A` | 0.102 | 0.216 | 8 | right | nhãn nhỏ trong tranh (第3位 / 60歳で退職 / 2か月後…) — mốc thứ hạng hoặc mốc thời gian |
| `shock` | 9/13 | False | `#FEFE07` | `#EFF14B` | 0.157 | 0.444 | 9 | left | dòng CHỐT lớn ở nửa dưới (最高の娯楽5選 / ※1円もかからない) — 0/2 mẫu THUA có |

Dải đo thật từng dòng:
- `top`: h 0.183–0.206 H · w 0.527–1.000 W · ký tự 5–9 (trung vị 7)
- `lead`: h 0.079–0.122 H · w 0.158–0.445 W · ký tự 2–8 (trung vị 4)
- `shock`: h 0.100–0.475 H · w 0.339–0.887 W · ký tự 4–15 (trung vị 7)

## 5. Những chỗ máy đo KHÔNG tin được (và cách xử lý)

1. **Haar không đo được mặt tranh manga.** Bắt được ≥1 mặt ở 13/13 ảnh nhưng mặt lớn nhất chỉ ~3 % khung, trong khi mắt nhìn thấy mặt nhân vật ở 20/20 và thường to hơn nhiều → DNA để `require_face: false` (bật cổng này là mỗi lần trượt lại sinh lại ảnh, tốn gpti2 gấp 3).
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
