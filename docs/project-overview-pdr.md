# Product Design Requirement — YouTube Trend & Outlier Hunter

## Vision

Tìm **ngách YouTube faceless đáng làm trước khi nó thành trend lớn**, bằng cách phát hiện tự động các *hiện tượng*: kênh nhỏ/mới có video bùng view, và bùng **nhiều lần** chứ không phải một video may mắn.

## Target user

Một người: chủ các kênh YouTube faceless (JP người già/sức khoẻ, satori/chuyện cảm động). Đọc báo cáo mỗi sáng trên Google Sheet, chọn 1–3 kênh/video để nghiên cứu sâu rồi đưa vào dây chuyền sản xuất (`youtube-script` → `youtube-image-prompts` → `veo3_flow_automation` / `grok_video` → `youtube-thumbnail`).

## Vấn đề đang giải

| Cách cũ | Vì sao hỏng |
|---|---|
| Trang Trending của YouTube | Đã bỏ từ 2025, chỉ còn Charts theo category (Music/Gaming) — vô dụng cho faceless |
| YouTube Studio → Trends | Dữ liệu tốt (Top searches, Breakout, Content gaps) nhưng **không có API**, phải login và bấm tay |
| Google Trends → YouTube Search | Nguyên lý đúng nhưng **pytrends bị chặn 429** (verify 2026-09-09) |
| Tìm tay "video nào nhiều view" | Ra toàn kênh triệu sub — không nhân bản được |

## Key features

1. **Discovery rộng, chi phí 0** — InnerTube keyless, 300+ keyword/ngày (Data API `search.list` chỉ cho ~80/ngày)
2. **Chấm điểm outlier đa chỉ số** — `breakout` (so median chính kênh) là chính, `view/sub` chỉ phụ; có sàn/trần chống nhiễu
3. **Delta 24h** — snapshot SQLite theo ngày, biết video *đang* được đẩy hay đã nguội
4. **`hit_rate` cấp kênh** — phân biệt "ngách đáng test" với "video may mắn"
5. **Momentum & content gap theo keyword** — thay Google Trends, đo cả cung lẫn cầu ngay trên YouTube
6. **Đào sâu tự động** — transcript + comment top 5 video/ngày → hook, cấu trúc, insight khán giả
7. **Google Sheet vừa là báo cáo vừa là bảng điều khiển** — sửa keyword/ngưỡng không cần đụng code

## Non-goals

Không sản xuất nội dung, không tải/đăng video, không dashboard web, không API trả phí bên thứ 3, không Shorts. Xem `plans/260909-1611-.../brainstorm-summary.md` §11.

## Ràng buộc cứng

- **Không xoá bất kỳ dòng/cột nào trong Google Sheet.** Chỉ append/update, chỉ trên tab whitelist (`TRENDING`, prefix `TRD_`). Sheet đích đang chứa dữ liệu thật ở tab `GMAIL` (974 dòng) và `NOTE`.
- Chạy máy nhà trước (IP đã verify sạch), VPS sau.
- Mỗi file code ≤ 200 dòng.
