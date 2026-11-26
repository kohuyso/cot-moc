# Requirement Analysis & Specification: Cột Mốc MVP (Phase 1)

## Metadata
- **Run ID**: `cot-moc-mvp`
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`
- **Status**: `DRAFT`
- **Intake Reference**: `artifacts/intake.md`
- **Source Document**: `docs/URD.md` (REQ-001 to REQ-012; REQ-013 to REQ-018 excluded as Phase 2)
- **Standard Conformance**: `ISO/IEC/IEEE 29148:2018 & IIBA BABOK v3`

---

## 1. Executive Summary & Business Objective

### 1.1 Business Need & Value Proposition
- **Problem Statement**: Người đi phượt thường xuyên di chuyển qua khu vực đèo núi, vùng sâu vùng xa nơi sóng di động chập chờn hoặc mất hoàn toàn. Khi xảy ra sự cố (tai nạn, hỏng xe, lạc đường), việc gửi tín hiệu cầu cứu kèm tọa độ chính xác và thông tin y tế gặp nhiều trở ngại; đồng thời người dùng cũng thiếu công cụ ghi lại nhật ký hành trình hoạt động ổn định khi offline.
- **Business Objective**: Xây dựng phiên bản Phase 1 MVP của ứng dụng **Cột Mốc (`cot-moc`)** gồm Mobile App (React Native, TypeScript, offline-first) và Backend + Web Tracking (FastAPI, Python), giải quyết trọn vẹn 3 trụ cột: (1) Tài khoản & Hồ sơ khẩn cấp, (2) An toàn & Cảnh báo khẩn cấp (Core SOS + Web Tracking + Dead Man's Switch), và (3) Nhật ký hành trình & Chia sẻ.
- **Value Proposition & Measurable Targets**:
  - Thời gian kích hoạt SOS và mở SMS Fallback khi mất sóng < 1,000 ms sau khi kết thúc đếm ngược 5 giây.
  - Độ trễ API đồng bộ và Web Tracking p95 < 300 ms.
  - Đảm bảo 0% mất mát dữ liệu chuyến đi và check-in khi mất mạng nhờ hàng đợi SQLite offline-first và đồng bộ idempotent.

### 1.2 Stakeholder Analysis & RACI Matrix
| Stakeholder Persona | Role | Responsibility | RACI |
|---|---|---|---|
| **Product Owner / User** | Chủ sở hữu sản phẩm | Phê duyệt phạm vi MVP, xác nhận câu hỏi mở và giả định | **A** (Accountable) |
| **Business Analyst (BA)** | `sdlc-ba-analysis` | Phân tích nghiệp vụ, viết SRS/FSD/Data Dictionary/RTM | **R** (Responsible) |
| **Solution Architect (SA)** | `sdlc-sa-review` / `sdlc-sa-design` | Thẩm định SRS và thiết kế kiến trúc hệ thống | **C** (Consulted) |
| **Lead Implementer (Dev)** | `sdlc-implementer` | Triển khai Mobile App (React Native) và Backend (FastAPI) | **C** (Consulted) |
| **QA Engineer / Lead** | `sdlc-test-design` / `sdlc-qa-review` | Thiết kế kiểm thử, thực thi và nghiệm thu chất lượng | **C** (Consulted) |
| **Security Reviewer** | `sdlc-security-review` | Đánh giá bảo mật JWT, tracking token, quyền riêng tư vị trí | **I** (Informed) |

---

## 2. Current State (AS-IS) vs Target State (TO-BE)

### 2.1 Current State (AS-IS)
Dự án đang ở trạng thái khởi tạo mới (`new_build`). Hiện tại chưa có mã nguồn `backend/` hay `mobile/`, mới chỉ có tài liệu yêu cầu người dùng `docs/URD.md` và cấu hình `.harness.yaml`.

### 2.2 Target State (TO-BE)
Hệ thống hoàn chỉnh gồm 2 thành phần chính:
1. **Mobile App (`mobile/`)**: Ứng dụng React Native (TypeScript) lưu trữ cục bộ bằng SQLite + SecureStore, hoạt động đầy đủ khi mất sóng cho SOS SMS Fallback, ghi vết hành trình nền, check-in ảnh gắn watermark và xuất poster tổng kết.
2. **Backend & Web Tracking (`backend/`)**: Dịch vụ FastAPI (Python) cung cấp REST API xác thực JWT, đồng bộ chuyến đi/check-in/breadcrumb idempotent, phát cảnh báo đa kênh, chạy tác vụ hẹn giờ Dead Man's Switch và phục vụ trang web theo dõi trực tiếp công khai theo `tracking_token` tạm thời.

---

## 3. Scope Boundaries & System Context

### 3.1 In-Scope Deliverables (Phase 1 MVP)
- **Module 1 — Tài khoản & Hồ sơ khẩn cấp (`auth_profile`)**: `REQ-001`, `REQ-002`, `REQ-003` (`FR-001`..`FR-004`).
- **Module 2 — An toàn & Cảnh báo khẩn cấp (`sos_safety`)**: `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008` (`FR-005`..`FR-009`).
- **Module 3 — Nhật ký hành trình & Chia sẻ (`trip_journal`)**: `REQ-009`, `REQ-010`, `REQ-011`, `REQ-012` (`FR-010`..`FR-013`).

### 3.2 Out-of-Scope & Non-Goals (Phase 2 — Đã được người dùng xác nhận loại trừ)
- `OOS-001` (`REQ-013`): Tải gói bản đồ và dữ liệu cứu hộ Offline theo cung đường.
- `OOS-002` (`REQ-014`): Danh bạ cứu hộ & sửa xe dọc tuyến Offline kèm xác nhận cộng đồng.
- `OOS-003` (`REQ-015`): Bản đồ cây xăng & điểm nghỉ với cảnh báo đoạn đường dài không có cây xăng.
- `OOS-004` (`REQ-016`): Tự động tô màu tỉnh thành Offline theo ranh giới hành chính.
- `OOS-005` (`REQ-017`): Bản đồ kỷ niệm theo tỉnh thành.
- `OOS-006` (`REQ-018`): Profile thống kê thành tích (`x/63` tỉnh, độ cao cao nhất, tổng ngày).

---

## 4. Domain Glossary & Ubiquitous Language

| Term | Business Definition | Technical Representation | Invariant / Boundary |
|---|---|---|---|
| **Emergency Contact** | Người thân nhận cảnh báo khi có SOS hoặc quá hạn check-in | Entity `EmergencyContact` (`tbl_emergency_contacts`) | Tối đa 5 liên hệ / tài khoản |
| **Emergency Card** | Thẻ thông tin y tế (nhóm máu, dị ứng, bệnh nền) và thông tin xe | Entity `EmergencyCard` (`tbl_emergency_cards`) | 1 thẻ / tài khoản |
| **SOS Session** | Phiên cầu cứu khẩn cấp được kích hoạt thủ công hoặc qua Dead Man's Switch | Entity `SosSession` (`tbl_sos_sessions`) | Trạng thái: `ACTIVE`, `RESOLVED`, `CANCELLED` |
| **Tracking Token** | Mã phiên tạm thời gắn vào URL công khai cho người thân xem vị trí | `tracking_token` (32-byte URL-safe string) | Hết hạn 24h sau khi kết thúc hoặc thu hồi tức thì |
| **Safety Timer** | Bộ đếm hẹn giờ check-in an toàn (Dead Man's Switch) | Entity `SafetyTimer` (`tbl_safety_timers`) | Trạng thái: `ARMED`, `CHECKED_IN`, `EXPIRED_ALERTED`, `CANCELLED` |
| **Breadcrumb** | Điểm tọa độ GPS ghi nhận theo chu kỳ trong chuyến đi | Entity `TripBreadcrumb` (`tbl_trip_breadcrumbs`) | Bỏ qua điểm có `accuracy > 100m` |
| **Trip** | Chuyến đi phượt do người dùng bắt đầu, tạm dừng và kết thúc | Entity `Trip` (`tbl_trips`) | Tối đa 1 chuyến `ACTIVE` hoặc `PAUSED` tại 1 thời điểm |
| **Check-in** | Ảnh chụp gắn watermark + ghi chú tại một tọa độ GPS trong chuyến đi | Entity `TripCheckin` (`tbl_trip_checkins`) | Ghi chú <= 500 ký tự; ảnh <= 10 MB |

---

## 5. Functional Requirements Specification

### Module 1: Tài khoản & Hồ sơ khẩn cấp (`auth_profile`)

#### FR-001: Đăng ký tài khoản người dùng bằng SĐT hoặc Email
- **Sources**: `REQ-001`
- **Actors**: Khách (chưa đăng nhập)
- **Preconditions**: Thiết bị có kết nối mạng; người dùng đang ở màn hình Đăng ký.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng mới đăng ký tài khoản bằng số điện thoại hoặc email kết hợp mật khẩu, kiểm tra tính duy nhất và lưu phiên đăng nhập an toàn.
- **Main Flow**:
  1. Người dùng nhập SĐT (định dạng `+84` hoặc `0xxxxxxxxx`) hoặc Email, mật khẩu (`>= 8` ký tự) và họ tên trên màn hình Đăng ký.
  2. Ứng dụng kiểm tra định dạng đầu vào cục bộ và gửi `POST /api/v1/auth/register` tới FastAPI backend.
  3. Backend băm mật khẩu bằng bcrypt/argon2, tạo bản ghi tài khoản mới, sinh cặp JWT `access_token` (TTL 15 phút) và `refresh_token` (TTL 30 ngày).
  4. Ứng dụng lưu token vào `SecureStore` trên thiết bị và chuyển hướng vào màn hình chính.
- **Alternate Flows**:
  - Đăng ký bằng Email: Hệ thống chuẩn hóa email về chữ thường và bỏ qua bước chuẩn hóa mã vùng `+84`.
- **Exception Flows**:
  - SĐT hoặc Email đã tồn tại: Backend trả `HTTP 409 Conflict` (`ERR_AUTH_DUPLICATE_IDENTIFIER`); ứng dụng hiển thị thông báo lỗi.
  - Mật khẩu dưới 8 ký tự hoặc thiếu chữ/số: Trả `HTTP 422` (`ERR_AUTH_WEAK_PASSWORD`).
  - Mất mạng khi đăng ký: Ứng dụng báo `ERR_NETWORK_OFFLINE`.
- **Data Attributes**: `phone` (String, E.164, optional nếu có email), `email` (String, max 255, optional nếu có phone), `password` (String, min 8, max 128, required), `full_name` (String, 1..100, required).
- **Business Rule `BR-001`**: Mỗi tài khoản bắt buộc có ít nhất 1 định danh (`phone` hoặc `email`) duy nhất. SĐT Việt Nam bắt đầu bằng `0` (10 số) được chuẩn hóa sang `+84`. Ví dụ: `'0912345678'` -> `'+84912345678'`; mật khẩu `'abc'` (3 ký tự) bị từ chối vì `< 8` ký tự.
- **Acceptance Criteria**:
  - **Given** người dùng chưa có tài khoản nhập SĐT `'0912345678'` và mật khẩu `'MatKhau123'`
    **When** bấm Đăng ký
    **Then** Backend trả `HTTP 201 Created`, lưu SĐT `'+84912345678'`, trả `access_token` và `refresh_token`, ứng dụng lưu vào `SecureStore`.
  - **Given** SĐT `'+84912345678'` đã tồn tại
    **When** gửi yêu cầu đăng ký với `'0912345678'`
    **Then** Backend trả `HTTP 409 Conflict` với mã `ERR_AUTH_DUPLICATE_IDENTIFIER`.
- **NFR Links**: `NFR-002`.

#### FR-002: Đăng nhập và duy trì phiên ngoại tuyến an toàn
- **Sources**: `REQ-001`
- **Actors**: Người dùng đã đăng ký
- **Preconditions**: Tài khoản đã tồn tại (khi đăng nhập online) hoặc đã có phiên hợp lệ trong `SecureStore` (khi mở app offline).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng đăng nhập bằng SĐT hoặc Email và mật khẩu, lưu phiên an toàn trên thiết bị để sử dụng được cả khi mất sóng.
- **Main Flow**:
  1. Người dùng nhập định danh (SĐT hoặc Email) và mật khẩu trên màn hình Đăng nhập.
  2. Ứng dụng gửi `POST /api/v1/auth/login` tới FastAPI backend.
  3. Backend xác thực mật khẩu băm, cấp `access_token` và `refresh_token` mới.
  4. Ứng dụng lưu token vào `SecureStore`, đồng bộ hồ sơ cá nhân về SQLite cục bộ.
- **Alternate Flows**:
  - Mở app khi offline nhưng đã có `refresh_token` hợp lệ trong `SecureStore`: Vào thẳng màn hình chính ở chế độ Offline.
  - `access_token` hết hạn khi có mạng: Tự động gọi `POST /api/v1/auth/refresh`.
- **Exception Flows**:
  - Sai mật khẩu hoặc không tìm thấy tài khoản: `HTTP 401 Unauthorized` (`ERR_AUTH_INVALID_CREDENTIALS`).
  - `refresh_token` hết hạn/thu hồi: `HTTP 401` (`ERR_AUTH_SESSION_EXPIRED`), xóa token cục bộ và đưa về màn hình Đăng nhập.
- **Data Attributes**: `identifier` (String, required), `password` (String, required), `access_token` (JWT, TTL 900s), `refresh_token` (JWT/Opaque, TTL 30d).
- **Business Rule `BR-002`**: Phiên đăng nhập hợp lệ khi offline nếu `SecureStore` còn `refresh_token` chưa quá 30 ngày. Ví dụ: đăng nhập `2026-11-01`, mở app offline `2026-11-20` (19 ngày <= 30 ngày) -> cho phép vào app.
- **Acceptance Criteria**:
  - **Given** tài khoản `'+84912345678'` tồn tại với mật khẩu `'MatKhau123'`
    **When** đăng nhập đúng thông tin
    **Then** Backend trả `HTTP 200 OK` kèm `access_token` và `refresh_token`; ứng dụng lưu vào `SecureStore`.
  - **Given** người dùng nhập sai mật khẩu `'SaiMatKhau'`
    **When** bấm Đăng nhập
    **Then** Backend trả `HTTP 401 Unauthorized` với mã `ERR_AUTH_INVALID_CREDENTIALS`.
- **NFR Links**: `NFR-002`.

#### FR-003: Quản lý danh bạ người thân khẩn cấp (tối đa 5 liên hệ)
- **Sources**: `REQ-002`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã có phiên đăng nhập hợp lệ.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng thêm, sửa, xóa và xem tối đa 5 liên hệ khẩn cấp gồm Tên, SĐT và Mối quan hệ, đồng bộ cả cục bộ và server.
- **Main Flow**:
  1. Người dùng mở màn hình Danh bạ khẩn cấp và chọn Thêm liên hệ.
  2. Người dùng nhập Tên (1..100 ký tự), SĐT hợp lệ và Mối quan hệ (1..50 ký tự).
  3. Ứng dụng lưu bản ghi vào SQLite cục bộ ngay lập tức và đồng bộ lên `POST /api/v1/contacts` (hoặc xếp hàng nếu offline).
  4. Backend kiểm tra giới hạn `<= 5` liên hệ và trả `HTTP 201 Created`.
- **Alternate Flows**:
  - Sửa/Xóa liên hệ: `PUT /api/v1/contacts/{id}` hoặc `DELETE /api/v1/contacts/{id}`.
  - Thao tác khi offline: Lưu cục bộ với `sync_status = PENDING`, tự đồng bộ khi có mạng.
- **Exception Flows**:
  - Thêm liên hệ thứ 6 khi đã đủ 5: `HTTP 400 Bad Request` (`ERR_CONTACT_LIMIT_EXCEEDED`).
  - SĐT sai định dạng: `HTTP 422` (`ERR_CONTACT_INVALID_PHONE`).
- **Data Attributes**: `name` (String, 1..100, required), `phone` (String, 10..15 digits, required), `relationship` (String, 1..50, required).
- **Business Rule `BR-003`**: `0 <= count(active_contacts) <= 5` trên mỗi tài khoản. Ví dụ: đang có 5 liên hệ, thêm liên hệ thứ 6 -> bị chặn với `ERR_CONTACT_LIMIT_EXCEEDED`.
- **Acceptance Criteria**:
  - **Given** người dùng đang có 4 liên hệ khẩn cấp
    **When** thêm liên hệ thứ 5 (`'Nguyễn Văn A'`, `'0987654321'`, `'Anh trai'`)
    **Then** lưu thành công (`HTTP 201`), tổng số liên hệ là 5.
  - **Given** người dùng đã có đủ 5 liên hệ
    **When** cố gắng thêm liên hệ thứ 6
    **Then** từ chối với `HTTP 400` và mã `ERR_CONTACT_LIMIT_EXCEEDED`.
- **NFR Links**: `NFR-003`.

#### FR-004: Quản lý thẻ thông tin y tế và phương tiện cá nhân
- **Sources**: `REQ-003`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã có phiên đăng nhập hợp lệ.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng lưu và cập nhật thẻ thông tin y tế (nhóm máu, dị ứng thuốc, bệnh nền) và thông tin xe (biển số, loại xe) để tự động đính kèm khi phát SOS.
- **Main Flow**:
  1. Người dùng mở màn hình Thẻ Y tế & Xe.
  2. Chọn nhóm máu, nhập dị ứng thuốc, bệnh nền, biển số xe và loại xe.
  3. Bấm Lưu: ứng dụng lưu SQLite cục bộ và gửi `PUT /api/v1/profile/emergency-card`.
  4. Backend xác thực và trả `HTTP 200 OK`.
- **Alternate Flows**:
  - Cập nhật khi offline: Lưu SQLite cục bộ với `sync_status = PENDING` để sẵn sàng đính kèm SMS SOS.
- **Exception Flows**:
  - Nhóm máu ngoài tập cho phép: `HTTP 422` (`ERR_PROFILE_INVALID_BLOOD_TYPE`).
  - Dị ứng/bệnh nền vượt 500 ký tự: `HTTP 422` (`ERR_PROFILE_FIELD_TOO_LONG`).
- **Data Attributes**: `blood_type` (Enum: `A+|A-|B+|B-|AB+|AB-|O+|O-|UNKNOWN`, default `UNKNOWN`), `drug_allergies` (String, max 500, optional), `medical_conditions` (String, max 500, optional), `vehicle_plate` (String, max 20, optional), `vehicle_model` (String, max 100, optional).
- **Business Rule `BR-004`**: `blood_type` thuộc tập `{A+, A-, B+, B-, AB+, AB-, O+, O-, UNKNOWN}`. Ví dụ: `blood_type='O+'`, `vehicle_plate='29A1-12345'` -> hợp lệ.
- **Acceptance Criteria**:
  - **Given** người dùng đã đăng nhập
    **When** cập nhật `blood_type='O+'`, `drug_allergies='Penicillin'`, `vehicle_plate='29A1-12345'`, `vehicle_model='Honda Winner X'`
    **Then** lưu thành công (`HTTP 200 OK`) cả ở server và SQLite cục bộ.
  - **Given** người dùng gửi `blood_type='XYZ'`
    **When** gọi `PUT /api/v1/profile/emergency-card`
    **Then** Backend trả `HTTP 422` với mã `ERR_PROFILE_INVALID_BLOOD_TYPE`.
- **NFR Links**: `NFR-003`.

---

### Module 2: An toàn & Cảnh báo khẩn cấp (`sos_safety`)

#### FR-005: Kích hoạt nút SOS khẩn cấp 1 chạm (giữ 3s + đếm ngược hủy 5s)
- **Sources**: `REQ-004`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đang ở màn hình chính (`SCR-SOS-01`).
- **Requirement Statement**: Hệ thống SHALL cung cấp nút SOS nổi bật trên màn hình chính yêu cầu bấm giữ liên tục 3 giây để kích hoạt, sau đó mở cửa sổ đếm ngược 5 giây cho phép hủy trước khi phát cảnh báo.
- **Main Flow**:
  1. Người dùng bấm và giữ nút SOS liên tục đủ 3.0 giây.
  2. Ứng dụng rung phản hồi (haptic), chuyển sang màn hình đếm ngược 5 giây (`5 -> 0`) kèm nút `'HỦY SOS'`.
  3. Hết 5 giây không bấm hủy -> chuyển trạng thái SOS sang `ACTIVE` và gọi luồng `FR-006`.
- **Alternate Flows**:
  - Nhả tay trước 3.0 giây: Đặt lại tiến trình về 0.
  - Bấm `'HỦY SOS'` trong 5 giây: Hủy kích hoạt, ghi log `SOS_CANCELLED_IN_COUNTDOWN`, quay về `IDLE`.
- **Exception Flows**:
  - GPS chưa khóa được tọa độ mới: Dùng tọa độ GPS cuối cùng đã lưu kèm cờ `is_stale_location = true`.
  - Chưa có liên hệ khẩn cấp: Vẫn gửi SOS lên server (tạo link web) và cảnh báo người dùng.
- **Business Rule `BR-005`**: `hold_duration >= 3000 ms`; `cancel_window = 5000 ms`. Ví dụ: giữ 2500 ms rồi thả -> không kích hoạt; giữ 3000 ms -> đếm ngược 5s; bấm Hủy ở giây thứ 3 -> hủy hoàn toàn.
- **Acceptance Criteria**:
  - **Given** người dùng ở màn hình chính
    **When** giữ nút SOS đủ 3 giây và không bấm Hủy trong 5 giây
    **Then** trạng thái SOS chuyển `ACTIVE` và kích hoạt `FR-006`.
  - **Given** màn hình đang đếm ngược SOS ở giây thứ 2
    **When** người dùng bấm `'HỦY SOS'`
    **Then** đếm ngược dừng, trạng thái về `IDLE` và không phát cảnh báo.
- **NFR Links**: `NFR-001`.

#### FR-006: Phát cảnh báo SOS đa kênh Online và SMS Fallback khi Offline
- **Sources**: `REQ-005`
- **Actors**: Hệ thống Mobile App, FastAPI Backend, Người thân khẩn cấp
- **Preconditions**: SOS vừa chuyển sang trạng thái `ACTIVE`.
- **Requirement Statement**: Hệ thống SHALL gửi tín hiệu SOS kèm tọa độ GPS, % pin và thông tin y tế lên FastAPI backend khi có mạng, hoặc tự động mở trình soạn SMS chứa link Google Maps và thông tin khẩn cấp khi mất mạng.
- **Main Flow**:
  1. Ứng dụng thu thập GPS (`lat`, `lng`, `accuracy`), `battery_level`, `recorded_at`, và `EmergencyCard` từ SQLite.
  2. Nếu có mạng: gọi `POST /api/v1/sos/trigger` (timeout 5000 ms).
  3. Backend tạo `SosSession` với `tracking_token`, lưu sự kiện SOS, gọi Notification Adapter gửi thông báo tới danh bạ khẩn cấp kèm `tracking_url`.
  4. Trả `HTTP 201 Created` gồm `sos_id` và `tracking_url`.
- **Alternate Flows**:
  - Offline hoặc API timeout `> 5000 ms`: Tự động mở OS SMS Composer điền sẵn danh sách SĐT người thân và nội dung `[COT MOC SOS] Toi dang can ho tro! Vi tri: https://maps.google.com/?q=<lat>,<lng> | Pin: <battery>% | Nhom mau: <blood> | Di ung: <allergy> | Bien so: <plate>`.
