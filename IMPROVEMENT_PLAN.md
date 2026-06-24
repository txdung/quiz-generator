# Kế hoạch Cải tiến Dự án Quiz Generator 🚀

Tài liệu này ghi lại các đề xuất cải thiện hệ thống để nâng cao tính bền bỉ, khả năng mở rộng và trải nghiệm người dùng cho dự án.

## 1. Quy trình Xử lý Dữ liệu & Tự động hóa (Ưu tiên Cao)
Mục tiêu: Làm cho script `rebuild2.py` trở nên "bền" hơn trước những thay đổi của file Excel đầu vào.

*   **Sử dụng thư viện Pandas:** 
    - Chuyển từ việc đọc cột theo chỉ số (`ws.cell(row, index)`) sang đọc bằng **Tên Cột**. Điều này giúp script không bị lỗi nếu người dùng chèn thêm hoặc xóa bớt các cột phụ trong Excel.
*   **Chuẩn hóa dữ liệu (Data Integrity):** 
    - Loại bỏ việc "sửa lỗi cứng" ngay trong code Python (ví dụ: `if 'ISLS' in text...`). 
    - **Giải pháp:** Sửa trực tiếp tại file nguồn Excel hoặc sử dụng một file cấu hình riêng (`corrections.json`) để ghi đè các đáp án sai khi chạy script. Điều này giúp logic lập trình tách biệt hoàn toàn với nội dung câu hỏi.
*   **Thêm bước Kiểm tra (Validation):** 
    - Tự động kiểm tra và báo lỗi nếu: trùng số thứ tự câu hỏi, thiếu phương án A/B/C/D, hoặc đáp án đúng không nằm trong phạm vi cho phép.

## 2. Quản lý Nội dung & Khả năng Mở rộng
Mục tiêu: Chuẩn bị cho việc ngân hàng câu hỏi tăng lên quy mô lớn (hàng nghìn câu).

*   **Chuyển đổi sang Cơ sở dữ liệu (SQLite):** 
    - Thay vì nạp một file JSON khổng lồ vào bộ nhớ điện thoại, sử dụng SQLite để truy vấn nhanh các nhóm chủ đề cụ thể. Điều này giúp ứng dụng chạy mượt mà hơn trên thiết bị di động cấu hình thấp.
*   **Hỗ trợ Hình ảnh minh họa:** 
    - Bổ sung trường `image_url` hoặc `image_file` trong JSON/Database để hiển thị sơ đồ, biểu đồ radar cho các câu hỏi kỹ thuật phức tạp.

## 3. Cải thiện Giao diện & Trải nghiệm Người dùng (UX)
Mục tiêu: Biến ứng dụng thành một công cụ học tập chuyên nghiệp và linh hoạt hơn.

*   **Tính năng Tìm kiếm & Bộ lọc:** Cho phép người dùng tìm nhanh câu hỏi theo từ khóa hoặc chọn ôn luyện riêng cho từng chủ đề nhỏ thay vì phải làm cả bảng tính lớn.
*   **Tối ưu hóa PWA (Progressive Web App):** 
    - Đảm bảo dữ liệu lịch sử học tập và "danh sách câu sai" được lưu trữ an toàn trong `IndexedDB` để không bị mất khi trình duyệt tự dọn dẹp bộ nhớ đệm.
*   **Tùy chỉnh Giao diện:** Thêm các chế độ như Dark Mode hoặc thay đổi kích thước font chữ để hỗ trợ việc học tập lâu dài mà không gây mỏi mắt.

## 4. Quy trình Phát triển (DevOps)
Mục tiêu: Đảm bảo tính ổn định khi nâng cấp mã nguồn.

*   **Viết Unit Test:** Xây dựng các bộ kiểm thử tự động cho script Python để đảm bảo việc thay đổi code hoặc cấu trúc file Excel không làm hỏng dữ liệu đầu ra JSON hiện có.

---
*Tài liệu được tạo bởi AI Assistant - [Ngày: 2026-06-24]*
