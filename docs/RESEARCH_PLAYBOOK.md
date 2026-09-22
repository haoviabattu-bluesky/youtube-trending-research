# Quy trình nghiên cứu — áp dụng cho mọi loại tìm kiếm

> **BẮT BUỘC đọc trước khi bắt đầu bất kỳ task nào dạng:** "tìm ngách mới", "tìm kênh để clone/reup",
> "nghiên cứu đề tài trong ngách X", "kênh nào đang lên", hoặc bất kỳ yêu cầu "nghiên cứu ... cho anh xem".
> Đúc kết từ Lane A (bí ẩn/vũ trụ) và Lane C (nghề nghiệp/lối sống), 2026-09-09/10 — cả 2 lần đều
> có sai sót thật đã sửa, ghi lại dưới đây để không lặp lại.

---

## -1. Ưu tiên NỘI DUNG TỐT hơn là bám đúng ngách xuất phát (user chốt 2026-09-11)

Mục tiêu dự án mở rộng ngách là tìm nội dung TỐT/có tiềm năng phát triển — ngách gốc (simbot2/người già) chỉ là điểm khởi đầu lịch sử, KHÔNG phải giới hạn cứng. Khi so sánh ứng viên, đừng chấm theo "đúng ngách ban đầu không" — chấm theo bằng chứng thật: công thức đề tài đã chứng minh lặp lại được, **momentum THẬT (view/ngày trong 7-30 ngày gần nhất, không phải tổng view lịch sử)**, và kho đề tài có mở rộng được không. Ngách liền kề/họ hàng (trung niên, kinh tế-xã hội, tâm lý học...) đều chấp nhận được nếu nội dung/tăng trưởng tốt hơn ngách gốc. Xem [[uu-tien-noi-dung-tot-hon-bam-nganh]] trong memory.

## 0. Bốn câu hỏi PHẢI trả lời được ở cuối, dù nghiên cứu kiểu gì

1. **Nội dung là gì** — không chỉ tên kênh, mà format/công thức kể chuyện cụ thể
2. **Khán giả là ai** — tuổi, hoàn cảnh, động cơ xem, kiểu tương tác (không phải đoán, phải đọc comment thật)
3. **Có clone được không** — định dạng nhân vật/hình ảnh có tái tạo bằng AI/narration được không
4. **Quy trình sản xuất thế nào** — cái gì tái dùng từ pipeline sẵn có, cái gì phải làm mới

Thiếu 1 trong 4 câu này → user không quyết được, sẽ phải hỏi lại (đã xảy ra thật ở Lane C, khiến phải làm lại báo cáo).

---

## 1. Nguyên tắc cốt lõi (trả giá thật mới rút ra được)

| # | Nguyên tắc | Bằng chứng đã dính |
|---|---|---|
| 1 | **`ch_mult` một mình không đủ — luôn kiểm `trend` thật** (median 5 video mới / median 5 video cũ) trước khi kết luận kênh "mạnh" | 極秘接触: `ch_mult` 37,9 (hạng nhất ngách) nhưng `trend` 0,07 — kênh đã chết 2 tuần. Suýt đề xuất nhầm. |
| 2 | **Số liệu không thay được đọc nội dung thật.** Phải tải transcript, comment gốc, thumbnail thật xuống xem — không suy diễn từ tiêu đề | Kết luận ban đầu "ngách này không dùng ảnh AI" chỉ đúng với THÂN video; tải thumbnail xuống mới phát hiện thumbnail LÀ ảnh AI. |
| 3 | **Báo cáo là bản đã nhai sẵn, tối đa 3–5 lựa chọn có khuyến nghị rõ** — không phải bảng dữ liệu thô nhiều cột nhiều tab | User phản ứng thẳng: "tao có đọc đâu" khi nhận báo cáo 150 dòng/8 cột. |
| 4 | **Link phải hiện rõ, bấm được ngay** — không chôn trong text mờ | User phải yêu cầu lại 2 lần mới đủ rõ (lần 1: có link nhưng ẩn trong bảng; lần 2: phải tách hẳn thành khối riêng). |
| 5 | **Đối chiếu ID/link với nguồn (DB), không gõ tay theo trí nhớ** | Gõ tay 1 channel ID bị sai ký tự giữa chừng, chỉ bắt được khi rà lại trước khi trình. |
| 6 | **Không tự ý bàn giao khi chưa được duyệt** — trình bày để duyệt trước, đóng gói gửi đi sau | User chặn đúng lúc: "Chưa bàn giao, phải gửi lên tao xem tao duyệt đã chứ". |
| 7 | **Sau khi duyệt, đồng bộ MỌI bản sao** (file gốc + bản đã copy sang dự án đích) — đừng chỉ sửa 1 chỗ | Mục "Đặt tên & SEO" thêm vào bản duyệt (artifact) nhưng quên đồng bộ vào file `.md` đã copy sang h2dev. |