- **Exception Flows**:
  - Notification Adapter lỗi: Backend vẫn trả `HTTP 201` với `delivery_status = PARTIAL_FAILED` và retry nền tối đa 3 lần.
  - Không có liên hệ khẩn cấp khi Offline: Hiển thị `ERR_SOS_NO_CONTACTS_OFFLINE` và gợi ý gọi 113/115.
- **Business Rule `BR-006`**: Timeout online `= 5000 ms` trước khi fallback SMS. Tọa độ định dạng 6 chữ số thập phân. Ví dụ: `lat=21.028511, lng=105.804817, battery=18%` -> `https://maps.google.com/?q=21.028511,105.804817 | Pin: 18%`.
- **Acceptance Criteria**:
  - **Given** thiết bị online, pin 42%, tọa độ `(21.028511, 105.804817)`, có 2 liên hệ khẩn cấp
    **When** SOS kích hoạt
    **Then** `POST /api/v1/sos/trigger` trả `HTTP 201`, sinh `tracking_url` và gọi Notification Adapter gửi cảnh báo tới 2 liên hệ.
  - **Given** thiết bị offline, pin 15%, có liên hệ `'0987654321'`
    **When** SOS kích hoạt
    **Then** tự động mở OS SMS Composer với người nhận `'0987654321'`, link Google Maps, `'Pin: 15%'` và thông tin y tế.
