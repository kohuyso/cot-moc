# Data Dictionary & Physical Entity Specification (Từ điển Dữ liệu Thực thể)

**Hệ thống**: `[Project Name]`  
**Cơ sở Dữ liệu**: `[SQL Server 2022 / PostgreSQL 16+ / CSDL chốt theo TSD/SAD]`  
**Liên kết mục lục**: [00-document-index.md](00-document-index.md) | **Kiến trúc dữ liệu**: [data-architecture.md](data-architecture.md)

> [!IMPORTANT]
> **Quy tắc Kiểm Soát Chất Lượng Bắt Buộc (Quality Gate Invariant)**:
> 100% các bảng dữ liệu thực thể trong hệ thống bắt buộc phải có bảng đặc tả chi tiết tối thiểu 4 cột (gồm Khóa chính PK, các trường dữ liệu nghiệp vụ, và các trường kiểm toán audit: `created_at`, `updated_at`).
> Tuyệt đối cấm tình trạng chỉ liệt kê 1 dòng mô tả tên bảng mà không có bảng định nghĩa cột chi tiết.

---

## 1. Danh mục Bảng Dữ liệu (Entity Table Registry)

| Tên Bảng | Module Sở hữu | Mục đích Nghiệp vụ | Loại Bảng | Chiến lược Phân vùng |
| :--- | :--- | :--- | :--- | :--- |
| `tbl_users` | `module_identity` | Lưu trữ thông tin tài khoản và trạng thái người dùng | Master | Không phân vùng |
| `tbl_orders` | `module_core_business` | Quản lý thông tin đơn hàng và trạng thái vòng đời | Transactional | Không phân vùng |
| `tbl_order_items` | `module_core_business` | Chi tiết từng mặt hàng thuộc đơn hàng | Transactional | Không phân vùng |
| `tbl_payments` | `module_integration` | Thông tin giao dịch thanh toán và đối soát đối tác | Transactional | Phân vùng theo năm |
| `tbl_audit_logs` | `module_audit` | Lưu vết nhật ký thay đổi dữ liệu phục vụ kiểm toán | Log (Append-only) | Phân vùng theo tháng |

---

## 2. Chi tiết Định nghĩa Trường Từng Bảng (Field-level Schema Definitions)

### 2.1. Bảng `tbl_users`
Quản lý danh sách người dùng trong hệ thống.

| Tên Cột | Kiểu Dữ liệu | Khóa (PK/FK) | Nullable | Ràng buộc / Mặc định | Mô tả Nghiệp vụ & Ghi chú |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `id` | `UUID / UNIQUEIDENTIFIER` | PK | NO | `PRIMARY KEY, DEFAULT NEWID() / gen_random_uuid()` | Khóa chính duy nhất của người dùng |
| `username` | `VARCHAR(100) / NVARCHAR(100)` | - | NO | `UNIQUE` | Tên đăng nhập người dùng |
| `email` | `VARCHAR(255) / NVARCHAR(255)` | - | NO | `UNIQUE` | Địa chỉ email chính thức |
| `password_hash` | `VARCHAR(255) / NVARCHAR(255)` | - | NO | - | Chuỗi băm mật khẩu (Argon2id hoặc Bcrypt) |
| `status` | `VARCHAR(30) / NVARCHAR(30)` | - | NO | `DEFAULT 'ACTIVE'` | Trạng thái: `ACTIVE`, `INACTIVE`, `LOCKED` |
| `created_at` | `DATETIMEOFFSET / TIMESTAMPTZ` | - | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm tạo bản ghi |
| `updated_at` | `DATETIMEOFFSET / TIMESTAMPTZ` | - | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm cập nhật cuối cùng |

---

### 2.2. Bảng `tbl_orders`
Lưu trữ thông tin đơn hàng và tổng giá trị.

