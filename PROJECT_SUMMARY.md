# 📝 Quiz Generator — Tổng quan dự án

**Ngày bắt đầu:** 18/06/2026  
**Cập nhật:** 24/06/2026  
**Trạng thái:** ✅ Hoàn thành + PWA  
**File chính:** `quiz_generator/index.html`  
**GitHub Pages:** https://txdung.github.io/quiz-generator/

---

## 🎯 Mục tiêu

Xây dựng ứng dụng quiz trắc nghiệm trực tuyến (HTML đơn file) để ôn thi bằng chứng chỉ VHF và kiến thức Radar hàng không. Không cần server, mở trong trình duyệt là chạy.

---

## ✅ Những gì đã làm

### 1. 🏗️ Kiến trúc
- **Single-file HTML** — không cần server, không phụ thuộc thư viện bên ngoài
- **952 câu hỏi nhúng sẵn** trong file HTML
- **Dark theme** xanh xám tối — dịu mắt khi làm bài lâu

### 2. 📚 Dữ liệu câu hỏi (952 câu)

#### 📡 Chế độ VHF (390 câu)
| Sheet | Số câu |
|-------|--------|
| Lý thuyết chung | 200 |
| Park Air T6T T6R | 50 |
| Jotron TA7650 RA7203 | 50 |
| Icom IC A200 | 20 |
| R&S 4200 | 20 |

#### 📟 Chế độ Radar (324 câu)
| Sheet | Số câu |
|-------|--------|
| PSR (Sơ cấp) | 98 |
| SSR (Thứ cấp) | 176 |
| Indra PSR SSR | 50 |

#### 🎖️ Chế độ Kíp Trưởng (238 câu)
| Sheet | Số câu |
|-------|--------|
| Radar Sơn Trà | 238 |

### 3. 🎮 Tính năng Quiz
- **3 chế độ thi:** VHF / Radar / Kíp Trưởng — toggle buttons
- **Sheet selection riêng** cho mỗi chế độ
- **Question count presets:** 10, 20, 50, 100, Tất cả
- **Shuffle ngẫu nhiên** thứ tự câu hỏi
- **Progress bar** theo dõi tiến độ
- **Auto-grading** chấm điểm /10
- **Review chi tiết:** ✅ Đúng, ❌ Sai, ⚠️ Chưa làm + badge sheet name
- **Làm lại** (reshuffle)
- **2 chế độ hiển thị:** Tất cả câu hỏi / Từng câu (có prev/next)
- **Timer đếm ngược** với presets (Tắt/15p/30p/60p/90p) + alert 5p/1p
- **Không lặp câu đã làm** (mặc định bật)
- **Bookmark câu khó** 🔖 (localStorage)
- **Luyện tập câu sai** 🎯 (tự động lưu câu sai, tạo bài chỉ từ câu sai)
- **Thống kê điểm số** (số lần làm, TB điểm, cao nhất, bảng lịch sử)
- **PWA** — Cài đặt như app trên điện thoại (manifest, service-worker v2, install prompt)
- **iOS support** — Hướng dẫn "Add to Home Screen" tự động hiện trên iOS
- **Service Worker** — Cache-first, offline fallback, auto-update mỗi 60s

### 4. 🎨 Giao diện UI/UX (Dark Theme)
- **Dark theme xanh xám tối:** nền `#475569→#334155`, card `#1e293b`
- **Question card:** `#0f172a` (tối hơn card)
- **Chữ:** `#cbd5e1` (xám nhạt, không chói)
- **Accent tím dịu:** `#7c3aed` / `#a5b4fc`
- **Nút bấm đồng bộ:** tất cả dùng `btn-secondary` (`#374151`/`#cbd5e1`)
- **Score circle:** `#374151`
- **Responsive:** Mobile-friendly
- **Smooth animations:** Hover effects, transitions

---

## 🔧 Các bug đã fix

| Lỗi | Nguyên nhân | Cách fix |
|-----|-------------|----------|
| Progress bar "Từng câu" không cập nhật | `updateProgress()` chạy trước `selectOption()` | Đổi thứ tự |
| Retake "Từng câu" hiện câu cuối | `readAllAnswersBeforeSubmit()` chạy sau `renderQuiz()` | Đọc đáp án trước |
| Progress không cập nhật khi navigate | Thiếu `updateProgress()` trong `renderCurrentQuestion()` | Thêm vào hàm |
| Page load không thấy nút mode | `updateStepVisibility()` ẩn `modeSelectionBox` | Bỏ ẩn, thêm `setMode('vhf')` init |
| "Xem đáp án" mất khi làm lại | Không reset review state | Thêm `reviewVisible = false` |
| Sửa đáp án PSR #45 | Đáp án sai trong file gốc | A → D |
| Sửa đáp án Indra #16 | Đáp án sai trong file gốc | A → C |

---

## 📁 Cấu trúc dự án

```
quiz_generator/
├── index.html                   ← File chính (mở trong trình duyệt)
├── manifest.json                ← PWA manifest
├── service-worker.js            ← PWA cache + offline (v2)
├── icon-192.png                 ← PWA icon 192×192
├── icon-512.png                 ← PWA icon 512×512
├── icon.png                     ← Icon gốc 2400×2400
├── .gitignore                   ← Git ignore rules
├── PROJECT_SUMMARY.md           ← File tóm tắt này
├── CHANGES_LOG.md               ← Nhật ký thay đổi
├── all_questions.json           ← Dữ liệu 952 câu hỏi
├── rebuild.py                   ← Unified Excel→JSON script
├── corrections.json             ← Answer corrections (no hardcoded fixes)
├── add_radar.js                 ← Script merge radar vào HTML
├── NH Câu hỏi, ĐA Lý thuyết_Nguyên lý PSR _16.5.2026.xlsx
├── NH Câu hỏi, ĐA Lý thuyết_Nguyên lý SSR _5.2026.xlsx
├── NH Câu hỏi, ĐA Lý thuyết_Radar_Indra_PSR_SSR INDRA_5.2026.xlsx
├── NHCH LÝ THUYẾT NĂNG LỰC VHF.xls
└── 06. LT KT Radar Son Tra_Long.xlsx
```

