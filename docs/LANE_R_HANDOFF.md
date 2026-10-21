# HỒ SƠ LANE R — 深夜食堂・恩返し · TRENDING-RESEARCH 2026-10-18

Video nguồn: **1z1jBVSRYNA** · kênh **逆転ときめき** `UC-xq-30Dlt4zsbpPxl7nwFg` · 117.383 view / 19:54
Hồ sơ phân tích đầy đủ (Artifact HTML): `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\docs\VIDEO_1Z1JBVSRYNA_DEEP_DIVE.html`
Gói bàn giao: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneR_shokudo_1z1jBVSRYNA_2026-10-18\`

---

## §0. ĐỌC TRƯỚC — 6 ĐIỀU QUAN TRỌNG NHẤT

1. **Đây là LANE MỚI (R), chưa có trong danh bạ.** Đã kiểm 10 lane hiện có (`kaigo-sukatto`,
   `yakkyoku-sukatto`, `senior_korekara`, `teinengo-anaba/fuufu/real/tanoshimi`, `shakai_no_naze`,
   `Lopezzapa68`, `_thu_kenh`): **không lane nào phủ** tổ hợp 深夜食堂 + 恩返し + ざまぁ. Chữ cái đã
   dùng: A B C D E F G H J K L M N O P Q X → **R còn trống**.
2. **Clone CÔNG THỨC, KHÔNG clone kênh.** Kênh nguồn là kênh ăn may: 117k view nhưng chỉ **614 sub**
   (0,22 sub/100 view), like **0,219%** (dưới trung vị kênh 0,501%), **8 comment**. Không lấy view
   của video này làm bằng chứng kênh đáng học.
3. **Trục cảm xúc là 恩返し (trả ơn), KHÔNG phải 復讐 (trả thù).** Người được giúp không ra tay;
   kẻ xấu tự sụp vì chính cách làm ăn của mình. Đây là điểm khác Lane K (`kaigo-sukatto`) — Lane K là
   nhân viên trong tổ chức bị cơ chế chế tài; Lane R là **cơ sở kinh doanh nhỏ + người ngoài**.
4. **Đề bài đã được thị trường xác nhận** (đo InnerTube 18/10): cùng mô-típ "quán ăn đêm + mẹ con bơ vơ
   + được cho ăn đổi lấy việc" đã có bản **309.031 · 222.675 · 101.393 · 34.992 · 22.037 view** ở các
   kênh khác. Nhưng bản **copy nguyên văn tiêu đề chỉ được 4 view** → cái ăn view là **đề bài + cách kể**,
   không phải câu chữ tiêu đề.
5. **Tiêu đề phải trong gate 39–46 ký tự** (đo trên 12 title Lane O: 39–46, gồm cả `【漫画】`).
   `title.txt` hiện tại = **40 ký tự**, đã PASS.
6. **Hook phải 140–175 TỪ** (đo trên 12 hook Lane O: 149–199 từ, phần lớn 149–175; "chữ" trong quy ước
   nghĩa là TỪ, không phải ký tự). Hook trong `series_ctx.txt` hiện tại = **160 từ**, đã PASS.

---

## §1. VÌ SAO VIDEO NÀY ĐÁNG BÓC

| Chỉ số | Video nguồn | Đọc ra điều gì |
|---|---|---|
| View / ngày | **72.909** | momentum rất mạnh (1,61 ngày tuổi) |
| Thời lượng | 19:54 | trong khung sản xuất bình thường |
| Độ phủ thoại | **92,4%** | gần như không có đoạn im — nhịp dày |
| Hook | 57s, payoff cảm xúc ở **giây 35** | giữ người qua điểm rơi 30s |
| Khối dài nhất | **198s (16,6%)** ở cuối | dồn toàn bộ phần thưởng, không rải |
| Số lần đảo trục | **3** (元夫 → sụp → bố chồng CEO) | cách nhau ~100–150s |

**Nhưng:** 0,22 sub/100 view + 8 comment + lỗi sản xuất thật ở 10:08 (thoại lặp tên 3 lần, sai tên;
2 khoảng lặng bất thường 615,8s / 621,5s) → **chỉ lấy công thức, đừng lấy kênh làm chuẩn.**

---

## §2. CÔNG THỨC BÓC ĐƯỢC (khung để h2dev viết tập mới)

```
NGƯỜI GẶP NẠN (mẹ + 2 con, bơ vơ, xin ăn)
   ↓ được giúp CÓ ĐIỀU KIỆN (làm việc để trả — không phải bố thí)
   ↓ NGƯỜI GIÚP đang ở thế yếu hơn tưởng (quán sắp phá sản)
   ↓ NĂNG LỰC ẨN của người được giúp (bằng cấp + con cái làm "người thử món")
   ↓ đổi lại: quán từ "chỉ sống 1 ngày/tuần" → "予約の取れない名店"
   ↓ KẺ XẤU 2 LỚP (người trực tiếp → người đứng sau có quyền lực hơn)
   ↓ KẺ XẤU tự phá sản bằng CHÍNH cách làm ăn của mình
   ↓ phần thưởng dồn cuối (16,6% thời lượng)
   ↓ KẾT: hôn nhân / gia đình + CTA