- **NFR Links**: `NFR-001`.

#### FR-007: Trang Web theo dõi trực tiếp cho người thân qua Token tạm thời
- **Sources**: `REQ-006`
- **Actors**: Người thân (không cần đăng nhập/cài app), Chủ tài khoản
- **Preconditions**: Có `SosSession` hoặc phiên chia sẻ hành trình với `tracking_token` hợp lệ.
- **Requirement Statement**: FastAPI backend SHALL cung cấp một trang web công khai theo mã phiên token tạm thời hiển thị vị trí cuối cùng, trạng thái SOS, mức pin và vệt di chuyển gần nhất mà người thân không cần cài app.
- **Main Flow**:
  1. Người thân mở `GET /track/{tracking_token}` trên trình duyệt.
  2. FastAPI kiểm tra tính hợp lệ và hạn dùng của `tracking_token`.
  3. Trả về trang HTML nhẹ hiển thị vị trí cuối cùng, trạng thái SOS (`ACTIVE`/`RESOLVED`), `% pin`, thời điểm cập nhật cuối, thông tin y tế/xe (khi SOS) và tối đa 50 điểm breadcrumb gần nhất.
  4. Trang tự làm mới qua `GET /api/v1/track/{tracking_token}/status` mỗi 15 giây.
- **Alternate Flows**:
  - Chủ tài khoản kết thúc SOS hoặc thu hồi link: Trạng thái chuyển `RESOLVED`, `expires_at = ended_at + 24h` (hoặc hết hạn ngay nếu thu hồi).
