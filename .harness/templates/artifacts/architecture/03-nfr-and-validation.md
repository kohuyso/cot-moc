# NFR & Quality Attribute Validation Matrix (Ma trận NFR & Kiểm chứng Chất lượng)

**Hệ thống**: `[Project Name]`  
**Mục tiêu**: Định lượng hóa toàn bộ yêu cầu phi chức năng (NFR) từ URD/SRS, gắn trách nhiệm xác nhận, giải pháp thiết kế đáp ứng và kế hoạch kiểm thử tự động truy vết 2 chiều sang Test Plan.  
**Liên kết mục lục**: [00-document-index.md](00-document-index.md)

---

## 1. Nguyên tắc Đo lường & Thẩm định Chỉ tiêu Chất lượng

1. **Định lượng tuyệt đối**: Nghiêm cấm các mô tả cảm tính như "phản hồi nhanh", "hệ thống chịu tải tốt", "dễ sử dụng". Mọi chỉ số bắt buộc có con số đo đạc cụ thể (ms, RPS, %, RTO/RPO).
2. **Truy vết 2 chiều (Bidirectional Traceability)**: Mỗi NFR phải truy vết từ mã nguồn yêu cầu trong `requirement.json` sang giải pháp thiết kế kiến trúc và sang test case cụ thể trong `artifacts/test-plan.md`.
3. **Phân định Trạng thái Rõ ràng**: Áp dụng 5 nhãn trạng thái chuẩn (`Đã xác nhận`, `Đề xuất`, `Chưa xác định`, `Không áp dụng`, `Chưa kiểm chứng`).

---

## 2. Ma trận NFR & Kế hoạch Đo lường Kiểm chứng (8 Cột Bắt buộc)

| Mã NFR | Kịch bản & Tác nhân | Chỉ số & Ngưỡng SLA | Điều kiện đo | Giải pháp thiết kế đáp ứng | Người xác nhận NFR | Kế hoạch Test kiểm chứng | Trạng thái hiện tại |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **`NFR-001`** | **Hiệu năng & Độ trễ**: Người dùng cuối thực hiện truy vấn danh sách giao dịch qua API Gateway | Thời gian phản hồi: **p95 $\le 500$ms**, **p99 $\le 1000$ms**; Tải: **200 RPS** | Môi trường Staging, database có sẵn 1 triệu bản ghi mô phỏng thực tế | Caching kết quả phân trang tại Redis (TTL 60s); đánh composite index trên `(user_id, created_at DESC)` | SA & QA Lead | Kịch bản Locust/k6 kiểm thử tải liên tục trong 15 phút (`TC-PERF-001`) | `Đề xuất` |
| **`NFR-002`** | **Tính Sẵn sàng & Chống lỗi (HA/DR)**: Một node ứng dụng hoặc vùng dữ liệu (AZ) gặp sự cố vật lý đột ngột | Tỷ lệ khả dụng: **$\ge 99.9\%$**; Thời gian tự phục hồi: **RTO $\le 30$ giây**, **RPO $= 0$** (không mất dữ liệu) | Tắt giả lập (kill process) đột ngột 1 Pod trên cụm Kubernetes khi đang có tải | Triển khai Multi-AZ với Kubernetes Pod replicas $\ge 2$; PostgreSQL Synchronous Replication | SRE Lead & DevOps | Chaos engineering test: ngắt kết nối Pod ngẫu nhiên khi chạy automation test (`TC-CHAOS-001`) | `Đề xuất` |
| **`NFR-003`** | **Bảo mật & Kiểm soát Truy cập**: Kẻ tấn công cố tình chèn payload SQL Injection hoặc truy cập tài nguyên trái phép | **Zero** lỗ hổng thuộc OWASP Top 10; **100%** endpoints được xác thực và bảo vệ RBAC | Quét bảo mật tự động bằng SAST/DAST và kiểm thử hộp đen | Sử dụng ORM/Parameterized SQL; Middleware RBAC kiểm tra quyền trước mọi Controller method | Security Architect | Quét SAST tự động qua SonarQube/Semgrep + Security Test Suite (`TC-SEC-001`) | `Đã xác nhận` |
| **`NFR-004`** | **Xử lý Đồng thời & Chống Trùng lặp**: 2 yêu cầu thanh toán cùng mã giao dịch được gửi tới đồng thời trong khoảng $\le 10$ms | **0%** xảy ra trừ tiền kép; **100%** request trùng nhận mã phản hồi `409 Conflict` hoặc kết quả idempotent | Bắn 20 threads đồng thời cùng chung `Idempotency-Key` và tham số payload | Redis Distributed Lock với cơ chế NX/PX + Ràng buộc Unique Key tại bảng cơ sở dữ liệu | SA Lead | Concurrency Test Suite bắn song song qua multi-threading test client (`TC-CONC-001`) | `Đã xác nhận` |
| **`NFR-005`** | **Khả năng Bảo trì & Module Hóa**: Kỹ sư bảo trì thay đổi logic nội bộ của một module | Tác động lan tỏa (Blast radius) $= 0$ sang các module khác; Coverage unit test **$\ge 80\%$** | Chạy kiểm tra tĩnh AST và phân tích biểu đồ phụ thuộc dependency | Ranh giới Modular Monolith nghiêm ngặt, giao tiếp qua Interface DTO, cấm gọi direct internal | Tech Lead | Kiểm tra tự động qua Harness Architecture Gate (`TC-ARCH-001`) | `Đã xác nhận` |
| **`NFR-006`** | **Lưu vết & Kiểm toán (Auditability)**: Người dùng thực hiện thay đổi trạng thái tài nguyên quan trọng | **100%** hành động được ghi vết chi tiết; Độ trễ ghi log không ảnh hưởng request chính (**$\le 5$ms**) | Kiểm tra bảng audit log sau khi thực hiện 1,000 giao dịch thay đổi dữ liệu | Ghi log bất biến (Append-only) bất đồng bộ qua hàng đợi nội bộ hoặc Background Task | Compliance Officer | Audit Trail Verification Test Suite (`TC-AUDIT-001`) | `Đã xác nhận` |

---

## 3. Quy trình Kiểm chứng & Báo cáo Nghiệm thu SLA

1. **Giai đoạn Thiết kế (SA_DESIGN)**: Ma trận NFR được thiết lập với ngưỡng SLA và giải pháp thiết kế tương ứng.
2. **Giai đoạn Thiết kế Test (TEST_DESIGN)**: QA chuyển hóa 100% các dòng trong ma trận thành Test Cases cụ thể trong `artifacts/test-plan.md`.
3. **Giai đoạn Kiểm thử (TEST_EXECUTION & QA_REVIEW)**: Thực hiện đo đạc thực tế, ghi lại bằng chứng khách quan (exit codes, latency percentiles, memory profiling) vào `artifacts/test-report.md`.
4. **Nghiệm thu**: Bất kỳ chỉ số nào vi phạm ngưỡng SLA mà không có lý do được phê duyệt sẽ kích hoạt `REJECT` hoặc `PUSHBACK` tại cổng QA.