```

### Nhịp 19 khối (đo bằng mốc thoại, dùng làm khung dựng)

| # | Giây | % | Chức năng |
|---|---|---|---|
| 1 | 0–57 | 4,8% | HOOK |
| 2 | 57–68 | 0,9% | mở loop 2 |
| 3 | 68–74 | 0,5% | chốt lời hứa |
| 4 | 74–103 | 2,4% | payoff nhỏ #1 |
| 5 | 103–139 | 3,0% | **đảo trục 1** (kẻ xấu xuất hiện) |
| 6 | 139–247 | 9,0% | cao trào cảm xúc #1 |
| 7 | 247–316 | 5,8% | giải thích cơ chế |
| 8 | 316–321 | 0,4% | báo trước điềm xấu |
| 9 | 321–402 | 6,8% | **sụp** |
| 10 | 402–516 | 9,5% | gỡ thế |
| 11 | 516–573 | 4,8% | sự cố |
| 12 | 573–607 | 2,8% | dồn |
| 13 | 607–694 | 7,3% | **đảo trục 2** (người có quyền) |
| 14 | 694–753 | 4,9% | payoff ấm |
| 15 | 753–816 | 5,3% | thưởng |
| 16 | 816–1014 | **16,6%** | payoff lớn nhất |
| 17 | 1014–1128 | 9,5% | **ざまぁ** |
| 18 | 1128–1160 | 2,7% | kết án |
| 19 | 1160–1187 | 2,3% | đóng |
| — | 1187–1194 | 0,6% | CTA |

---

## §3. GÓI BÀN GIAO

`FlowHandoff_local\results\laneR_shokudo_1z1jBVSRYNA_2026-10-18\mau\ep01-shinya-shokudo\`

| File | Nội dung |
|---|---|
| `series_ctx.txt` | **File chính.** [D1]–[D3] + CẢNH XUNG ĐỘT CHO HOOK (160 từ) + QUY ƯỚC + nhân vật + 3 lần câu cửa miệng + TÌNH TIẾT CẤM CHÉP |
| `title.txt` | 40 ký tự, PASS gate 39–46 |
| `promise.txt` | 1 câu lời hứa (dạng 「…までの話。」) |
| `PHAN_TICH.md` | Bóc tách đầy đủ: số đo, 19 beat, hook từng câu, công thức, lỗi sản xuất |
| `competitor.segments.json` | 268 segment thật (`start`/`end`/`text`, `duration` từ ASR) |
| `competitor.txt` | Transcript dạng `[mm:ss]` |
| `competitor.NGUON.txt` | Nhãn nguồn + **cảnh báo ASR sai chữ** |
| `video_goc.json` | Metadata video gốc |
| `hook_record.json` | Bản ghi đã nạp HOOK_LIBRARY (score 10/12, H38/K03) |

---

## §4. ĐÃ KIỂM

- ✅ Lane: đã dò 10 lane hiện có bằng máy (`profiles/profiles/*.json` + `DANH_BA_LANE.md` + `BAT_DAU_LANE/`),
  không lane nào phủ 食堂/恩返し → hợp lệ đề xuất lane mới.
- ✅ Chữ cái R chưa dùng (grep toàn dự án: A B C D E F G H J K L M N O P Q X).
- ✅ Title 40 ký tự (gate 39–46 đo trên 12 title Lane O).
- ✅ Hook 160 từ (gate 140–175 đo trên 12 hook Lane O).
- ✅ Tên nhân vật: `高瀬` không nằm trong danh sách cấm; đã sửa khỏi trùng `鈴木` (tên nhân vật video gốc).
- ✅ 268 segment có `start`/`end` thật, không phải ước lượng.
- ✅ Hook đã nạp `HOOK_LIBRARY/hooks.jsonl` (403 dòng, backup `.bak_before_1z1`).
- ✅ `pytest tests -q` → **93 passed**.

---

## §5. RỦI RO / LƯU Ý

1. **Transcript là auto-caption, KHÔNG phải whisper.** Sai nhiều: 回線卵丼→海鮮玉子丼, 美オ→みお,
   ざめき→きらめき, 大正教→大盛況, 元旦那→元夫. **Chỉ dùng hiểu nhịp, không trích câu, không lấy số.**
2. **Kênh nguồn không đáng clone** — xem §0.2. Nếu h2dev dùng kênh này làm "kênh mẫu" thì sai hướng.
3. **Chưa có kênh thật cho Lane R.** Cần anh chốt: dựng kênh mới, hay gắn vào kênh sẵn có?
4. **Thumbnail chưa bóc tách.** Đã đo được: 4 nhân vật + 3 khối chữ lớn; nhưng chưa có hướng dẫn
   dựng thumbnail cho Lane R (việc của h2dev, cần brief riêng).
5. **Chưa kiểm 3–5 kênh khác cùng mô-típ** (chỉ đo view của chúng qua InnerTube, chưa đọc hook).
   Nếu anh muốn chắc hơn, nên bóc thêm 2–3 hook của các bản 309k/222k để so công thức.

---

## §6. VIỆC CỦA H2DEV

1. Đọc `series_ctx.txt` trước — đã đủ khối, **không cần tài liệu ngoài**.
2. Giữ đúng `title.txt` (40 ký tự). Nếu đổi, phải kiểm lại gate 39–46.
3. **Không chép** 12 tình tiết trong mục TÌNH TIẾT CẤM CHÉP: 元夫 đòi nối lại · bố chồng là CEO ·
   nhầm 2 khách cùng tên · バラマンディ · マリンズフーズ · 2 con làm "người thử món" thành menu chính ·
   cầu hôn cuối · 元夫 phá sản rồi bị bắt · 顧問弁護士 · lý do ly hôn "chuyển tình cảm" ·
   海鮮玉子丼 từ cá thuyền của bố mẹ đẻ.
4. Số trong truyện phải khớp mọi mốc (38歳/32歳/6歳/79歳/8年/10年/47人/38人/23人/14人).
5. **Lỗi phải tránh** (video gốc bị chê): bảng đọc kana cho tên nhân vật + từ dễ sai; kiểm khoảng lặng
   bất thường trước khi xuất bản; khoá nhân vật → giọng trong `vai.txt`.