---

## 2. Quy trình 7 bước

### Bước 1 — Quét rộng (bỏ qua nếu đã có ngách/kênh cụ thể cần soi)

Công cụ: `src/explore_niches.py` (chấm điểm ngách) hoặc query trực tiếp `data/trending.db` nếu đã có dữ liệu quét sẵn từ tool chạy hằng ngày.

```bash
py -3.13 -X utf8 src/explore_niches.py --detail   # sửa danh sách ở config/explore.yaml
```

Lọc kênh ứng viên bằng SQL trên `trending.db` khi cần tra cứu nhanh trong dữ liệu đã có:
```sql
SELECT c.title, c.ch_age_days, cs.subs, b.median_views, b.trend,
       ROUND(b.median_views * 1.0 / MAX(cs.subs, 300), 1) AS ch_mult
FROM channel c
JOIN channel_baseline b ON b.channel_id = c.channel_id
JOIN channel_snapshot cs ON cs.channel_id = c.channel_id
  AND cs.snap_date = (SELECT MAX(snap_date) FROM channel_snapshot x WHERE x.channel_id = c.channel_id)
WHERE cs.subs >= 300 AND c.ch_age_days <= 200
ORDER BY ch_mult DESC;
```

Tiêu chí sàng lọc vòng 1: tuổi kênh ≤ 90–200 ngày (đủ mới để bắt kịp), `ch_mult` ≥ 10–15 (video điển hình vượt xa số sub), sub ≥ 300 (chống nhiễu).

