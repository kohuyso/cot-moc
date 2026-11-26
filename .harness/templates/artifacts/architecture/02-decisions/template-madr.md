# ADR-xxx: [Tên Quyết Định Kiến Trúc]

## 1. Metadata & Trạng Thái

- **Trạng thái**: `Đề xuất` | `Đã duyệt` | `Thay thế` | `Hủy`
- **Ngày ban hành**: `YYYY-MM-DD`
- **Người đề xuất**: `[Họ và tên / Vai trò]`
- **Người phê duyệt**: `[Technical Reviewer / Lead Architect]`
- **Quyết định bị thay thế (nếu có)**: `N/A` hoặc `ADR-yyy`

---

## 2. Bối cảnh và Vấn đề Cần Quyết định (Context and Problem Statement)

`[Mô tả bối cảnh kỹ thuật hoặc nghiệp vụ dẫn đến sự cần thiết phải đưa ra quyết định kiến trúc này. Nêu rõ vấn đề cốt lõi, phạm vi ảnh hưởng và các ràng buộc hiện hữu của hệ thống.]`

---

## 3. Tiêu chí Ra Quyết định (Decision Drivers)

1. **Yêu cầu Nghiệp vụ**: `[Khả năng đáp ứng nghiệp vụ, thời gian bàn giao MVP, tính linh hoạt]`
2. **Yêu cầu Phi chức năng (NFR)**: `[Hiệu năng, độ trễ, khả năng mở rộng, tính sẵn sàng cao]`
3. **Chi phí & Độ phức tạp**: `[Chi phí hạ tầng, độ phức tạp vận hành, thời gian đào tạo đội ngũ]`
4. **Bảo mật & Tuân thủ**: `[Mức độ an toàn dữ liệu, phòng chống gian lận, tuân thủ tiêu chuẩn]`

---

## 4. Các Phương án Đã Xem xét (Considered Options)

### Phương án A: `[Tên Phương án A - Ví dụ: Giải pháp lựa chọn]`
- **Mô tả**: `[Tóm tắt cách tiếp cận kỹ thuật]`
- **Ưu điểm (+)**:
  - `[Lợi thế 1]`
  - `[Lợi thế 2]`
- **Nhược điểm (-)**:
  - `[Hạn chế 1]`
  - `[Hạn chế 2]`

### Phương án B: `[Tên Phương án B - Ví dụ: Giải pháp thay thế]`
- **Mô tả**: `[Tóm tắt cách tiếp cận kỹ thuật]`
- **Ưu điểm (+)**:
  - `[Lợi thế 1]`
- **Nhược điểm (-)**:
  - `[Hạn chế 1]`
  - `[Hạn chế 2]`

---

## 5. Quyết định Lựa chọn và Lý do Căn cứ (Decision Outcome)

**Quyết định**: Chọn **Phương án `[A/B]`** vì đáp ứng tốt nhất các tiêu chí ưu tiên:
- **Căn cứ 1**: `[Lý do kỹ thuật / nghiệp vụ thuyết phục nhất]`
- **Căn cứ 2**: `[Sự phù hợp với hiện trạng công nghệ và nguồn lực dự án]`

---

## 6. Hệ quả & Đánh đổi (Consequences & Trade-offs)

### Lợi ích Thu được (Positive Consequences)
- `[Lợi ích tích cực 1]`
- `[Lợi ích tích cực 2]`

### Chi phí / Rủi ro Chấp nhận Đánh đổi (Negative Consequences & Mitigations)
- `[Rủi ro/đánh đổi 1]` -> *Biện pháp giảm thiểu*: `[Giải pháp khắc phục]`
- `[Rủi ro/đánh đổi 2]` -> *Biện pháp giảm thiểu*: `[Giải pháp khắc phục]`

---

## 7. Ranh giới Áp dụng & Quy tắc Bắt buộc Tuân thủ (Invariants)

- **Binds (Phạm vi ràng buộc)**: `[Các module, thành phần hoặc lớp code bắt buộc phải tuân theo quyết định này]`
- **Prevents (Ngăn chặn sai lệch)**: `[Những hành vi code, cấu hình hoặc kiến trúc bị nghiêm cấm hoàn toàn]`
- **Invariants (Bất biến kỹ thuật)**:
  1. `[Bất biến 1: Không được phép ...]`
  2. `[Bất biến 2: Bắt buộc phải ...]`

---

## 8. Phương pháp Kiểm chứng Kiến trúc (Architecture Validation)

- **Automated Rule / Linter**: `[Kiểm tra tĩnh qua Ruff / ESLint / ArchUnit hoặc AST check]`
- **Test Case kiểm chứng**: `[Mã test case hoặc kịch bản kiểm thử tự động xác nhận tính đúng đắn của quyết định]`
- **Code Review Check**: `[Tiêu chí thẩm định bắt buộc trong checklist review code]`