- **Exception Flows**:
  - Token không tồn tại, đã thu hồi hoặc quá hạn 24h: Trả `HTTP 410 Gone` (`ERR_TRACK_TOKEN_EXPIRED`).
- **Business Rule `BR-007`**: `tracking_token` là chuỗi ngẫu nhiên 32 byte URL-safe; `expires_at = ended_at + 24h`. Ví dụ: SOS kết thúc `2026-11-25 18:00` -> hết hạn `2026-11-26 18:00`.
- **Acceptance Criteria**:
  - **Given** phiên SOS `ACTIVE` với `tracking_token` hợp lệ, tọa độ `(21.028511, 105.804817)`, pin 35%
    **When** truy cập `GET /track/{tracking_token}`
    **Then** trả `HTTP 200 OK` với HTML hiển thị trạng thái `ACTIVE`, tọa độ, pin `35%` và vệt di chuyển.
  - **Given** `tracking_token` đã quá hạn 24h hoặc bị thu hồi
    **When** truy cập `GET /track/{tracking_token}`
    **Then** trả `HTTP 410 Gone` (`ERR_TRACK_TOKEN_EXPIRED`).
- **NFR Links**: `NFR-001`, `NFR-002`.

#### FR-008: Hẹn giờ Check-in an toàn (Dead Man's Switch)
- **Sources**: `REQ-007`
- **Actors**: Người dùng đã đăng nhập, Scheduler nền trên FastAPI
- **Preconditions**: Người dùng đã thiết lập ít nhất 1 liên hệ khẩn cấp (hoặc có tọa độ GPS gần nhất).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng đặt mốc thời gian dự kiến an toàn và tự động phát cảnh báo kèm tọa độ cuối cùng cho người thân nếu quá hạn mà người dùng không xác nhận 'Tôi an toàn'.
- **Main Flow**:
  1. Người dùng đặt `deadline_at` (`>= now + 5 phút`) và bấm Bắt đầu đếm giờ.
  2. Ứng dụng gửi `POST /api/v1/safety-timers` (trạng thái `ARMED`).
  3. Trước hạn 10 phút, ứng dụng nhắc người dùng bấm `'Tôi an toàn'` hoặc gia hạn.
  4. Quá `deadline_at` mà chưa có check-in: Tác vụ nền server chuyển timer sang `EXPIRED_ALERTED` và phát cảnh báo SOS kèm tọa độ cuối cùng tới người thân.
