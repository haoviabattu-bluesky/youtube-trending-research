# THÔNG BÁO TỪ h2dev — đổi bố cục `FlowHandoff_local\results\` (2026-09-25)

**Gửi:** dự án `E:\CLAUDE\YOUTUBE\TRENDING-RESEARCH`
**Từ:** `E:\CLAUDE\YOUTUBE\h2dev` (tab dọn hạ tầng)
**Cần các anh/chị làm gì:** đọc mục 3 và 4. Không phải sửa code gấp — h2dev đã làm phần tương thích ngược.

---

## 1. Bố cục MỚI của `FlowHandoff_local\results\`

```
FlowHandoff_local\results\
  img_render\<upload_channel>\<slug>\     ảnh AI máy 2 vẽ xong          (MỚI)
  video_render\<upload_channel>\<slug>\   video máy 2 dựng xong         (không đổi)
  channel_dna\<slug kênh mẫu>\            Channel DNA K1+K2             (KHÔNG ĐỔI)
  nghien_cuu\<mã lane>\                   hồ sơ nghiên cứu ngách        (MỚI — thay `<lane>_from_research`)
```

Luật một dòng: **không còn thư mục `<slug>` nào nằm thẳng ở gốc `results\`.**

Lý do đổi: tới 25/09 gốc `results\` có 20 thư mục slug phẳng (`ep04-fermi-paradox`, `simbot2-01-…`)
không nhìn ra của lane nào, lẫn với `70dai-kenko\` (tên TAB sheet, không phải tên kênh) — ba thế hệ
quy ước chồng lên nhau.

## 2. Đường dẫn cũ ↔ mới (liên quan trực tiếp tới TRENDING-RESEARCH)

| Đang ghi/đọc (cũ) | Từ nay |
|---|---|
| `results\laneE_from_research\` | `results\nghien_cuu\kenko-chiebukuro\` |
| `results\laneF_from_research\` | `results\nghien_cuu\teinengo-real\` |
| `results\laneG_from_research\` | `results\nghien_cuu\teinengo-tanoshimi\` |
| `results\laneK_from_research\` | `results\nghien_cuu\yakkyoku-sukatto\` |
| `results\hook_from_research\` | `results\nghien_cuu\_hook_chung\` |
| `results\channel_dna\<slug>\` | **KHÔNG ĐỔI** |
| `results\<slug>\` (ảnh, phẳng) | `results\img_render\<upload_channel>\<slug>\` |

**Chưa cần sửa ngay:** h2dev đã vá `pipeline\channel_analyzer.py` + thêm `pipeline\duong_ket_qua.py`
để dò **cả tên cũ lẫn tên mới**, nên cổng chống-chạy-lại-K1+K2 vẫn nhận đúng hồ sơ dù bên nào dọn trước.
Đổi tên dần khi thuận tiện là được.

## 3. ⚠️ CẢNH BÁO RỦI RO MẤT DỮ LIỆU — đọc kỹ mục này

`FlowHandoff_local\results\` là thư mục Syncthing kiểu **`receiveonly` ở máy này** (chỉ nhận từ máy 2,
máy 2 là `sendonly`). Nghĩa là **mọi thứ TRENDING-RESEARCH ghi thẳng vào đó đều bị Syncthing xếp loại
*local additions*** — không gửi đi đâu, và **sẽ bị XOÁ SẠCH nếu có ai bấm "Revert local changes"** trên
thư mục `results` trong giao diện Syncthing (đó chính là tác dụng của nút đó với folder receive-only).

Số đo thật trên máy này ngày 25/09:
`localFiles=3027` · `globalFiles=2833` · **`receiveOnlyChangedFiles=219`** — 219 mục đang ở trạng thái đó,
trong đó có nguyên `hook_from_research\`, `hook_lane_EFG_2026-09-23\`, `laneK_from_research\`,
`channel_dna\shakai-no-naze\`, `channel_dna\yakkyoku-sukatto\` — tức phần lớn hồ sơ TRENDING-RESEARCH đã giao.

Hiện chúng **vẫn dùng được** (h2dev đọc cùng ổ đĩa, không cần sync), nên không phải sửa gấp.
Nhưng đừng coi đó là chỗ lưu trữ an toàn: **luôn giữ bản gốc trong `TRENDING-RESEARCH\data\`**,
coi `results\` chỉ là chỗ bàn giao.

## 4. Gợi ý (h2dev chỉ đề xuất, không tự sửa dự án khác)

Nếu muốn thoát hẳn rủi ro ở mục 3, hai bên có thể chuyển kênh bàn giao hồ sơ nghiên cứu sang
`FlowHandoff_local\shared\` (kiểu `sendreceive`, không có bẫy revert). Việc này cần sửa cả
`h2dev\CLAUDE.md` lẫn quy trình bên TRENDING-RESEARCH nên **chưa làm** — nêu ra để anh quyết.

Trả lời / phản hồi: ghi vào `FlowHandoff_local\shared\` hoặc nhắn thẳng tab h2dev.