| Tên Cột | Kiểu Dữ liệu | Nullable | Ràng buộc / Mặc định | Mô tả Nghiệp vụ & Ghi chú |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `UUID` | NO | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Khóa chính định danh đơn hàng |
| `user_id` | `UUID` | NO | `REFERENCES tbl_users(id)` | Khóa ngoại trỏ tới người đặt hàng |
| `order_code` | `VARCHAR(50)` | NO | `UNIQUE` | Mã đơn hàng hiển thị cho khách hàng (ORD-YYYYMMDD-XXXX) |
| `total_amount` | `NUMERIC(15, 2)`| NO | `CHECK (total_amount >= 0)` | Tổng giá trị đơn hàng (VNĐ) |
| `status` | `VARCHAR(30)` | NO | `DEFAULT 'PENDING'` | Trạng thái: `PENDING`, `CONFIRMED`, `PAID`, `CANCELLED` |
| `version` | `INT` | NO | `DEFAULT 0` | Phiên bản phục vụ Optimistic Concurrency Control |
| `created_at` | `TIMESTAMPTZ` | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm tạo đơn hàng |
| `updated_at` | `TIMESTAMPTZ` | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm cập nhật trạng thái đơn |

---

### 2.3. Bảng `tbl_order_items`
Chi tiết các sản phẩm trong đơn hàng.

| Tên Cột | Kiểu Dữ liệu | Nullable | Ràng buộc / Mặc định | Mô tả Nghiệp vụ & Ghi chú |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `UUID` | NO | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Khóa chính chi tiết sản phẩm |
| `order_id` | `UUID` | NO | `REFERENCES tbl_orders(id) ON DELETE CASCADE`| Khóa ngoại trỏ về đơn hàng |
| `item_name` | `VARCHAR(255)`| NO | - | Tên sản phẩm/dịch vụ |
| `quantity` | `INT` | NO | `CHECK (quantity > 0)` | Số lượng đặt mua |
| `unit_price` | `NUMERIC(15, 2)`| NO | `CHECK (unit_price >= 0)` | Đơn giá tại thời điểm đặt hàng |

---

### 2.4. Bảng `tbl_payments`
Quản lý giao dịch thanh toán kết nối đối tác.

| Tên Cột | Kiểu Dữ liệu | Nullable | Ràng buộc / Mặc định | Mô tả Nghiệp vụ & Ghi chú |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `UUID` | NO | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Khóa chính định danh thanh toán |
| `order_id` | `UUID` | NO | `REFERENCES tbl_orders(id)` | Khóa ngoại liên kết tới đơn hàng |
| `payment_ref` | `VARCHAR(100)`| NO | `UNIQUE` | Mã giao dịch tham chiếu từ Cổng thanh toán đối tác |
| `amount` | `NUMERIC(15, 2)`| NO | `CHECK (amount > 0)` | Số tiền thực hiện thanh toán |
| `status` | `VARCHAR(30)` | NO | `DEFAULT 'INITIATED'` | Trạng thái: `INITIATED`, `SUCCESS`, `FAILED` |
| `created_at` | `TIMESTAMPTZ` | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm phát sinh giao dịch thanh toán |

---

### 2.5. Bảng `tbl_audit_logs`
Bảng ghi vết kiểm toán hệ thống (Append-Only).

| Tên Cột | Kiểu Dữ liệu | Nullable | Ràng buộc / Mặc định | Mô tả Nghiệp vụ & Ghi chú |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `BIGSERIAL` | NO | `PRIMARY KEY` | Khóa chính tự tăng |
| `entity_name` | `VARCHAR(100)`| NO | - | Tên thực thể bị tác động (tbl_orders, tbl_payments...) |
| `entity_id` | `UUID` | NO | - | Khóa chính của thực thể bị tác động |
| `action` | `VARCHAR(30)` | NO | - | Hành động: `CREATE`, `UPDATE`, `DELETE`, `STATUS_CHANGE` |
| `changed_data` | `JSONB` | YES | - | Dữ liệu sai khác trước và sau thay đổi |
| `performed_by` | `VARCHAR(100)`| NO | - | Định danh người dùng hoặc hệ thống thực hiện |
| `created_at` | `TIMESTAMPTZ` | NO | `DEFAULT CURRENT_TIMESTAMP` | Thời điểm ghi nhận hành động kiểm toán |