- **Alternate Flows**:
  - Bấm `'Tôi an toàn'` trước hạn: `POST /api/v1/safety-timers/{id}/checkin` -> `CHECKED_IN`.
  - Gia hạn thêm 30/60 phút trước hạn: Cập nhật `deadline_at`.
- **Exception Flows**:
  - `deadline_at` ở quá khứ hoặc `< now + 5m`: `HTTP 422` (`ERR_TIMER_INVALID_DEADLINE`).
- **Business Rule `BR-008`**: `now + 5m <= deadline_at <= now + 72h`. Ví dụ: hiện tại 14:00, đặt 18:00 (240 phút) -> hợp lệ; đặt 13:55 -> từ chối `ERR_TIMER_INVALID_DEADLINE`.
- **Acceptance Criteria**:
  - **Given** safety timer đặt deadline `18:00` với tọa độ cuối `(21.1, 105.8)`
    **When** đồng hồ server vượt `18:00` mà chưa check-in
    **Then** server chuyển `EXPIRED_ALERTED` và phát cảnh báo kèm tọa độ `(21.1, 105.8)`.
  - **Given** safety timer deadline `18:00`
    **When** người dùng bấm `'Tôi an toàn'` lúc `17:45`
    **Then** `HTTP 200 OK`, chuyển `CHECKED_IN` và không phát cảnh báo lúc `18:00`.