---

## 🚀 Cách sử dụng

1. Mở `index.html` trong trình duyệt (hoặc truy cập https://txdung.github.io/quiz-generator/)
2. Chọn chế độ: **VHF** / **Radar** / **Kíp Trưởng**
3. Tick chọn các sheet muốn làm quiz
4. Chọn số câu: 10, 20, 50, 100, hoặc Tất cả
5. (Tùy chọn) Bật timer, bật không lặp câu đã làm
6. Nhấn **"🚀 Bắt đầu làm bài"**
7. Làm bài → Nộp bài → Xem kết quả chi tiết + lịch sử
8. Có thể làm lại, luyện tập câu sai, hoặc về màn hình chính

---

## 💡 Cấu trúc code chính

### Variables
- `embeddedQuestions[]` — Mảng 952 câu hỏi (`mode: 'vhf'`, `'radar'`, `'kip_truong'`)
- `currentMode` — Chế độ hiện tại
- `vhfSheetSelection`, `radarSheetSelection`, `kipTruongSheetSelection` — Set sheet đang chọn
- `quizQuestions[]` — Câu hỏi đã shuffle cho quiz hiện tại
- `userAnswers[]` — Đáp án người dùng đã chọn
- `scoreHistory[]` — Lịch sử điểm số (localStorage)
- `doneQuestionKeys` — Câu đã làm (localStorage)
- `wrongQuestionKeys` — Câu sai (localStorage)
- `bookmarkedQuestionKeys` — Câu được bookmark (localStorage)
- `quizViewModePreference` — Chế độ hiển thị ưu tiên: `'all'` hoặc `'one'`
- `quizViewMode` — Chế độ hiển thị hiện tại
- `currentQuestionIndex` — Index câu hiện tại (mode "Từng câu")

### Key Functions
- `getActiveQuestions()` — Lấy câu hỏi từ sheet đã chọn
- `getTotalQuestions()` — Đếm số câu có thể chọn
- `setMode(mode)` — Chuyển chế độ VHF/Radar/Kíp Trưởng
- `renderSheetGroups()` — Render sheet selection theo nhóm
- `shuffle(array)` — Fisher-Yates shuffle
- `toggleBookmark(q)` — Bật/tắt bookmark câu hỏi
- `toggleModeSheet(name, checked)` — Bật/tắt sheet
- `selectOption(radioInput)` — Xử lý chọn đáp án
- `setQuizView(mode)` — Chuyển "tất cả" / "từng câu"
- `renderCurrentQuestion()` — Render 1 câu (mode "Từng câu")
- `navigateQuestion(delta)` — Chuyển câu trước/sau
- `buildReview()` — Xây dựng danh sách review
- `startPracticeWrong()` — Bắt đầu luyện tập câu sai
- `updateWrongCountDisplay()` — Cập nhật số câu sai hiển thị

---

## 🎨 Bảng màu Dark Theme

| Thành phần | Màu nền | Màu chữ |
|------------|---------|---------|
| Body | `#475569 → #334155` | — |
| Card | `#1e293b` | — |
| Question card | `#0f172a` | — |
| Label đáp án | `#1e293b` | `#cbd5e1` |
| Sticky header | `#0f172a` | — |
| Progress bar | `#334155` | fill: `#7c3aed` |
| Nút bấm (tất cả) | `#374151` | `#cbd5e1` |
| Score circle | `#374151` | `#cbd5e1` |
| Badge câu hỏi | `#4c1d95` | `#a5b4fc` |
| Sheet badge VHF | `#312e81` | `#a5b4fc` |
| Sheet badge Radar | `#831843` | `#f9a8d4` |
| Sheet badge Kíp Trưởng | `#451a03` | `#fcd34d` |
| Bookmark | `#422006` | `#fcd34d` |
| Đúng | `#052e16` | `#86efac` |
| Sai | `#450a0a` | `#fca5a5` |
| Chưa làm | `#1a1a15` | `#fcd34d` |

---

## 🔮 Có thể cải thiện thêm
- Export kết quả ra Excel/PDF
- Tìm kiếm câu hỏi theo từ khóa
- Chế độ ngẫu nhiên tất cả 952 câu (3 mode trộn lẫn)
- Database (SQLite) cho scalability
- Hỗ trợ hình ảnh trong câu hỏi
- Light mode
- Chế độ đua 2 người

---

**Tổng kết:** Quiz Generator đã hoàn thành với 952 câu hỏi VHF + Radar + Kíp Trưởng, dark theme xanh xám tối dịu mắt, giao diện đồng bộ, bookmark, luyện tập câu sai, thống kê điểm số, PWA (cài đặt như app trên điện thoại), GitHub Pages hosting — chạy offline hoàn toàn.

**Pipeline rebuild:** `rebuild.py` (pandas column-name-based) + `corrections.json` → `all_questions.json` → embed vào `index.html` + `add_radar.js`.
