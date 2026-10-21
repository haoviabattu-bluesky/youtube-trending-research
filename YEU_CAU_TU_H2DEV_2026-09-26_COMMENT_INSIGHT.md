# YÊU CẦU TỪ DỰ ÁN h2dev — CHẮT BÌNH LUẬN THẬT THÀNH "COMMENT_INSIGHT" CHO 3 KÊNH E · F · G

> Người gửi: `E:\CLAUDE\YOUTUBE\h2dev` · Ngày 2026-09-26.
> Đơn **tự chứa** — đọc hết file là làm được, không cần hỏi lại h2dev. Làm theo mục 3 → 4 → 5, tự kiểm mục 6, báo lại mục 7.

---

## 1. VÌ SAO CẦN

Anh chốt 2026-09-26: trước khi viết kịch bản, phải đọc bình luận dưới video kênh mẫu như **góp ý/phản ánh thật** của
người xem. Bên h2dev đã có cơ chế: mỗi kênh mẫu có 1 file `COMMENT_INSIGHT.md`; khối cuối file (`## ĐƯA VÀO PROMPT`)
được máy **tự nhồi vào lệnh cho model viết kịch bản** của mọi tập lane đó. Khối này viết sai/nhạt thì mọi tập sau viết sai/nhạt.

Đã làm xong 3 kênh (làm MẪU, đọc trước khi bắt tay):
- `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\yakkyoku-sukatto\COMMENT_INSIGHT.md` (Lane K — **mẫu chuẩn nhất, bám theo file này**)
- `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\shakai-no-naze\COMMENT_INSIGHT.md` (Lane L)
- `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\otonanomouten\COMMENT_INSIGHT.md` (Lane M)

Phát hiện chính từ 3 kênh đó (để biết cần tìm cái gì): video làm người xem **ức chế/giận** có view gấp 10–100 lần video
nhẹ nhàng; bình luận top toàn là giận nhân vật, cuối video người xem chuyển sang **thương cảm** và **chép lại câu đạo lý**;
người xem kể chuyện thật của họ, bắt lỗi dữ kiện, và bênh nhân vật xấu nếu người bị hại cư xử vô lý.

## 2. VIỆC CẦN LÀM — 3 KÊNH

| Lane h2dev | Kênh mẫu | Dữ liệu (đã có sẵn, bên em tải) | Ghi kết quả vào (thư mục đã tồn tại) |
|---|---|---|---|
| E `kenko-chiebukuro` | シニアいきいき健康 `UCBODlDy5sXo_49pC7KPr7vQ` · 27 video · 168 bình luận | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\E_kenko\` | `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\ikiiki-kenko\` |
| F `teinengo-real` | 老後の暮らし研究所 `UCRkP44Mcw-K8IktdTqxC9dg` · 15 video · 433 bình luận | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\F_real\` | `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougonokurashi\` |
| G `teinengo-tanoshimi` | 老後のお金ストーリー `UCI2cPqBmCPMxxKI4u2Gqs_Q` · 20 video · 214 bình luận | `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\G_tano\` | `E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougo-money-story\` |

Mỗi kênh ra **2 file** trong thư mục cột cuối: `COMMENTS_TOP.md` (máy sinh) + `COMMENT_INSIGHT.md` (em đọc và viết tay).
**Chỉ ghi đúng 2 file này** — không sửa file nào khác của h2dev (profile, code, SOP, CHANNEL_DNA.md…).

## 3. BƯỚC 1 — SINH FILE ĐỌC NHANH (máy, 0 LLM, vài giây)

Dùng đúng tool của h2dev (chỉ CHẠY, không sửa) để 3 kênh cùng một khuôn với K/L/M:
```
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\E_kenko --profile kenko-chiebukuro
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\F_real --profile teinengo-real
py -3.13 -X utf8 E:\CLAUDE\YOUTUBE\h2dev\pipeline\comment_digest.py --src E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH\data\hook_audit_laneEFG\G_tano --profile teinengo-tanoshimi
```
Mỗi lệnh in `✓ <đường dẫn>\COMMENTS_TOP.md`. File đó xếp video theo view, mỗi video 15 bình luận nhiều like nhất, có nhãn
thô (giận / kể chuyện thật / bắt lỗi / góp ý sản xuất / thương cảm). **Nhãn chỉ để lọc nhanh — phải đọc nguyên văn.**

## 4. BƯỚC 2 — ĐỌC VÀ VIẾT `COMMENT_INSIGHT.md` (người/LLM đọc tiếng Nhật)

Đọc hết `COMMENTS_TOP.md` (nếu cần đọc thêm bình luận ngoài top 15 thì mở `comments.json` gốc). Viết file theo **đúng khuôn
dưới** (tiêu đề mục giữ nguyên chữ, vì máy tìm đúng dòng `## ĐƯA VÀO PROMPT`):