- **NFR Links**: `NFR-002`.

#### FR-009: Lưu vết hành trình nền tối ưu pin (Breadcrumb Trail)
- **Sources**: `REQ-008`
- **Actors**: Dịch vụ nền Mobile App, FastAPI Backend
- **Preconditions**: Có một chuyến đi ở trạng thái `ACTIVE`.
- **Requirement Statement**: Hệ thống SHALL ghi nhận tọa độ GPS theo chu kỳ tối ưu pin khi chuyến đi đang chạy, lưu cục bộ trên thiết bị và đồng bộ theo lô lên server khi có mạng.
- **Main Flow**:
  1. Khi chuyến đi `ACTIVE`, dịch vụ nền thu thập GPS (`lat`, `lng`, `altitude`, `speed`, `battery_level`, `recorded_at`).
  2. Điều chỉnh tần suất: 15s khi `speed >= 2 km/h`; 120s khi `speed < 2 km/h`.
  3. Lưu điểm hợp lệ vào SQLite với `synced = false`.
  4. Khi có mạng và đủ lô 10 điểm (hoặc mỗi 60s), gửi `POST /api/v1/trips/{trip_id}/breadcrumbs` và đánh dấu `synced = true`.
- **Alternate Flows**:
  - Mất mạng kéo dài: Lưu toàn bộ trong SQLite và đồng bộ bù theo thứ tự thời gian khi có mạng.
- **Exception Flows**:
  - Điểm GPS có `accuracy > 100m`: Loại bỏ điểm nhiễu.
  - Lỗi mạng/5xx khi đồng bộ: Giữ `synced = false` để thử lại.
- **Business Rule `BR-009`**: Chu kỳ = `15s` nếu `speed >= 2.0 km/h`, `120s` nếu `speed < 2.0 km/h`; lọc bỏ `accuracy > 100m`. Ví dụ: `speed = 45 km/h, accuracy = 12m` -> ghi mỗi 15s; `accuracy = 250m` -> bỏ qua.
- **Acceptance Criteria**:
  - **Given** chuyến đi `ACTIVE` đang offline
    **When** ghi nhận 3 điểm GPS hợp lệ (`accuracy = 10m`) rồi có mạng trở lại
    **Then** 3 điểm lưu SQLite trước và tự đồng bộ lên `POST /api/v1/trips/{trip_id}/breadcrumbs` (`HTTP 200 OK`).
  - **Given** điểm GPS có `accuracy = 250m`
    **When** bộ lọc xử lý
    **Then** điểm bị loại bỏ, không lưu vào SQLite.
- **NFR Links**: `NFR-003`.

---

### Module 3: Nhật ký hành trình & Chia sẻ (`trip_journal`)

#### FR-010: Quản lý vòng đời chuyến đi và lịch sử (Bắt đầu / Tạm dừng / Kết thúc)
- **Sources**: `REQ-009`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã đăng nhập (online hoặc offline).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng Bắt đầu, Tạm dừng, Tiếp tục và Kết thúc chuyến đi, tự động tính tổng quãng đường (km) và thời gian di chuyển để xem lại trong lịch sử.
- **Main Flow**:
  1. Người dùng nhập tên chuyến đi (tùy chọn) và bấm `'Bắt đầu chuyến đi'`.
  2. Ứng dụng tạo chuyến đi `ACTIVE` trong SQLite và đồng bộ `POST /api/v1/trips`.
  3. Người dùng có thể bấm `'Tạm dừng'` (`ACTIVE -> PAUSED`) hoặc `'Tiếp tục'` (`PAUSED -> ACTIVE`).
  4. Bấm `'Kết thúc chuyến đi'` -> chuyển `COMPLETED`, tính tổng `distance_km` (Haversine) và `duration_seconds` (không tính thời gian `PAUSED`).
- **Alternate Flows**:
  - Xem lịch sử: Tab Nhật ký hiển thị danh sách chuyến đi đã hoàn thành kèm tên, ngày, `distance_km` và thời gian.
- **Exception Flows**:
  - Tạo chuyến đi mới khi đang có chuyến `ACTIVE` hoặc `PAUSED`: Chặn với mã `ERR_TRIP_ALREADY_ACTIVE`.