**Tiêu chí BẮT BUỘC bổ sung (user chốt 2026-09-11, áp dụng mọi lần tìm kênh clone từ nay):**
- **Sub ≥ 1.000** — kênh nhiều view nhưng ít sub (vd 결말주의: 631 sub sau 179 ngày dù có video 77k view) chuyển đổi view→sub yếu, KHÔNG đủ để đề xuất chính dù trend/view đẹp.
- **Video CŨ NHẤT của kênh ≤ 60 ngày** — không phải tuổi kênh (`ch_created_at`), mà tuổi của video ĐẦU TIÊN kênh đăng. Kênh có thể tạo từ nhiều năm trước rồi mới hồi sinh (như simbot2: tạo 2019, nội dung mới chỉ 68 ngày) — phải lấy toàn bộ video qua `recent_uploads()` rồi tìm `min(published_at)`, không suy ra từ ngày tạo kênh. Nếu kênh có >50 video (giới hạn 1 lượt gọi API), coi kết quả là GẦN ĐÚNG (ghi rõ "(≈)"), vì có thể còn video cũ hơn ngoài tầm lấy được.
- Cách lọc nhanh trên tập lớn (hàng trăm kênh): B1 lọc `subs>=1000` trước (rẻ, đã có sẵn trong dữ liệu enrich), B2 chỉ với nhóm đã qua B1 mới gọi thêm `recent_uploads()` để tính tuổi video cũ nhất (đắt hơn vì cần thêm API call), tránh gọi cho toàn bộ hàng trăm kênh.
- **`recent_uploads(limit=50)` KHÔNG đủ để kết luận số liệu cuối cùng cho 1 kênh CỤ THỂ đã chọn đào sâu, nếu kênh có >50 video.** Đã dính thật 2 lần liên tiếp: 돈의 맥락 93 video (mẫu 50 → oldest=25d/trend=5,6× SAI; đủ 93 → oldest=62d/trend=1,77× ĐÚNG), 노년의 지혜 87 video (mẫu 50 → oldest=51d/top1=8,4% SAI; đủ 87 → oldest=90d/top1=17,8% ĐÚNG — lần này sai NẶNG hơn, kênh thực ra đã fail hẳn tiêu chí 60 ngày chứ không phải sai số nhỏ). Ở bước sàng lọc sơ bộ hàng trăm kênh thì lấy gần đúng (50 video) là chấp nhận được (đánh dấu "(≈)"), nhưng khi đã CHỌN 1 kênh để đào sâu/đề xuất chính thức thì BẮT BUỘC phân trang lấy đủ 100% video trước khi chốt số liệu — không có ngoại lệ, kể cả khi số liệu mẫu trông đã "đủ tốt".
- **Kênh có thể có 2 lớp phụ đề: 1 lớp tải TAY (giả/tóm tắt chung chung) và 1 lớp TỰ ĐỘNG nhận diện giọng nói (lời thoại thật).** `youtube_transcript_api` mặc định có thể trả về lớp TAY trước (ngắn 100-200 ký tự, đọc như mô tả video) khiến tưởng nhầm kênh "không có gì để phân tích". Đã dính thật ở 노년의 지혜. Luôn kiểm `transcript.is_generated` — nếu bản đầu quá ngắn bất thường so với độ dài video, phải tìm bản `is_generated=True` (auto-caption) mới ra lời thoại thật.
- **Kênh phải làm CHỦ YẾU video ≤ 40 phút** (user chốt 2026-09-11) — tính % số video của kênh có `duration_s <= 2400`, chỉ giữ kênh có tỉ lệ này cao (≥70-80%). Lý do trả giá thật: 2 ứng viên mạnh nhất từng tìm được (view/sub cao nhất) hoá ra đều là kênh "오디오북"/drama dài hơi 83 phút–3,8 giờ/tập — sản xuất nặng gấp 6-13 lần mức bình thường (20-30 phút). Xu hướng chung: video càng dài, watch time càng cao, YouTube càng đẩy — nhưng đó không phải đánh đổi có lợi cho pipeline sản xuất hiện tại. Áp tiêu chí này SẼ loại bỏ nhiều ứng viên view cao nhất — đây là đánh đổi có chủ đích, không phải bỏ sót.
- **Tác dụng phụ có lợi của việc lọc kỹ (sub + tuổi + duration): dễ bắt được false-positive trùng từ khoá.** Đã dính thật: kênh "평안의 서재" lọt vào danh sách ứng viên ngách người già Hàn Quốc (median view cao, duration hợp lệ) nhưng hoá ra là kênh giảng đạo Kitô giáo của 1 mục sư có tên thật — trùng từ khoá tìm kiếm chứ không liên quan nội dung. Luôn đọc tiêu đề video thật (không chỉ tin số liệu) trước khi đưa vào bảng đề xuất.

### Bước 2 — Xác minh TREND THẬT (chống bẫy kênh đang chết)

**Không bỏ qua bước này với bất kỳ kênh nào lọt vòng 1**, kể cả khi `ch_mult` rất cao.

```python
# Gọi lại API lấy 10-16 video gần nhất, tính trend
ch = api.channels_batch([cid])[cid]
st = api.videos_batch(api.recent_uploads(ch['uploads_playlist'], 16))
rows = sorted(((now - published_at(d)).days, d['views']) for d in st.values())
half = len(rows) // 2
trend = median(v for _, v in rows[:half]) / median(v for _, v in rows[half:])
```

Loại kênh có `trend < 0,6` dù `ch_mult` cao đến đâu — đó là kênh đã qua đỉnh, không phải hình mẫu để clone.

**Ngược lại, `trend` RẤT CAO cũng phải nghi ngờ như nhau.** Nếu nửa cũ gần như chết (baseline gần 0) thì bất kỳ cải thiện nhỏ nào cũng cho ra tỉ lệ trend "hàng trăm lần" — con số này KHÔNG chứng minh công thức ổn định. Luôn tính thêm **% tổng view do top 1/top 3 video chiếm** (như đã làm ở Lane D: top3/15=76%). Nếu top 1 video chiếm >25% tổng view cả kênh → gọi đúng bản chất là "hit rải rác", KHÔNG gọi là "bùng nổ"/"đã tìm ra công thức" dù trend tính ra rất đẹp. Đã dính thật: 백세TV trend 210,6× nhưng 50% video (22/44) dưới 1.000 view và top 1 video ăn 27,8% tổng view — bị gọi nhầm là "bùng nổ" cho tới khi user chỉ ra.

