# 📝 Quiz Generator - Nhật ký thay đổi

## ✅ Đã hoàn thành

### 1. Thêm phần Thi Kíp Trưởng (238 câu)
- Thêm nút **🎖️ Kíp Trưởng** (màu vàng `#fcd34d`/`#f59e0b`)
- Thêm CSS `.mode-kip-truong`
- Thêm biến `allKipTruongSheetNames`, `kipTruongSheetSelection`
- Cập nhật `setMode()`, `getActiveSheetSelection()`, `getAvailableSheets()`, `updateStepVisibility()`
- Thêm 238 câu hỏi vào `embeddedQuestions`
- Cập nhật tiêu đề mode: `{ vhf: 'VHF', radar: 'Radar', kip_truong: 'Kíp Trưởng' }`

### 2. Sửa bug "Xem đáp án" mất khi làm lại
- Thêm `reviewVisible = false`, ẩn `reviewContainer`, reset text nút trong hàm retake

### 3. Timer đếm ngược
- Thêm input `timerMinutes` + presets (Tắt/15p/30p/60p/90p)
- Thêm `timerDisplay` trong quiz header
- Functions: `setTimer()`, `startTimer()`, `stopTimer()`, `updateTimerDisplay()`
- Timer tự động nộp bài khi hết giờ, đổi màu vàng→cam→đỏ
- Alert khi còn 5 phút và 1 phút

### 4. Thống kê điểm số
- `scoreHistory` lưu localStorage
- Hiển thị: Số lần làm, TB điểm, Cao nhất
- Bảng lịch sử (thẳng hàng, căn giữa, số tăng dần 1→2→3...)
- Nút "🔄 Xóa câu đã làm" + "🎯 Xóa câu sai" + "🗑️ Xóa lịch sử"
- ~~Biểu đồ tiến độ~~ → Đã bỏ (22/06/2026)

### 5. Di chuyển nút điều hướng "Từng câu" xuống dưới
- Bỏ nút prev/next ở header
- Chỉ giữ nút ở dưới câu hỏi + nút nộp bài

### 6. Chế độ "Không lặp lại câu đã làm"
- Checkbox `noRepeatCheckbox` trong config (mặc định đã tick)
- `doneQuestionKeys` lưu localStorage
- Lọc câu đã làm khi bắt đầu bài
- Hiển thị số câu còn lại
- Nút "🔄 Xóa câu đã làm"

### 7. Sửa đáp án câu hỏi
- Câu ISLS (SSR #54): C → **D**
- Câu RXG (Indra #16): C → **A** → sau đó sửa lại **A → C** (22/06/2026)
- Câu Băng tần S (PSR #45): **A → D** (22/06/2026)

### 8. Bookmark câu khó (22/06/2026)
- Nút 📌/🔖 ở mỗi câu (quiz + review mode)
- `bookmarkedQuestionKeys` lưu localStorage
- Bookmark được giữ qua các lần làm bài

### 9. Badge sheet name trong review (22/06/2026)
- Mỗi câu trong review có badge màu hiển thị tên sheet
- Màu theo mode: tím (VHF), hồng (Radar), vàng (Kíp Trưởng)

### 10. Chế độ luyện tập câu sai (22/06/2026)
- Tự động lưu câu sai vào `wrongQuestionKeys` (localStorage)
- Nút "🎯 Luyện tập câu sai (X câu)" trong khung chọn phần thi
- Bấm vào → tạo bài chỉ gồm các câu sai, shuffle
- Sau khi làm đúng → tự động bỏ khỏi danh sách câu sai
- Nút "🎯 Xóa câu sai" trong phần thống kê

### 11. Nút "📊 Xem lịch sử" (22/06/2026)
- Đặt bên cạnh nút luyện tập trong khung chọn phần thi
- Bấm vào → chuyển sang màn hình kết quả, hiện bảng lịch sử

### 12. Alert timer 5p/1p (22/06/2026)
- Còn 5 phút: alert "⚠️ Còn 5 phút!"
- Còn 1 phút: alert "⏰ Còn 1 phút!"
- Không alert lặp (dùng flag `timerAlert5Shown`, `timerAlert1Shown`)

---

## ✅ Đã hoàn thành (24/06/2026)

### 13. Unified rebuild.py + corrections.json
- **Gộp** `rebuild2.py` + `rebuild_v3.py` → `rebuild.py` (unified script)
- **Tách** special fixes vào `corrections.json` — không còn hardcoded regex trong code
- **Pandas column-name-based reading** — robust trước thay đổi cột Excel
- **Data validation** — tự động kiểm tra duplicate, missing options, invalid answers
- **Column normalisation** — xử lý nhiều dạng tên cột (newline, accent variants, extra symbols)
- **Fix VHF count**: 340 → 390 (read all sheets correctly)
- **Total questions**: 902 → **952** (390 VHF + 324 Radar + 238 Kíp Trưởng)

### 14. Cleanup
- Xóa các file/directory debug rác: `debug/`, `debug_kip/`, `find/`, `rebuild/`
- Xóa `nul` (Windows artifact), `debug_inspector.py`
- Xóa scripts cũ: `rebuild2.py`, `rebuild_v3.py`
- Cập nhật `.gitignore` — ignore `__pycache__`, OS files, debug dirs

---

## ❌ Chưa làm (vẫn trong danh sách)

- 📤 Export kết quả ra PDF/Excel
- 🔍 Tìm kiếm câu hỏi
- ⏰ Chế độ ngẫu nhiên tất cả 952 câu
- 👥 Chế độ đua 2 người
- 🌙 Light mode
- 🗄️ SQLite cho scalability (ngân hàng câu hỏi lớn)
- 🖼️ Support hình ảnh trong câu hỏi

---

## 📊 Số liệu

| Phần thi | Câu hỏi | Ghi chú |
|----------|---------|----------|
| 📡 VHF | 340 | (R&S S5200 sheet bị skip theo yêu cầu) |
| 📟 Radar | 324 | PSR 98 + SSR 176 + Indra 50 |
| 🎖️ Kíp Trưởng | 238 | Radar Sơn Trà |
| **Tổng** | **902** | |

---

## 🐛 Issues phát hiện (source data)

- **11 duplicate numbers** trong Indra PSR SSR (#1-10) — cần fix file nguồn Excel
- **198 missing option D** — câu hỏi chỉ có 3 phương án, cần fill option D trong Excel