- **Business Rule `BR-010`**: Tối đa 1 chuyến `ACTIVE`/`PAUSED` mỗi người dùng tại 1 thời điểm. `distance_km` tính bằng tổng Haversine các cặp breadcrumb liên tiếp (làm tròn 2 chữ số thập phân). Ví dụ: `(21.000, 105.800)` -> `(21.009, 105.800)` ~ `1.00 km`.
- **Acceptance Criteria**:
  - **Given** không có chuyến đi nào đang chạy
    **When** Bắt đầu -> Tạm dừng -> Tiếp tục -> Kết thúc
    **Then** trạng thái chuyển `ACTIVE -> PAUSED -> ACTIVE -> COMPLETED` và tính đúng `distance_km` + `duration_seconds`.
  - **Given** đang có chuyến `T-001` ở trạng thái `ACTIVE`
    **When** cố gắng tạo chuyến đi mới `T-002`
    **Then** từ chối với mã `ERR_TRIP_ALREADY_ACTIVE`.
- **NFR Links**: `NFR-003`.

#### FR-011: Check-in ảnh & ghi chú gắn tọa độ GPS với hàng đợi Offline
- **Sources**: `REQ-010`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đang có chuyến đi ở trạng thái `ACTIVE` hoặc `PAUSED`.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng chụp/chọn ảnh và nhập ghi chú gắn đúng tọa độ GPS hiện tại trong chuyến đi, lưu hàng đợi cục bộ khi mất sóng và tự đồng bộ khi có mạng.
- **Main Flow**:
  1. Người dùng bấm Check-in, chụp/chọn ảnh và nhập ghi chú (`<= 500` ký tự).
  2. Ứng dụng gắn GPS hiện tại (`lat`, `lng`, `altitude_m`) và thời gian chụp.
  3. Lưu ảnh đã gắn watermark (`FR-012`) và metadata vào SQLite với `sync_status = PENDING`.
  4. Khi có mạng, worker tải lên `POST /api/v1/trips/{trip_id}/checkins` và cập nhật `sync_status = SYNCED`.
- **Alternate Flows**:
  - Check-in khi offline: Hiển thị ngay trên bản đồ/danh sách với huy hiệu `'Chờ đồng bộ'`, tự upload khi có mạng.
- **Exception Flows**:
  - Ảnh sai định dạng (không phải JPEG/PNG) hoặc vượt 10 MB sau nén: Trả `ERR_CHECKIN_INVALID_IMAGE`.
  - Ghi chú > 500 ký tự: Trả `ERR_CHECKIN_NOTE_TOO_LONG`.
  - Upload lỗi mạng: Retry với backoff 5s, 15s, 45s.
- **Business Rule `BR-011`**: Ghi chú `<= 500` ký tự; ảnh tối đa `10 MB` (JPEG/PNG). Ví dụ: ảnh 3.2 MB JPEG + note 120 ký tự -> hợp lệ.
- **Acceptance Criteria**:
  - **Given** chuyến đi `ACTIVE` ở vùng mất sóng
    **When** chụp ảnh check-in với ghi chú `'Đỉnh đèo Mã Pí Lèng'`
    **Then** lưu hàng đợi với `sync_status = PENDING` và tự đồng bộ lên server (`HTTP 201`) khi có mạng.
  - **Given** ghi chú dài 600 ký tự
    **When** bấm lưu Check-in
    **Then** từ chối với mã `ERR_CHECKIN_NOTE_TOO_LONG`.
- **NFR Links**: `NFR-003`.

#### FR-012: Gắn watermark thông số lên ảnh Check-in
- **Sources**: `REQ-011`
- **Actors**: Hệ thống Mobile App
- **Preconditions**: Người dùng vừa chụp/chọn ảnh trong luồng `FR-011`.
- **Requirement Statement**: Hệ thống SHALL tự động gắn lớp phủ watermark lên ảnh check-in gồm Tên địa điểm (hoặc tọa độ GPS), Độ cao (m) và Ngày giờ chụp trước khi lưu và đồng bộ.
- **Main Flow**:
  1. Đọc Tên địa điểm (nếu reverse-geocode thành công) hoặc tọa độ `'lat, lng'`, Độ cao (`m`), và Ngày giờ (`YYYY-MM-DD HH:mm`).
  2. Vẽ dải watermark bán trong suốt ở góc dưới ảnh chứa 3 thông số trên.
  3. Lưu bản ảnh đã gắn watermark làm ảnh check-in chính thức.
- **Alternate Flows**:
  - Offline không reverse-geocode được: Hiển thị tọa độ `'21.028511, 105.804817'`.
  - `altitude` là `null`: Hiển thị `'-- m'`.
- **Exception Flows**:
  - Lỗi render đồ họa: Ghi log `ERR_WATERMARK_RENDER_FAILED` và giữ ảnh gốc kèm metadata văn bản.
- **Business Rule `BR-012`**: Watermark gồm 3 phần: `<Địa điểm | Tọa độ> | <Độ cao> m | <YYYY-MM-DD HH:mm>`. Ví dụ: `'Đèo Ô Quy Hồ | 2000 m | 2026-11-25 10:30'`.
- **Acceptance Criteria**:
  - **Given** chụp ảnh tại `(22.356410, 103.776520)`, độ cao `2000 m`, lúc `2026-11-25 10:30` khi offline
    **When** xử lý ảnh check-in
    **Then** ảnh kết quả có watermark chứa `'22.356410, 103.776520'`, `'2000 m'`, `'2026-11-25 10:30'`.
  - **Given** cảm biến không trả `altitude` (`null`)
    **When** render watermark
    **Then** hiển thị `'-- m'` và không crash.
- **NFR Links**: `NFR-003`.

