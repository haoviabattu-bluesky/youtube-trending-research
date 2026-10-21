# BÁO CÁO DUYỆT — TẬP 22 · LANE L · 「金曜しか稼げない」

Ngày 2026-10-18 · người viết: **gpt-5.6-sol** (ns24, không dùng Claude) · chờ anh duyệt nội dung

---

## 0. BA VIỆC ANH GIAO — ĐÃ XONG

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Lane L, tập 22 | ✅ Lane L = `shakai_no_naze`, đã có ep01–ep21 → tập 22 đúng ô trống. Gói: `laneL_tap22_shinya_shokudo_2026-10-18/mau/ep22-shinya-shokudo/` |
| 2 | Bóc hook 2 bản 309k / 222k | ✅ Đo trực tiếp ASR 0–125s cả 2 bản + bản gốc → `docs/HOOK_2_BAN_THANG_309K_222K.md` |
| 3 | Sol 5.6 viết kịch bản + QC | ✅ Viết 3 lượt (thô → sửa luật → cắt độ dài), QC 9 hạng mục, tất cả PASS |

---

## 1. HOOK — DỊCH NGUYÊN VĂN

### 1a. Hook tập 22 (tiếng Nhật, nguyên văn từ `script.txt`)

> 「すみません。……お願いがあります」
>
> 声は、震えていた。
>
> 「今夜だけでいいんです。働かせてもらえませんか」
>
> 「子どもが二人います。仕事を失って、今夜の寝る場所も決まっていません」
>
> 女の後ろには、同じ顔をした幼い姉妹が立っていた。
>
> 「うちは、金曜しか、人を雇う余裕がない」
>
> 男は、そう言って目を伏せた。
>
> 「それに、明日の朝には閉めるかもしれない」
>
> 港町の外れにある深夜食堂「灯屋」を、桐生悠真は一人で切り盛りしていた。
>
> 店が開いて六年になるが、客が入るのは金曜の夜だけだった。
>
> 「一晩だけなら、やってみるか」
>
> 「本当ですか」
>
> 「皿洗いと仕込みだけだ」
>
> 女は何度も頭を下げた。
>
> 「ありがとうございます」
>
> その夜から、灯屋の時間が少しずつ動き始めた。
>
> 「この店は、俺が立て直す」
>
> 東京商工リサーチの調査では、2026年度上半期の飲食業倒産は514件で、年度上半期として30年間で最多だった。
>
> なぜ、深夜の食堂は、金曜の夜しか稼げないのか。
>
> その答えは、店主が閉じたままにしていた、古い仕込み帳の中にあった。
>
> 時は少し遡る。

### 1b. Dịch nghĩa hook tập 22

> "Xin lỗi… tôi có một việc muốn nhờ."
>
> Giọng cô ấy run.
>
> "Chỉ đêm nay thôi. Anh cho tôi làm việc được không?"
>
> "Tôi có hai đứa con. Mất việc rồi, đêm nay ngủ ở đâu cũng chưa biết."
>
> Sau lưng cô, hai đứa bé gái sinh đôi giống hệt nhau đứng đó.
>
> "Quán tôi chỉ đủ tiền thuê người vào thứ Sáu thôi."
>
> Người đàn ông nói xong thì cúi mặt.
>
> "Với lại, sáng mai có khi tôi đóng cửa luôn."
>
> Quán ăn đêm nhỏ "灯屋" ở rìa thị trấn cảng, Kiryu Yuma một mình gánh.
>
> Quán mở sáu năm, nhưng chỉ đêm thứ Sáu mới có khách.
>
> "Một đêm thôi thì thử xem."
>
> "Thật ạ?"
>
> "Chỉ rửa bát với sơ chế thôi đấy."
>
> Người phụ nữ cúi đầu lia lịa.
>
> "Cảm ơn anh."
>
> Từ đêm đó, thời gian của 灯屋 bắt đầu dịch chuyển, từng chút một.
>
> "Quán này, tôi sẽ dựng lại."
>
> Theo điều tra của Tokyo Shoko Research, nửa đầu năm tài chính 2026, ngành ăn uống có 514 vụ phá sản — cao nhất trong 30 năm tính theo nửa đầu năm.
>
> Tại sao quán ăn đêm lại chỉ kiếm được tiền vào đêm thứ Sáu?
>
> Câu trả lời nằm trong cuốn sổ sơ chế cũ mà người chủ đã đóng lại từ lâu.
>
> Thời gian lùi lại một chút.

### 1c. Ba hook đối chứng — nguyên văn giây đầu

