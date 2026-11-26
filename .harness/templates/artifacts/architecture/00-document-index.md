# Enterprise Architecture Artifact Suite: Document Index & Governance

## 1. Document Metadata

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Dự án** | `[Project Name]` |
| **Run ID** | `[run-YYYYMMDD-HHMMSS-xxxxxx]` |
| **Phiên bản Kiến trúc** | `1.0.0` |
| **Trạng thái phê duyệt** | `Đề xuất` (Chờ thẩm định bởi Technical Reviewer) |
| **Chủ trì Kiến trúc (SA Owner)** | `Software Architect (SA)` |
| **Người thẩm định (Reviewer)** | `Independent Technical Reviewer` |
| **Ngày cập nhật cuối** | `YYYY-MM-DD` |

---

## 2. Quy ước Trạng thái Nội dung (Content Status Convention)

Mọi cấu phần, quyết định, tích hợp và thuộc tính chất lượng trong bộ tài liệu kiến trúc bắt buộc phải được gắn một trong 5 nhãn trạng thái chuẩn hóa dưới đây:

| Nhãn Trạng Thái | Định nghĩa & Ý nghĩa Pháp lý / Kỹ thuật | Trách nhiệm & Ràng buộc Thực thi |
| :--- | :--- | :--- |
| **`Đã xác nhận`** | Đã được xác thực từ yêu cầu nghiệp vụ (URD/SRS), tài liệu chính thức của đối tác hoặc đã được kiến trúc sư trưởng phê duyệt. | Đầy đủ căn cứ, bắt buộc Developer và Tester tuân thủ 100%. |
| **`Đề xuất`** | Đang được đề xuất bởi Software Architect hoặc nhóm kỹ thuật; đang chờ phản biện từ Technical Reviewer. | Chưa phải quyết định cuối cùng; cần được chốt trước khi bước vào `DEV_CODING`. |
| **`Chưa xác định`** | Thiếu dữ liệu thực tế, phụ thuộc đối tác ngoài hoặc đang chờ phản hồi làm rõ. | **Nghiêm cấm bịa đặt thông số**. Bắt buộc ghi chú đầu mối chịu trách nhiệm và deadline làm rõ. |
| **`Không áp dụng`** | Hạng mục nằm ngoài phạm vi kiến trúc của run hiện tại hoặc công nghệ không áp dụng. | Ghi rõ lý do loại trừ để đảm bảo tính minh bạch ranh giới. |
| **`Chưa kiểm chứng`** | Đã có giả thuyết kỹ thuật hoặc thiết kế nhưng chưa qua thử nghiệm tải, đo đạc hoặc PoC thực tế. | Bắt buộc phải có kịch bản Spike/PoC kiểm chứng trong kế hoạch triển khai. |

---

## 3. Danh mục Bộ Tài liệu Kiến trúc (Master Architecture Suite Index)

Bộ tài liệu kiến trúc phân cấp được tổ chức theo chuẩn **Enterprise Architecture Artifact Suite**:

| STT | Mã Tài Liệu | Tên Tài Liệu & Đường dẫn | Trọng tâm Nghiệp vụ & Kỹ thuật | Người Sở hữu | Trạng thái Hiện tại |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 00 | `ARCH-IDX` | [00-document-index.md](00-document-index.md) | Mục lục tổng thể, quy ước trạng thái và phân quyền hồ sơ kiến trúc | SA Lead | `Đã xác nhận` |
| 01 | `ARCH-SAD` | [01-solution-architecture.md](01-solution-architecture.md) | Tài liệu kiến trúc tổng thể theo chuẩn quốc tế **arc42 (12 sections)** & C4 Model | SA Lead | `Đề xuất` |
| 02 | `ARCH-ADR` | [02-decisions/](02-decisions/) | Sổ bộ quyết định kiến trúc theo chuẩn **MADR** (mỗi ADR 1 file độc lập) | SA / Tech Lead | `Đề xuất` |
| 03 | `ARCH-NFR` | [03-nfr-and-validation.md](03-nfr-and-validation.md) | Ma trận chỉ tiêu chất lượng (NFR) 8 cột & kế hoạch đo lường kiểm chứng SLA | SA / QA Lead | `Đề xuất` |
| 04 | `ARCH-INT` | [04-integration/](04-integration/) | Đặc tả tích hợp hệ thống, API Contract OAS 3.1 (`openapi.yaml`) & luồng Message | SA / Integration | `Đề xuất` |
| 05 | `ARCH-DAT` | [05-data/](05-data/) | Kiến trúc dữ liệu, mô hình lưu trữ, phân vùng và từ điển dữ liệu thực thể chi tiết | Data Architect | `Đề xuất` |
| 06 | `ARCH-SEC` | [06-security/](06-security/) | Mô hình mối đe dọa (STRIDE), IAM, RBAC matrix, quản lý secret & OWASP Top 10 | Security Architect | `Đề xuất` |
| 07 | `ARCH-OPS` | [07-deployment-and-operations/](07-deployment-and-operations/) | Kiến trúc hạ tầng, CI/CD, Container, HA/DR, Observability (Metrics, Logs, Traces) | DevOps / SRE | `Đề xuất` |

---

## 4. Truy vết Yêu cầu & Lịch sử Thay đổi (Traceability & Change History)

### 4.1. Ma trận Ánh xạ Nguồn Yêu cầu (Traceability to Source Artifacts)
- **Tài liệu Yêu cầu nghiệp vụ đầu vào**: `artifacts/requirement-analysis.md` (hoặc `artifacts/srs.md`)
- **Bộ dữ liệu yêu cầu máy đọc được**: `artifacts/requirement.json`
- **Đặc tả chức năng màn hình/trường**: `artifacts/fsd.json` & `artifacts/fsd.md`

### 4.2. Nhật ký Sửa đổi (Revision Log)
| Phiên bản | Ngày | Người thực hiện | Tóm tắt Thay đổi | Quyết định/ADR liên quan |
| :--- | :--- | :--- | :--- | :--- |
| `1.0.0` | `YYYY-MM-DD` | `Software Architect` | Khởi tạo toàn bộ bộ hồ sơ kiến trúc Enterprise Architecture Suite | ADR-001 |