```markdown
# INSIGHT TỪ BÌNH LUẬN THẬT — Lane <X> `<mã lane>` (kênh mẫu <tên kênh>)

Đọc và chắt lọc ngày <yyyy-mm-dd> từ <N> bình luận khán giả / <M> video
(nguyên văn xếp theo lượt thích: `<đường dẫn tuyệt đối COMMENTS_TOP.md>`, dữ liệu gốc `<đường dẫn tuyệt đối comments.json>`).
Khối ĐƯA VÀO PROMPT ở cuối file được lean_script.py tự nhồi vào prompt model VIẾT (S2).

## 1. Video nào nổ và vì sao (view đo thật)
<bảng: tiêu đề tiếng Nhật (dịch Việt) | view | bình luận> — 4–8 video, cả nhóm nổ lẫn nhóm xịt.
<1–2 câu: điểm chung của nhóm nổ khác nhóm xịt ở đâu (chủ đề? có nhân vật để giận? có con số gây sốc?)>

## 2. Năm tín hiệu rút ra
1. <tín hiệu> — trích 1–2 bình luận nguyên văn kèm dịch + số like → hệ quả cho kịch bản (1 câu bắt đầu bằng "→").
... (đúng 5 mục, ưu tiên theo thứ tự: người xem giận/ức chế cái gì · thương/cảm động cái gì · chuyện thật họ kể ·
lỗi dữ kiện họ bắt · câu nói/đạo lý họ chép lại)

## 3. Góp ý sản xuất (không phải kịch bản — chuyển tab lane xem)
<giọng, hình, chữ, tốc độ… nếu có; bình luận chính trị/kỳ thị ghi 1 dòng "BỎ QUA">

## ĐƯA VÀO PROMPT
- <5–8 gạch đầu dòng, TIẾNG VIỆT, câu mệnh lệnh cho người viết kịch bản>
```

**Luật viết (bắt buộc):**
1. **Mọi con số phải tra ngược được**: view lấy từ `channel.json` (`videos[].views`), số bình luận/like lấy từ `comments.json`.
   Không làm tròn khác đi, không suy diễn số không có trong dữ liệu.
2. **Mọi chữ tiếng Nhật trích dẫn phải kèm dịch tiếng Việt ngay sau trong ngoặc** — kể cả 1 từ.
3. Khối `## ĐƯA VÀO PROMPT`: 5–8 dòng, mỗi dòng 1 câu mệnh lệnh cụ thể ("Cho…", "Không để…", "Kết bằng…"), viết để model
   viết kịch bản làm theo được ngay. **Không** chép tên người/tên nhân vật/tình tiết đặc trưng của kênh mẫu vào khối này
   (tránh bị chép nguyên), **không** đưa quan điểm chính trị/kỳ thị giới, tuổi, thế hệ. Trích tiếng Nhật trong khối này cũng
   phải kèm dịch.
4. Ghi rõ lane E là kênh **sức khoẻ người già dạng liệt kê kiểu bác sĩ** (không phải truyện có nhân vật xấu) — tín hiệu "giận"
   có thể là giận thông tin sai / lo sợ bệnh; không ép khuôn "nhân vật đáng ghét" vào kênh này nếu bình luận không cho thấy vậy.
   Viết đúng cái bình luận thật nói, **không** viết cái mình đoán.
5. Nếu 1 kênh có quá ít bình luận để rút 5 tín hiệu đáng tin (vd vài video 0 bình luận), ghi rõ "ít dữ liệu" ở mục 2 và chỉ
   viết số tín hiệu có bằng chứng — đừng bịa cho đủ 5.

## 5. KHÔNG ĐƯỢC LÀM
- Không sửa `comment_digest.py`, profile, SOP hay bất kỳ file nào khác của h2dev — chỉ tạo 2 file/kênh ở mục 2.
- Không tải lại bình luận từ YouTube (dữ liệu đã đủ); nếu thấy thiếu, ghi vào báo cáo mục 7, đừng tự tải.
- Không ghi đè `COMMENT_INSIGHT.md` của K/L/M.

## 6. TỰ KIỂM TRƯỚC KHI BÁO XONG
Lệnh sau phải in `True` cho cả 3 lane (máy đọc được khối ĐƯA VÀO PROMPT):
```
py -3.13 -X utf8 -c "import sys;sys.path.insert(0,r'E:\CLAUDE\YOUTUBE\h2dev\pipeline');import profiles,lean_script as l;[print(p,'KHÁN GIẢ THẬT' in l.khoi_them(profiles.load(p))) for p in ('kenko-chiebukuro','teinengo-real','teinengo-tanoshimi')]"
```
Và tự đối chiếu: chọn ngẫu nhiên 3 con số trong mỗi file → mở `channel.json`/`comments.json` kiểm lại đúng.

## 7. BÁO LẠI (bàn giao)
Trả cho anh đúng khối sau (anh chuyển lại cho h2dev):
```
XONG COMMENT_INSIGHT E/F/G — <yyyy-mm-dd hh:mm>
E: E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\ikiiki-kenko\COMMENT_INSIGHT.md — <N> bình luận · 1 câu phát hiện chính
F: E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougonokurashi\COMMENT_INSIGHT.md — <N> bình luận · 1 câu phát hiện chính
G: E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\rougo-money-story\COMMENT_INSIGHT.md — <N> bình luận · 1 câu phát hiện chính
Tự kiểm mục 6: True/True/True
Ghi chú (thiếu dữ liệu, video 0 bình luận…): <nếu có>
```

## 8. VIỆC LÂU DÀI (từ nay, mọi kênh bên em nghiên cứu cho h2dev)
Mỗi khi bên em giao hồ sơ kênh mẫu mới cho h2dev (có `comments.json`), làm luôn mục 3–6 cho kênh đó và ghi vào
`E:\CLAUDE\YOUTUBE\h2dev\docs\channel_dna\<slug kênh>\` — tập đầu của lane mới sẽ có insight ngay, không phải chờ.
