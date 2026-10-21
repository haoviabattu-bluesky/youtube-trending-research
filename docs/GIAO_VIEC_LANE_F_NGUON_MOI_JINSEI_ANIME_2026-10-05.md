# GIAO VIỆC — Lane F (teinengo-real) đổi kênh mẫu sang 人生の物語アニメ — 05/10/2026

> Từ TRENDING-RESEARCH. **Anh đã duyệt** kênh mẫu mới và 12 video gốc. Mở đầu mọi báo cáo bằng `@lane:teinengo-real`.

## Việc
Từ tập 13 trở đi, Lane F lấy video gốc từ kênh **人生の物語アニメ** (Chuyện đời hoạt hình, `UC5iOuqUPyR4dBLYnrD0tB9A`)
thay cho 老後の暮らし研究所 (đã dùng hết video tốt). Dùng đúng 12 video đã duyệt, theo thứ tự ưu tiên trong hồ sơ.

## Đọc (đường dẫn tuyệt đối)
1. Hồ sơ tổng — ĐỌC HẾT trước tập đầu tiên:
   `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_nguon_jinsei_anime_2026-10-05\HO_SO_BAN_GIAO_LANE_F.md`
2. Mỗi tập: file phân tích của video gốc tập đó (mục 2, 6, 7, 8, 9):
   `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_nguon_jinsei_anime_2026-10-05\phan_tich\<id>.md`
3. Bản có ảnh cho anh xem: `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\results\laneF_nguon_jinsei_anime_2026-10-05\BAO_CAO.html`

## Làm ngay
1. **Tập 13 = video gốc ưu tiên 1: `1qtJbj1lIZY`.** Góc: 48 tuổi bỏ công ty ra làm riêng (脱サラ) → "tuổi giao điểm" với bạn ở lại công ty.
   Chi tiết ở hồ sơ mục 8 và `phan_tich\1qtJbj1lIZY.md` mục 9.
   Đề tài cột B tab `F-teinengo-real`: báo anh điền, hoặc anh cho phép thì agent điền (research không ghi tab lane).
2. Làm đúng quy trình ở hồ sơ mục 9:
   - `competitor.txt` lấy từ `...\channel_dna_raw\_raw\transcripts.json`
   - `video_goc.py` ghi nguồn
   - `series_ctx` có danh sách "CẤM trùng ep.."
   - `SỐ ĐƯỢC PHÉP` chỉ gồm số chế độ đã kiểm luật 2026
3. Hook và thân bài theo luật anh (`C:\Users\admin\.claude\skills\youtube-kich-ban\`). Chỗ kênh mẫu mở hook bằng phép tính số → làm theo hồ sơ mục 4.3 (đưa con số vào cảnh).
4. Thêm vào soát trước khi giao máy 3 các cổng ở hồ sơ mục 6:
   - số học khớp mọi mốc
   - lương hưu ghi rõ 額面/手取り (trước/sau trừ), trả 2 tháng/lần
   - nhân vật cùng đường thì phải nhắc 生活保護
   - nguyên nhân sụp đổ = quyết định trên tiêu đề
   - mọi chữ tiêu đề/thumbnail grep được trong script

## Không làm
- Không chạy `channel_analyzer.py` cho cả kênh mới (nó lấy cả đề tài đã bão hoà mà anh không duyệt).
- Không dùng video ngoài 12 video. Không chép tên nhân vật hay câu thoại gốc (phụ đề Whisper có thể sai tên).
- Tiêu đề/mô tả/thumbnail vẫn TẮT theo lệnh 01/10. Phần phân tích tiêu đề/thumbnail trong hồ sơ để dùng khi anh bật lại.

## Báo lại
Ghi `E:\CLAUDE\YOUTUBE\h2dev\FlowHandoff_local\shared\BAO_CAO_H2DEV_LANE_F_NGUON_MOI_<ngày>.md`:
- đã đọc hồ sơ
- tập 13 dùng video nào, góc gì, kiểu hook mã gì
- điểm nào trong hồ sơ không khớp SOP/luật hiện hành (nếu có)