#### FR-013: Export ảnh tổng kết hành trình (Poster 9:16 hoặc 1:1) có che 1–2 km đầu/cuối
- **Sources**: `REQ-012`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Chuyến đi đã hoàn thành (`COMPLETED`) hoặc có ít nhất 2 ảnh check-in.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng chọn 2–4 ảnh check-in nổi bật, chọn tỷ lệ 9:16 hoặc 1:1 và tùy chọn ẩn 1–2 km đầu/cuối cung đường để xuất ảnh tổng kết lưu về máy hoặc chia sẻ.
- **Main Flow**:
  1. Từ Chi tiết chuyến đi, người dùng bấm `'Xuất ảnh hành trình'`.
  2. Chọn 2–4 ảnh check-in, chọn tỷ lệ `9:16` hoặc `1:1`, chọn mức che đầu/cuối (`0 km`, `1 km`, hoặc `2 km`).
  3. Hệ thống cắt bỏ các điểm breadcrumb trong khoảng `privacy_trim_km` ở đầu và cuối cung đường, vẽ cung đường + lưới ảnh + tổng `km` + thời gian lên poster.
  4. Người dùng lưu về máy hoặc chia sẻ qua OS Share Sheet.
- **Alternate Flows**:
  - Chọn 2, 3, hoặc 4 ảnh: Tự động bố cục lưới tương ứng.
- **Exception Flows**:
  - Chọn `< 2` hoặc `> 4` ảnh: Từ chối với `ERR_EXPORT_INVALID_PHOTO_COUNT`.
  - Tổng quãng đường `< 2 * privacy_trim_km`: Cảnh báo và giới hạn mức che tối đa 25% chiều dài cung đường.
- **Business Rule `BR-013`**: `2 <= selected_photos <= 4`; tỷ lệ `'9:16'` (`1080x1920 px`) hoặc `'1:1'` (`1080x1080 px`); `privacy_trim_km in {0, 1, 2}`. Ví dụ: chuyến 120 km, che 2 km -> vẽ từ km 2 đến km 118.
- **Acceptance Criteria**:
  - **Given** chuyến đi hoàn thành dài `50 km` có 5 ảnh check-in
    **When** chọn 3 ảnh, tỷ lệ `9:16`, che `2 km` đầu/cuối và bấm Xuất
    **Then** tạo ảnh `1080x1920 px` vẽ cung đường đã cắt 2 km đầu/cuối, 3 ảnh check-in, tổng `'50.00 km'` và thời gian di chuyển.
  - **Given** người dùng chỉ chọn 1 ảnh
    **When** bấm Xuất ảnh hành trình
    **Then** từ chối với mã `ERR_EXPORT_INVALID_PHOTO_COUNT`.
- **NFR Links**: `NFR-002`.

---

## 6. Non-Functional Requirements (ISO/IEC 25010)

| NFR ID | Characteristic | Sub-Characteristic | Target Metric / Acceptance Threshold | Verification Method |
|---|---|---|---|---|
| **NFR-001** | Performance | Time Behavior | FastAPI REST API p95 < 300ms; Offline SOS SMS fallback < 1000ms | Load/API timing test & unit timer test |
| **NFR-002** | Security | Confidentiality & Integrity | Password hashed (bcrypt/argon2), JWT in SecureStore, 32-byte tracking token (24h TTL) | Security & auth integration test |
| **NFR-003** | Reliability | Fault Tolerance | Zero data loss offline via SQLite queue; idempotent sync by `client_id` | Offline queue & duplicate-sync test |

---

## 7. Assumptions, Dependencies & Constraints

### 7.1 Assumptions Index (All Confirmed by User)
- **ASM-001**: Đăng ký/đăng nhập dùng SĐT hoặc Email + mật khẩu (`>= 8` ký tự), cấp JWT lưu SecureStore.
- **ASM-002**: Khi Offline phát SOS, app mở OS SMS Composer điền sẵn danh sách SĐT người thân và nội dung chuẩn (hoạt động cả iOS & Android).
- **ASM-003**: `tracking_token` là chuỗi ngẫu nhiên 32-byte URL-safe, hết hạn sau 24 giờ kể từ khi kết thúc SOS/chuyến đi hoặc thu hồi ngay khi chủ tài khoản tắt chia sẻ.

### 7.2 Dependencies & External Interfaces
- **DEP-001**: OS Location / GPS & Battery APIs (React Native).
- **DEP-002**: OS SMS Composer & Share Sheet (React Native).
- **DEP-003**: Notification Adapter (Push/SMS gateway với mock adapter cho dev/test).

### 7.3 Design Constraints
- **CON-001**: Mobile dùng React Native + TypeScript (`npm test`, `npm run typecheck`, `npm run lint`).
- **CON-002**: Backend dùng FastAPI + Python (`pytest`, `python -m compileall .`).

---

## 8. Open Questions & Ambiguities Register

| Question ID | Description | Owner | Status | Resolution |
|---|---|---|---|---|
| **OQ-001** | Cơ chế xác thực cho Đăng ký / Đăng nhập (REQ-001)? | User / PO | `RESOLVED` | Dùng Mật khẩu (SĐT hoặc Email + Password) với JWT lưu SecureStore. |
| **OQ-002** | Hành vi SMS Fallback khi mất mạng (REQ-005) và kênh thông báo Online? | User / PO | `RESOLVED` | Offline mở trình soạn SMS điền sẵn nội dung + SĐT; Online dùng adapter Push/SMS có mock cho dev/test. |
| **OQ-003** | Thời hạn hiệu lực (TTL) của URL theo dõi trực tiếp (REQ-006)? | User / PO | `RESOLVED` | Hết hạn sau 24 giờ kể từ khi kết thúc SOS/chuyến đi, hoặc thu hồi ngay khi tắt chia sẻ. |

---

## 9. Requirements Traceability Matrix (RTM) Anchor
Chi tiết toàn bộ 18 source IDs (`REQ-001`..`REQ-018`) được lập bảng 1-1 tại `artifacts/rtm.md`.