### Bước 3 — Loại kênh không clone được

Kiểm tra nhanh: kênh có phải **người thật xuất hiện/quay** (vlog mặt thật, giọng thật, không phải narration+ảnh/manga) không? Nếu có → loại ngay, ghi rõ lý do trong báo cáo (đừng âm thầm bỏ qua — user cần biết tại sao một kênh số liệu đẹp lại không dùng được).

### Bước 4 — Đào sâu 3–5 ứng viên còn lại

Với mỗi ứng viên:
1. **Titles** — 8–15 video gần nhất → phân tích công thức tiêu đề, đo tương quan độ dài tiêu đề với view
2. **Transcript đầy đủ** — 2–4 video top (`youtube-transcript-api`) → cấu trúc kịch bản, hook, nhịp thiết bị giữ chân (đếm theo từng khoảng 10% thời lượng, không chỉ đọc lướt)
3. **Comment gốc** — 50–70/video (`src/deepdive.py::fetch_comments`) → chân dung khán giả, và **luôn tìm 2 loại comment**: đồng cảm (nhiều like) + bắt lỗi (số học, tính thực tế) — loại thứ 2 chỉ ra đúng cổng QC cần thêm
4. **Thumbnail thật** — tải ảnh xuống xem trực tiếp, đừng suy diễn từ mô tả. Ghép lưới bằng PIL để soi nhanh nhiều ảnh cùng lúc

### Bước 5 — Chấm điểm & chọn 1

Bảng so sánh bắt buộc có các cột: tuổi, sub, median view, `ch_mult`, `trend`, **mô tả NỘI DUNG** (không chỉ tên), kết luận. Chọn theo: view tuyệt đối cao + trend dương + độ dễ clone + khớp năng lực/khán giả sẵn có — không chọn thuần theo điểm số tổng hợp.

### Bước 6 — Đóng gói báo cáo DUYỆT (Artifact, không phải Sheet/file thô)

Cấu trúc đã kiểm chứng qua 2 lần làm thật, đủ để user quyết mà không phải hỏi lại:

```
00. Ngách này đang làm về cái gì       (orientation — 1 câu/kênh)
01. Bảng đối chiếu + LINK từng kênh    (bấm được, tách khối riêng — không chôn trong bảng)
02. Kênh đề xuất + lý do               (bám 4 lý do cụ thể, không chung chung)
03. Tệp khán giả                       (persona: tuổi/hoàn cảnh/động cơ/kiểu tương tác — có quote thật)
04. Bằng chứng                         (thumbnail thật + trích kịch bản + trích comment)
05–08. Cấu trúc kịch bản, định lượng, khoảng trống đề tài
09. Quy trình sản xuất                 (đánh số bước, ĐÁNH DẤU RÕ bước MỚI vs TÁI DÙNG pipeline có sẵn)
10. Đặt tên/mô tả/hashtag/tag SEO      (nếu mục tiêu là dựng kênh mới — 3 phương án tên, không chỉ 1)
11. Video đầu tiên — checklist
12. Chưa làm / rủi ro                  (nói thẳng giới hạn, đừng để user tưởng đã xong)
13. Quyết định                         (nêu rõ các lựa chọn: duyệt / đổi / xem thêm — KHÔNG tự bàn giao)
```

Dùng skill `artifact-design` khi dựng trang này — đây là tài liệu cần đọc và quyết định, không phải chat text thuần.

### Bước 7 — Sau khi duyệt: đóng gói bàn giao

1. Rà lại toàn bộ ID/link theo đúng bản đã duyệt (đối chiếu DB, không gõ tay)
2. Viết `LANE_X_HANDOFF.md` tự chứa — dự án nhận bàn giao không cần mở lại dự án research
3. Copy kèm data gốc (transcript/comment/thumbnail) + tool liên quan sang thư mục dự án đích
4. Viết `PROMPT_GUI_SANG_<dự_án>.txt` để user copy-paste nguyên văn
5. **Nếu artifact duyệt có mục nào chưa nằm trong file `.md`** (như mục Đặt tên/SEO ở Lane C) → bổ sung vào cả 2 bản (gốc + bản copy) trước khi coi là xong
6. Không tự ý gửi/kích hoạt phiên bên kia — để user chủ động