| Bản | View | Giây 0 | Câu đau | Danh tính | Lời hứa |
|---|---|---|---|---|---|
| `_B6QWue5R88` 噂のスカッと | **309.040** | 来ないね もう今日は来ないのかも | この料理どうする? 捨てちゃうの? ママが一生懸命作ったのに | 74,4s | 68,6s |
| `QX7vYQS6qKo` 2ch馴れ初め | **222.675** | すみません。駆けうどんいっぱいいただけますか? | そういった彼女の声は、小さく震えていた。 | 47s | **34,7s** |
| `1z1jBVSRYNA` 逆転ときめき | 117.383 | すみません。何か食べさせてもらえませんか? | 最後に誰かの笑顔が見たかったのでよかった。 | 8,8s | 68,6s |

**Công thức chốt:** 0–5s câu xin, KHÔNG giới thiệu ai → 5–35s câu đau do chính người trong cuộc nói → danh tính đến muộn (≥40s) → lời hứa ≤45s → cắt 数ヶ月後.

---

## 2. TÓM TẮT KỊCH BẢN

**Logline:** Một chủ quán ăn đêm tin rằng quán mình "chỉ kiếm được tiền vào thứ Sáu". Một đêm mưa, anh nhận một người mẹ đơn thân làm thử một buổi. Sáng hôm sau doanh thu cao hơn thứ Sáu — và anh buộc phải nhìn vào thứ mình đã ngừng làm suốt ba năm.

