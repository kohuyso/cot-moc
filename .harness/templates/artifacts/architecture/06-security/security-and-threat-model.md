# Security Architecture & Threat Model (STRIDE / OWASP)

**Hệ thống**: `[Project Name]`  
**Mục tiêu**: Nhận diện mối đe dọa an toàn thông tin theo mô hình **STRIDE**, thiết lập ma trận phân quyền **RBAC**, quản lý thông tin bí mật (Secrets) và biện pháp phòng chống **OWASP Top 10**.  
**Liên kết mục lục**: [00-document-index.md](00-document-index.md)

---

## 1. Phân tích Mối đe dọa (STRIDE Threat Modeling)

| Nguy cơ (STRIDE) | Kịch bản Tấn công Tiềm ẩn | Đối tượng Bị nhắm đến | Mức độ | Biện pháp Phòng vệ Kiến trúc (Mitigation) |
| :--- | :--- | :--- | :---: | :--- |
| **Spoofing** (Giả mạo) | Kẻ tấn công tạo token giả mạo hoặc replay token cũ | API Gateway & Core Service | `HIGH` | Xác thực JWT qua chữ ký số RSA/JWKS, kiểm tra thời hạn `exp` và `jti` |
| **Tampering** (Can thiệp) | Chỉnh sửa payload số tiền khi gửi request thanh toán | Controller & Payment API | `CRITICAL` | Ký số payload (HMAC Signature), kiểm tra tính toàn vẹn tại Gateway |
| **Repudiation** (Chối bỏ) | Người dùng chối bỏ việc đã thực hiện chuyển dịch trạng thái | Bảng giao dịch nghiệp vụ | `MEDIUM` | Ghi log kiểm toán bất biến (Append-only) vào `tbl_audit_logs` kèm định danh |
| **Information Disclosure** (Lộ lọt thông tin) | Rò rỉ dữ liệu thẻ hoặc PII qua thông điệp lỗi hoặc log | Logs, API Error Response | `HIGH` | Masking dữ liệu nhạy cảm (số thẻ chỉ lưu 4 số cuối), chuẩn lỗi `ERR-xx-xxx` |
| **Denial of Service** (Từ chối dịch vụ) | Bắn hàng loạt request để làm tràn bộ nhớ/CPU | Toàn bộ hệ thống | `HIGH` | Rate Limiting tại API Gateway (100 req/min/IP), Connection Pooling giới hạn |
| **Elevation of Privilege** (Leo thang đặc quyền) | Người dùng thường gọi API dành riêng cho Quản trị viên | Admin Endpoints | `CRITICAL` | RBAC Middleware kiểm tra quyền chặt chẽ trước khi dispatch request |

---

## 2. Ma trận Phân quyền Vai trò (RBAC Matrix)

| Vai trò (Role) | Mô tả Quyền hạn | `GET /resources` | `POST /resources` | `PUT /resources/{id}` | `DELETE /resources/{id}` |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`ROLE_ANONYMOUS`** | Khách chưa đăng nhập | `ALLOW` (Công khai) | `DENY` (401) | `DENY` (401) | `DENY` (401) |
| **`ROLE_USER`** | Người dùng đã đăng nhập | `ALLOW` (Dữ liệu của mình) | `ALLOW` | `ALLOW` (Nếu sở hữu) | `DENY` (403) |
| **`ROLE_OPERATOR`** | Nhân viên vận hành hỗ trợ | `ALLOW` (Toàn bộ) | `DENY` | `ALLOW` (Duyệt đơn) | `DENY` (403) |
| **`ROLE_ADMIN`** | Quản trị viên hệ thống | `ALLOW` (Toàn bộ) | `ALLOW` | `ALLOW` | `ALLOW` |

---

## 3. Quản lý Bí mật & Thông tin Nhạy cảm (Secret Management)

1. **Nghiêm cấm Hardcode**: Tuyệt đối không lưu trữ database passwords, API keys, private keys trong mã nguồn hoặc git repository.
2. **Cơ chế Tiêm cấu hình**: Sử dụng HashiCorp Vault hoặc Kubernetes Secrets được tiêm vào ứng dụng dưới dạng biến môi trường (Environment Variables) trong thời gian chạy (Runtime).
3. **Luân chuyển Khóa (Key Rotation)**: Khóa ký JWT và database credentials phải được thiết lập quy trình tự động luân chuyển định kỳ 90 ngày.

---

## 4. Phòng chống OWASP Top 10

- **Injection (SQL/Command)**: 100% truy vấn cơ sở dữ liệu sử dụng ORM hoặc Parameterized Queries. Cấm tuyệt đối nối chuỗi SQL thủ công.
- **Security Misconfiguration**: Vô hiệu hóa tính năng debug mode, tắt header `X-Powered-By`, chỉ mở các cổng mạng thiết yếu.
- **CORS & CSRF**: Thiết lập `SameSite=Strict` cho cookies xác thực; cấu hình CORS chỉ cho phép các domain frontend được cấp phép tường minh.