---

## 3. Cạm bẫy đã gặp — đừng lặp lại

| Cạm bẫy | Cách tránh |
|---|---|
| `ch_mult` cao nhưng kênh đang chết | Luôn làm Bước 2, không có ngoại lệ |
| Suy diễn "định dạng hình ảnh" mà không tải ảnh thật xuống xem | Luôn tải + ghép lưới thumbnail trước khi kết luận |
| **1 tấm thumbnail vẫn KHÔNG đủ để phân biệt "video thật" vs "ảnh/clip AI ghép"** — thumbnail chỉ là 1 khung hình nên không lộ sự KHÔNG NHẤT QUÁN giữa các cảnh (dấu hiệu rõ nhất của AI: màu sân/kiểu tóc/tỉ lệ cơ thể đổi khác giữa các đoạn). Đã dính thật ở kênh 백세TV — kết luận "stock video licensed" hoá ra sai, đúng ra là ảnh AI ghép montage | Khi nghi ngờ 1 kênh dùng video thật hay AI, PHẢI tải nguyên video xuống (`yt-dlp`, retry `--extractor-args youtube:player_client=android` nếu dính "Requested format is not available") rồi trích ≥5 khung ở nhiều mốc thời gian khác nhau (ffmpeg — dùng binary `imageio_ffmpeg` nếu máy không có ffmpeg trên PATH) trước khi kết luận định dạng |
| Bảng chỉ có số, không giải thích nội dung | Mỗi hàng kênh có ít nhất 1 dòng mô tả nội dung, không chỉ tên |
| Link kênh chôn trong text mờ | Tách hẳn thành khối/danh sách riêng, mỗi kênh 1 nút bấm rõ |
| Gõ tay ID/link dễ sai | Luôn lấy trực tiếp từ SQL/API, dán chứ không gõ |
| Trình bày như đã bàn giao xong dù chưa được duyệt | Luôn có bước duyệt tường minh trước khi đóng gói gửi đi |
| Sửa artifact nhưng quên đồng bộ file `.md`/bản copy | Sau khi duyệt, kiểm tra chéo artifact vs handoff doc trước khi coi là xong |
| Báo cáo dài dòng, nhiều tab, nhiều cột | Tối đa 3–5 lựa chọn, 1 khuyến nghị rõ, phần còn lại nói rõ vì sao loại |

---

## 4. Công cụ liên quan

| Việc | Lệnh |
|---|---|
| Chấm điểm ngách | `py -3.13 -X utf8 src/explore_niches.py --detail` |
| Dò khoảng trống đề tài | `py -3.13 -X utf8 src/topic_gap.py --topics config/topics_<ten>.yaml` |
| Tải tư liệu hình an toàn bản quyền | `py -3.13 -X utf8 src/stockfetch.py --q "..." --n 8 --sources nasa,commons` |
| Đào sâu 1 kênh (titles/transcript/comment/thumbnail) | Viết script tổ hợp `ytapi.YouTubeAPI` + `deepdive.fetch_comments` + `youtube_transcript_api` + `PIL` — xem code mẫu trong lịch sử phiên Lane A/Lane C, chưa đóng gói thành script dùng lại được (việc cần làm ở §5) |

---

## 5. Việc chưa làm — cần đóng gói thêm

- **Chưa có script `deep_dive_channel.py` dùng chung** — hiện mỗi lần đào sâu 1 kênh phải viết lại đoạn code tổ hợp API+transcript+comment+thumbnail từ đầu. Nên gộp thành 1 hàm nhận `channel_id` → trả về đủ titles/transcripts/comments/thumbnails, để Bước 4 nhanh hơn.
- **Chưa có template artifact tái dùng** — mỗi lần dựng báo cáo duyệt phải viết lại toàn bộ CSS/component từ đầu. Có thể trích thành 1 file `templates/research_review.html` giữ khung + component (bảng, linklist, persona, pipeline, chips) rồi chỉ đổi nội dung.