| Chương | Diễn biến |
|---|---|
| **Hook (0–2')** | 三沢千夏 (34) dắt 2 con sinh đôi ướt mưa xin làm một đêm. 桐生悠真 (41) từ chối: "chỉ thứ Sáu mới đủ tiền thuê người", rồi tự nói câu đau: "sáng mai có khi đóng cửa". Anh nhận cô một đêm. Số 514件. Câu hỏi なぜ. 時は少し遡る. |
| **1 — 金曜だけの店** | Sáu năm, thực đơn chỉ ba món: cá nướng, canh miso thịt, cơm nắm nướng. 佐伯 (68) ngồi đúng một chỗ từ ngày mở quán. 千夏 sắp lại chỗ sơ chế. |
| **2 — 一晩の仕込み** | Cô gộp ba món thành set「港の夜の小皿」. Khách gọi thêm. Quán đóng muộn hơn mọi khi. 悠真 hỏi: "sao em làm nhanh thế" — "ở chỗ cũ, ngày nào tôi cũng làm". |
| **3 — 土曜の朝** | Thứ Bảy đông hơn thứ Sáu. 悠真 đếm hoá đơn hai lần, không tin. Anh trả lương một đêm, nhận thêm ba buổi (thứ Tư, Năm, Bảy). |
| **4 — 変えられなかった理由** | Thứ Tư, Năm vẫn vắng — vì anh vẫn nấu đúng ba món cũ. 佐伯 nói thật: "quán anh ba năm rồi vị không đổi". 悠真 nổi giận: "đổi thì không còn là quán này". 千夏 mở cuốn sổ 40 món cô từng nấu. |
| **5 — 灯りを消さないために** | 悠真 đọc sổ. Anh nhận ra mình ngừng nấu món mới từ khi vợ bỏ đi — không phải vì "chỉ thứ Sáu mới có khách". Anh mở thực đơn sáu món, ba món lấy từ sổ của cô. |
| **6 — 金曜だけではなかった** | 「金曜しか稼げないんじゃない。金曜しか、商売をしていなかったんだ」 — "Không phải chỉ thứ Sáu mới kiếm được tiền. Mà là tôi chỉ làm ăn vào thứ Sáu." Kết mở, hai câu hỏi khán giả, CTA. |

**Năm câu trả lời なぜ:** (1) ngành F&B chết vì chi phí + thiếu người, không phải vì khách không đến; (2) quán nhỏ chết vì không đổi thực đơn; (3) "chỉ thứ Sáu đông" là kết quả, không phải nguyên nhân; (4) không có phép màu — 千夏 cứu quán bằng 4 năm nghề có sẵn; (5) người trong cuộc phải tự đổi.

**Không có:** trả thù, hả hê, phép màu, kẻ phản diện. Nhân vật chính đáng thương, không đáng ghét.

---

## 3. SỐ LIỆU — ĐỦ NGUỒN, KHÔNG BỊA

| Mã | Số | Nguồn (đọc trực tiếp 18/10) | Trong kịch bản |
|---|---|---|---|
| D1 | 飲食業倒産 **514件**, 3.4%増, 30年で最多 | 東京商工リサーチ 2026-10-08 | hook |
| D2 | 飲食店倒産 **473件**, **4年連続**増 | 帝国データバンク 2026-07-27 | ch.5 |
| D3 | ラーメン店 **46.4%**増 | 東京商工リサーチ 2026-10-08 | ch.5 |
| D4 | 人手不足倒産 **240件** | 東京商工リサーチ (TBS 2026-10-11) | ch.5 |
| D5 | ゼロゼロ融資後 **149件**, 30.6%**減** | 東京商工リサーチ | cắt vì độ dài |

**Bẫy đã tránh:** `514件` là 飲食**業** (ngành) — không được viết "514件の飲食店"; `473件` mới là 飲食**店**. Hai nguồn khác nhau, không gộp. `ゼロゼロ融資` là **giảm** 30.6%, không phải tăng.

---

## 4. QC — 9 HẠNG MỤC, ĐO TỪ 24 KỊCH BẢN LANE L THẬT

| Hạng mục | Chuẩn thật | Kết quả |
|---|---|---|
| Độ dài | 4.849–8.170 ký tự | **7.949** ✅ |
| Ngoặc thoại | 「 = 」 | 263 = 263 ✅ |
| Số dạng Ả Rập | `514件`, `4年連続` | ✅ (không kanji) |
| `%` thay `パーセント` | 21/24 bản dùng `%` | ✅ |
| Không mục "第Nの理由" | 0/24 bản có | ✅ |
| CTA cuối bài | 24/24 bản có | ✅ |
| 復讐 / ざま / 奇跡 / 恩返し | 0 lần | ✅ |
| Tên gốc 鈴木公平 / みお | 0 lần | ✅ |
| Số bịa ngoài tư liệu | 0 | ✅ |
| Title | 21–38 ký tự, 【漫画】 cuối | 31 ký tự ✅ |

**Ba lỗi đã bắt được và sửa** (nếu anh muốn biết em đã chặn cái gì):
1. Lượt 1 Sol viết **bảng + mốc thời gian** (24.842 ký tự) — sai hẳn format `script.txt` thật. Viết lại.
2. Lượt 2 dùng **kanji cho số** (五百十四件) và `パーセント` — đo 24 bản thật thì họ dùng `514件` / `%`. Sửa.
3. Lượt 2 có mục **「第一の理由は…」** liệt kê — 0/24 bản thật làm vậy, đọc như bài luận. Bỏ, thay bằng thoại.

---

## 5. FILE ĐÃ GIAO

`E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneL_tap22_shinya_shokudo_2026-10-18\mau\ep22-shinya-shokudo\`

| File | Nội dung |
|---|---|
| `script.txt` | **Kịch bản hoàn chỉnh** 7.949 ký tự — bản để duyệt |
| `series_ctx.txt` | Tư liệu: số được phép, 5 nguồn [D1–D5], bẫy cấm, nhân vật, thang leo, công thức hook |
| `title.txt` | 「金曜しか稼げない」なぜ深夜食堂は平日に客が来ないのか【漫画】 (31 ký tự) |
| `promise.txt` | なぜ、深夜の食堂は、金曜の夜しか稼げないのか。 |
| `PHAN_TICH.md` | Phân tích đầy đủ: vì sao chọn, công thức hook, 5 chương, 5 câu trả lời, QC |
| `video_goc.json` | Video nguồn + 2 bản tham khảo hook (309k/222k) |
| `competitor.NGUON.txt` | Nguồn, ghi rõ **ASR auto-caption có lỗi chữ, không phải whisper** |
| `competitor.txt` | 290 dòng thoại gốc kèm mốc thời gian |
| `competitor.segments.json` | 290 segment `{start, end, text}`, không chồng lấn |
| `script.pre_fix.txt` / `script.pre_trim.txt` | Bản trước khi sửa — chỉ để đối chiếu |

---

## 6. CHỜ ANH DUYỆT

Em **dừng ở đây**, chưa làm gì thêm. Anh xem `script.txt` rồi chốt:

- **Duyệt** → em đóng gói bàn giao chính thức (copy sang đúng đường, viết `HO_SO_LANE_L_TAP22.md`).
- **Sửa** → anh nói chỗ nào (giọng nhân vật, nhịp, tên, kết), em cho Sol viết lại phần đó.
- **Đổi đề bài** → em làm tập khác.

**Chưa làm (thuộc h2dev, không thuộc dự án này):** ảnh, giọng đọc, dựng video.
