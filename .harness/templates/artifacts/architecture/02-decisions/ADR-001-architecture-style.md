# ADR-001: Lựa Chọn Phong Cách Kiến Trúc Hệ Thống (Modular Monolith)

## 1. Metadata & Trạng Thái

- **Trạng thái**: `Đã duyệt`
- **Ngày ban hành**: `2026-11-11`
- **Người đề xuất**: `Software Architect (SA)`
- **Người phê duyệt**: `Technical Reviewer`
- **Quyết định bị thay thế**: `N/A`

---

## 2. Bối cảnh và Vấn đề Cần Quyết định (Context and Problem Statement)

Hệ thống cần phục vụ quy mô ban đầu với lưu lượng giao dịch trung bình và yêu cầu thời gian đưa tính năng ra thị trường (Time-to-Market) nhanh. Đội ngũ phát triển có quy mô vừa (5-10 kỹ sư), ưu tiên tính đơn giản trong triển khai, kiểm thử cục bộ và giám sát lỗi tập trung mà không chịu chi phí vận hành phân tán (network latency, distributed transaction, service mesh). Tuy nhiên, kiến trúc phải đảm bảo tính module hóa cao để sẵn sàng tách thành các microservices độc lập trong tương lai khi lưu lượng tăng trưởng vượt bậc.

---

## 3. Tiêu chí Ra Quyết định (Decision Drivers)

1. **Độ phức tạp Vận hành**: Hạn chế tối đa số lượng containers độc lập cần quản lý ở giai đoạn hiện tại.
2. **Tính toàn vẹn Dữ liệu (ACID)**: Yêu cầu giao dịch tài chính/nghiệp vụ cốt lõi phải đảm bảo tính nhất quán tức thì (strong consistency).
3. **Ranh giới Domain (Decoupling)**: Các module phải phân định rõ ràng trách nhiệm nghiệp vụ, không rò rỉ phụ thuộc chéo.
4. **Chi phí Hạ tầng**: Tối ưu chi phí server và băng thông mạng nội bộ.

---

## 4. Các Phương án Đã Xem xét (Considered Options)

### Phương án A: Kiến trúc Đơn khối Module hóa (Modular Monolith)
- **Mô tả**: Tổ chức mã nguồn trong một codebase duy nhất, chia thành các package/module nghiệp vụ biệt lập với interface contract nghiêm ngặt và database chung nhưng phân chia schema/bảng rõ ràng.
- **Ưu điểm (+)**:
  - Triển khai và debug cực kỳ đơn giản, không phát sinh chi phí phân tán mạng.
  - Hỗ trợ ACID transaction tự nhiên giữa các thực thể trong cùng một quy trình nghiệp vụ.
  - Dễ dàng tái cấu trúc (refactor) và chia sẻ DTOs/Domain models nội bộ.
- **Nhược điểm (-)**:
  - Nguy cơ các lập trình viên gọi chéo internal functions nếu không có linter/kiểm tra ranh giới tự động.
  - Phải scale toàn bộ ứng dụng cùng nhau khi có một module chịu tải cao.

### Phương án B: Kiến trúc Vi dịch vụ Phân tán (Microservices)
- **Mô tả**: Tách ngay từ đầu thành 4-6 services độc lập, giao tiếp qua HTTP/gRPC và Message Broker (Kafka).
- **Ưu điểm (+)**:
  - Scale độc lập từng service theo nhu cầu tài nguyên.
  - Độc lập về công nghệ và chu kỳ release cho từng nhóm nhỏ.
- **Nhược điểm (-)**:
  - Chi phí vận hành hạ tầng (K8s, Istio, tracing) rất lớn so với quy mô hiện tại.
  - Cực kỳ phức tạp trong việc xử lý phân tán giao dịch (Saga pattern, 2PC, eventual consistency).
  - Tăng độ trễ mạng nội bộ (network hop) cho mỗi luồng nghiệp vụ.

---

## 5. Quyết định Lựa chọn và Lý do Căn cứ (Decision Outcome)

**Quyết định**: Chọn **Phương án A: Modular Monolith** cho hệ thống.

**Căn cứ lựa chọn**:
1. Phù hợp hoàn hảo với quy mô đội ngũ và mục tiêu giao hàng nhanh của giai đoạn hiện tại.
2. Vẫn đảm bảo tính kỷ luật kiến trúc: Khi cần thiết, từng module đã được thiết kế cô lập có thể dễ dàng tách ra thành một Microservice độc lập mà không cần viết lại logic nghiệp vụ.

---

## 6. Hệ quả & Đánh đổi (Consequences & Trade-offs)

### Lợi ích Thu được
- Đơn giản hóa CI/CD pipeline và môi trường phát triển cục bộ của Developer.
- Đảm bảo tính nhất quán dữ liệu giao dịch 100% qua local DB transactions.
- Giảm thiểu độ trễ giao tiếp giữa các thành phần xuống mức microsecond.

### Rủi ro Chấp nhận & Biện pháp Giảm thiểu
- **Rủi ro rò rỉ ranh giới (Domain leakage)**: Lập trình viên có thể vô tình import trực tiếp implementation nội bộ của module khác.
  - *Biện pháp*: Thiết lập rule kiểm tra import tĩnh tự động (ArchUnit / Ruff import restriction) trong harness quality gate.

---

## 7. Ranh giới Áp dụng & Quy tắc Bắt buộc Tuân thủ (Invariants)

- **Binds**: Áp dụng cho toàn bộ cấu trúc mã nguồn trong `src/` và các gói mở rộng.
- **Prevents**: Nghiêm cấm mọi hành vi gọi trực tiếp cơ sở dữ liệu hoặc import các lớp nội bộ (`*.internal.*`, `*.infrastructure.*`) từ module khác.
- **Invariants**:
  1. Giao tiếp giữa các module chỉ được phép thông qua Public Service Interface hoặc Event Bus nội bộ.
  2. Mỗi module chịu trách nhiệm hoàn toàn về các bảng dữ liệu (schema) thuộc phạm vi của mình.

---

## 8. Phương pháp Kiểm chứng Kiến trúc (Architecture Validation)

- **Automated Guard**: Harness gate kiểm tra tính toàn vẹn ranh giới miền (`rejected:domain_boundary_violation:direct_internal_coupling`).
- **Test Case**: Unit tests kiểm tra dependency injection và mock contract interfaces giữa các modules.
