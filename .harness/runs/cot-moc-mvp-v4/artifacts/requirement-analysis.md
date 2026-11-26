# Requirement Analysis & Specification: Cột Mốc MVP (Phase 1)

## Metadata
- **Run ID**: `cot-moc-mvp-v3`
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`
- **Status**: `SUBMITTED`
- **Intake Reference**: `artifacts/intake.md`
- **Source Document**: `docs/URD.md` (REQ-001 to REQ-012; REQ-013 to REQ-018 excluded as Phase 2)
- **Standard Conformance**: `ISO/IEC/IEEE 29148:2018 & IIBA BABOK v3`

---

## 1. Executive Summary & Business Objective

### 1.1 Business Need & Value Proposition
- **Problem Statement**: Người đi phượt thường xuyên di chuyển qua khu vực đèo núi, vùng sâu vùng xa nơi sóng di động chập chờn hoặc mất hoàn toàn. Khi xảy ra sự cố (tai nạn, hỏng xe, lạc đường), việc gửi tín hiệu cầu cứu kèm tọa độ chính xác và thông tin y tế gặp nhiều trở ngại; đồng thời người dùng cũng thiếu công cụ ghi lại nhật ký hành trình hoạt động ổn định khi offline.
- **Business Objective**: Xây dựng phiên bản Phase 1 MVP của ứng dụng **Cột Mốc (`cot-moc`)** gồm Mobile App (React Native, TypeScript, offline-first) và Backend + Web Tracking (FastAPI, Python), giải quyết trọn vẹn 3 trụ cột: (1) Tài khoản & Hồ sơ khẩn cấp, (2) An toàn & Cảnh báo khẩn cấp (Core SOS + Web Tracking + Dead Man's Switch), và (3) Nhật ký hành trình & Chia sẻ.
- **Value Proposition & Measurable Targets**:
  - Thời gian kích hoạt SOS và mở SMS Fallback khi mất sóng `< 1000 ms` sau khi kết thúc đếm ngược 5 giây.
  - Độ trễ API đồng bộ, `POST /api/v1/sos/trigger` (bất đồng bộ) và Web Tracking `p95 < 300 ms`.
  - Đảm bảo 0% mất mát dữ liệu chuyến đi và check-in khi mất mạng nhờ hàng đợi SQLite offline-first và đồng bộ idempotent theo `(user_id, client_id)`.

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
2. **Backend & Web Tracking (`backend/`)**: Dịch vụ FastAPI (Python) cung cấp REST API xác thực JWT, đồng bộ chuyến đi/check-in/breadcrumb idempotent, phát cảnh báo SMS Gateway bất đồng bộ, chạy tác vụ hẹn giờ Dead Man's Switch và phục vụ trang web theo dõi trực tiếp công khai theo `tracking_token` tạm thời.

---

## 3. Scope Boundaries & System Context

### 3.1 In-Scope Deliverables (Phase 1 MVP)
- **Module 1 — Tài khoản & Hồ sơ khẩn cấp (`auth_profile`)**: `REQ-001`, `REQ-002`, `REQ-003` (`FR-001`..`FR-004`).
- **Module 2 — An toàn & Cảnh báo khẩn cấp (`sos_safety`)**: `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008` (`FR-005`..`FR-009`, `FR-014`).
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
| **Emergency Contact** | Người thân nhận cảnh báo khi có SOS hoặc quá hạn check-in | Entity `EmergencyContact` (`tbl_emergency_contacts`) | Tối đa 5 liên hệ / tài khoản; SĐT chuẩn `+84` |
| **Emergency Card** | Thẻ thông tin y tế (nhóm máu, dị ứng, bệnh nền) và thông tin xe | Entity `EmergencyCard` (`tbl_emergency_cards`) | 1 thẻ / tài khoản |
| **SOS Session** | Phiên cầu cứu khẩn cấp được kích hoạt thủ công hoặc qua Dead Man's Switch | Entity `SosSession` (`tbl_sos_sessions`) | Trạng thái: `ACTIVE`, `RESOLVED`; tối đa 1 `ACTIVE`/user |
| **Tracking Token** | Mã phiên tạm thời gắn vào URL công khai cho người thân xem vị trí | `tracking_token` (32-byte URL-safe string) | Hết hạn 24h sau khi kết thúc hoặc thu hồi tức thì |
| **Safety Timer** | Bộ đếm hẹn giờ check-in an toàn (Dead Man's Switch) | Entity `SafetyTimer` (`tbl_safety_timers`) | Trạng thái: `ARMED`, `CHECKED_IN`, `EXPIRED_ALERTED`, `CANCELLED` |
| **Breadcrumb** | Điểm tọa độ GPS ghi nhận theo chu kỳ trong chuyến đi | Entity `TripBreadcrumb` (`tbl_trip_breadcrumbs`) | Bỏ qua điểm có `accuracy_m > 100` |
| **Trip** | Chuyến đi phượt do người dùng bắt đầu, tạm dừng và kết thúc | Entity `Trip` (`tbl_trips`) | Tối đa 1 chuyến `ACTIVE` hoặc `PAUSED` tại 1 thời điểm |
| **Check-in** | Ảnh chụp gắn watermark + ghi chú tại một tọa độ GPS trong chuyến đi | Entity `TripCheckin` (`tbl_trip_checkins`) | Ghi chú <= 500 ký tự; ảnh sau nén <= 10 MB |

---

## 5. Functional Requirements Specification

### Module 1: Tài khoản & Hồ sơ khẩn cấp (`auth_profile`)

#### FR-001: Đăng ký tài khoản người dùng bằng SĐT hoặc Email
- **Sources**: `REQ-001`
- **Actors**: Khách (chưa đăng nhập)
- **Preconditions**: Thiết bị có kết nối mạng; người dùng đang ở màn hình Đăng ký (`SCR-AUTH-01`).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng mới đăng ký tài khoản bằng số điện thoại hoặc email kết hợp mật khẩu, kiểm tra tính duy nhất và lưu phiên đăng nhập an toàn.
- **Main Flow**:
  1. Người dùng nhập SĐT (định dạng `+84` hoặc `0xxxxxxxxx`) hoặc Email, mật khẩu (`8..128` ký tự, gồm `>= 1` chữ cái và `>= 1` chữ số) và họ tên trên màn hình Đăng ký.
  2. Ứng dụng kiểm tra định dạng đầu vào cục bộ và gửi `POST /api/v1/auth/register` tới FastAPI backend.
  3. Backend băm mật khẩu bằng bcrypt/argon2, tạo bản ghi tài khoản mới, sinh cặp JWT `access_token` (TTL 15 phút) và `refresh_token` (TTL 30 ngày, lưu SHA-256 hash vào `tbl_refresh_tokens`).
  4. Ứng dụng lưu token vào `SecureStore` trên thiết bị và chuyển hướng vào màn hình chính.
- **Alternate Flows**:
  - Đăng ký bằng Email: Hệ thống chuẩn hóa email về chữ thường và bỏ qua bước chuẩn hóa mã vùng `+84`.
- **Exception Flows**:
  - SĐT hoặc Email đã tồn tại: Backend trả `HTTP 409 Conflict` (`ERR_AUTH_DUPLICATE_IDENTIFIER`); trạng thái giữ nguyên chưa đăng nhập.
  - Mật khẩu dưới 8 ký tự hoặc thiếu chữ cái/chữ số: Trả `HTTP 422 Unprocessable Entity` (`ERR_AUTH_WEAK_PASSWORD`) và giữ nguyên form để sửa.
  - Mất mạng khi đăng ký: Ứng dụng báo `ERR_NETWORK_OFFLINE` và giữ nguyên màn hình Đăng ký.
- **Data Attributes**:
  - `phone`: String (E.164, max 20, optional nếu có `email`, default `null`, regex `^(\+84|0)[0-9]{9,10}$`).
  - `email`: String (RFC 5322, max 255, optional nếu có `phone`, default `null`, lowercase).
  - `password`: String (8..128 chars, required, >= 1 letter & >= 1 digit).
  - `full_name`: String (1..100 chars, required).
- **Business Rule `BR-001`**: Mỗi tài khoản bắt buộc có ít nhất 1 định danh (`phone` hoặc `email`) duy nhất. SĐT Việt Nam bắt đầu bằng `0` (10 số) chuẩn hóa sang `+84`. Mật khẩu dài `8..128` ký tự gồm ít nhất 1 chữ cái và 1 chữ số. Ví dụ: `'0912345678'` -> `'+84912345678'`; `'abcdefgh'` hoặc `'abc123'` bị từ chối.
- **Acceptance Criteria**:
  - **Given** người dùng chưa có tài khoản nhập SĐT `'0912345678'` và mật khẩu `'MatKhau123'`
    **When** bấm Đăng ký
    **Then** Backend trả `HTTP 201 Created`, lưu SĐT `'+84912345678'`, trả `access_token` và `refresh_token`, ứng dụng lưu vào `SecureStore`.
  - **Given** SĐT `'+84912345678'` đã tồn tại
    **When** gửi yêu cầu đăng ký với `'0912345678'`
    **Then** Backend trả `HTTP 409 Conflict` với mã `ERR_AUTH_DUPLICATE_IDENTIFIER`.
- **NFR Links**: `NFR-002`.

#### FR-002: Đăng nhập, đăng xuất và duy trì phiên ngoại tuyến an toàn
- **Sources**: `REQ-001`
- **Actors**: Người dùng đã đăng ký
- **Preconditions**: Tài khoản đã tồn tại (khi đăng nhập online) hoặc đã có phiên/dữ liệu cục bộ trên thiết bị (khi mở app offline).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng đăng nhập/đăng xuất bằng SĐT hoặc Email và mật khẩu, đồng bộ hồ sơ về máy và duy trì chế độ SOS ngoại tuyến ngay cả khi phiên hết hạn.
- **Main Flow**:
  1. Người dùng nhập định danh (SĐT hoặc Email) và mật khẩu trên màn hình Đăng nhập.
  2. Ứng dụng gửi `POST /api/v1/auth/login` tới FastAPI backend.
  3. Backend xác thực mật khẩu băm, cấp `access_token` và lưu hash của `refresh_token` vào `tbl_refresh_tokens`.
  4. Ứng dụng lưu token vào `SecureStore`, gọi `GET /api/v1/me` để đồng bộ hồ sơ cá nhân, thẻ y tế và danh bạ khẩn cấp về SQLite cục bộ.
- **Alternate Flows**:
  - Mở app khi offline với `refresh_token <= 30 ngày`: Vào thẳng màn hình chính ở chế độ Offline.
  - Mở app khi offline với `refresh_token > 30 ngày`: Vào **Limited Offline-SOS Mode** (nút SOS, SMS fallback, thẻ y tế và danh bạ cục bộ vẫn hoạt động; đồng bộ chuyến đi bị khóa tới khi đăng nhập lại online).
  - Đăng xuất (`POST /api/v1/auth/logout`): Thu hồi `refresh_token` trên server (`revoked_at = now`), xóa token khỏi `SecureStore` và xóa dữ liệu cá nhân trong SQLite.
- **Exception Flows**:
  - Sai mật khẩu hoặc không tìm thấy tài khoản: `HTTP 401 Unauthorized` (`ERR_AUTH_INVALID_CREDENTIALS`), giữ nguyên màn hình Đăng nhập.
  - `refresh_token` hết hạn hoặc bị thu hồi khi đang online: `HTTP 401 Unauthorized` (`ERR_AUTH_SESSION_EXPIRED`), xóa token và đưa về màn hình Đăng nhập.
- **Data Attributes**:
  - `identifier`: String (1..255 chars, required, phone hoặc email).
  - `password`: String (8..128 chars, required).
  - `access_token`: String (JWT, TTL 900s, output).
  - `refresh_token`: String (Opaque/JWT, TTL 30d, output).
- **Business Rule `BR-002`**: Phiên đầy đủ hợp lệ khi offline nếu `refresh_token <= 30 ngày`. Nếu `> 30 ngày` khi offline, mở Limited Offline-SOS Mode để không khóa nút SOS. Ví dụ: ngày 19 (`<= 30`) -> vào app đầy đủ; ngày 31 offline -> vào Limited Offline-SOS Mode.
- **Acceptance Criteria**:
  - **Given** tài khoản `'+84912345678'` tồn tại với mật khẩu `'MatKhau123'`
    **When** đăng nhập đúng thông tin
    **Then** Backend trả `HTTP 200 OK` kèm `access_token` và `refresh_token`; ứng dụng lưu vào `SecureStore` và gọi `GET /api/v1/me` đồng bộ SQLite.
  - **Given** thiết bị đang offline và `refresh_token` trong `SecureStore` đã quá 31 ngày
    **When** người dùng mở ứng dụng
    **Then** ứng dụng mở Limited Offline-SOS Mode cho phép bấm nút SOS và gửi SMS Fallback tới danh bạ khẩn cấp cục bộ.
- **NFR Links**: `NFR-002`.

#### FR-003: Quản lý danh bạ người thân khẩn cấp (tối đa 5 liên hệ)
- **Sources**: `REQ-002`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã có phiên đăng nhập hợp lệ.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng thêm, sửa, xóa và xem tối đa 5 liên hệ khẩn cấp gồm Tên, SĐT (chuẩn hóa `+84`) và Mối quan hệ, đồng bộ cả cục bộ và server.
- **Main Flow**:
  1. Người dùng mở màn hình Danh bạ khẩn cấp (`SCR-AUTH-03`) và chọn Thêm liên hệ.
  2. Ứng dụng kiểm tra số liên hệ hiện có trong SQLite (`< 5`), chuẩn hóa SĐT `0xxx -> +84xxx`, nhận Tên (`1..100` ký tự) và Mối quan hệ (`1..50` ký tự).
  3. Ứng dụng lưu bản ghi vào SQLite với `client_id` và `sync_status = PENDING`, gửi `POST /api/v1/contacts` nếu có mạng.
  4. Backend kiểm tra giới hạn `<= 5` liên hệ, trả `HTTP 201 Created` (hoặc `HTTP 200 OK` nếu trùng `(user_id, client_id)`) và app cập nhật `sync_status = SYNCED`.
- **Alternate Flows**:
  - Sửa/Xóa liên hệ: `PUT /api/v1/contacts/{id}` hoặc `DELETE /api/v1/contacts/{id}` (có modal xác nhận xóa trên UI).
  - Thao tác khi offline: Lưu SQLite với `sync_status = PENDING`, tự đồng bộ khi có mạng.
- **Exception Flows**:
  - Thêm liên hệ thứ 6 khi đã đủ 5 (cả cục bộ lẫn server): Chặn ngay với `ERR_CONTACT_LIMIT_EXCEEDED` (`HTTP 400 Bad Request` trên server); không lưu bản ghi mới.
  - Xung đột đồng bộ trả `HTTP 400 ERR_CONTACT_LIMIT_EXCEEDED`: Đánh dấu `sync_status = FAILED_PERMANENT` và thông báo người dùng xóa bớt liên hệ.
  - SĐT sai định dạng: `HTTP 422 Unprocessable Entity` (`ERR_CONTACT_INVALID_PHONE`).
- **Data Attributes**:
  - `contact_id`: UUID (required, server-generated).
  - `client_id`: UUID (required for offline sync, unique per `(user_id, client_id)`).
  - `name`: String (1..100 chars, required).
  - `phone`: String (10..15 digits, normalized to E.164 `+84...`, required).
  - `relationship`: String (1..50 chars, required).
- **Business Rule `BR-003`**: `0 <= count(active_contacts) <= 5` trên cả SQLite cục bộ và server. SĐT Việt Nam bắt đầu bằng `0` (10 số) chuẩn hóa sang `+84`. Ví dụ: `'0987654321'` -> `'+84987654321'`; đang có 5 liên hệ -> chặn thêm với `ERR_CONTACT_LIMIT_EXCEEDED`.
- **Acceptance Criteria**:
  - **Given** người dùng đang có 4 liên hệ khẩn cấp
    **When** thêm liên hệ thứ 5 (`'Nguyễn Văn A'`, `'0987654321'`, `'Anh trai'`)
    **Then** lưu thành công (`HTTP 201`) với SĐT `'+84987654321'`, tổng số liên hệ là 5.
  - **Given** người dùng đã có đủ 5 liên hệ (kể cả khi offline)
    **When** cố gắng thêm liên hệ thứ 6
    **Then** từ chối ngay tại thiết bị và trên server (`HTTP 400`) với mã `ERR_CONTACT_LIMIT_EXCEEDED`.
- **NFR Links**: `NFR-002`, `NFR-003`.

#### FR-004: Quản lý thẻ thông tin y tế và phương tiện cá nhân
- **Sources**: `REQ-003`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã có phiên đăng nhập hợp lệ.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng lưu và cập nhật thẻ thông tin y tế (nhóm máu, dị ứng thuốc, bệnh nền) và thông tin xe (biển số, loại xe) để tự động đính kèm khi phát SOS.
- **Main Flow**:
  1. Người dùng mở màn hình Thẻ Y tế & Xe (`SCR-AUTH-02`).
  2. Chọn nhóm máu, nhập dị ứng thuốc, bệnh nền, biển số xe và loại xe.
  3. Bấm Lưu: ứng dụng lưu SQLite với `sync_status = PENDING` và gửi `PUT /api/v1/profile/emergency-card`.
  4. Backend xác thực và trả `HTTP 200 OK`; app cập nhật `sync_status = SYNCED`.
- **Alternate Flows**:
  - Cập nhật khi offline: Lưu SQLite với `sync_status = PENDING` để sẵn sàng đính kèm SMS SOS.
- **Exception Flows**:
  - Nhóm máu ngoài tập cho phép: `HTTP 422 Unprocessable Entity` (`ERR_PROFILE_INVALID_BLOOD_TYPE`), giữ nguyên dữ liệu form.
  - Dị ứng/bệnh nền vượt 500 ký tự: `HTTP 422 Unprocessable Entity` (`ERR_PROFILE_FIELD_TOO_LONG`).
- **Data Attributes**:
  - `blood_type`: Enum (`A+|A-|B+|B-|AB+|AB-|O+|O-|UNKNOWN`, required, default `UNKNOWN`).
  - `drug_allergies`: String (0..500 chars, optional, default `null`).
  - `medical_conditions`: String (0..500 chars, optional, default `null`).
  - `vehicle_plate`: String (0..20 chars, optional, default `null`).
  - `vehicle_model`: String (0..100 chars, optional, default `null`).
- **Business Rule `BR-004`**: `blood_type` thuộc tập `{A+, A-, B+, B-, AB+, AB-, O+, O-, UNKNOWN}`. Ví dụ: `blood_type='O+'`, `vehicle_plate='29A1-12345'` -> hợp lệ.
- **Acceptance Criteria**:
  - **Given** người dùng đã đăng nhập
    **When** cập nhật `blood_type='O+'`, `drug_allergies='Penicillin'`, `vehicle_plate='29A1-12345'`, `vehicle_model='Honda Winner X'`
    **Then** lưu thành công (`HTTP 200 OK`) cả ở server và SQLite cục bộ.
  - **Given** người dùng gửi `blood_type='XYZ'`
    **When** gọi `PUT /api/v1/profile/emergency-card`
    **Then** Backend trả `HTTP 422` với mã `ERR_PROFILE_INVALID_BLOOD_TYPE`.
- **NFR Links**: `NFR-002`, `NFR-003`.

---

### Module 2: An toàn & Cảnh báo khẩn cấp (`sos_safety`)

#### FR-005: Kích hoạt nút SOS khẩn cấp 1 chạm (giữ 3s + đếm ngược hủy 5s)
- **Sources**: `REQ-004`
- **Actors**: Người dùng đã đăng nhập (hoặc đang ở Limited Offline-SOS Mode)
- **Preconditions**: Đang ở màn hình chính (`SCR-SOS-01`).
- **Requirement Statement**: Hệ thống SHALL cung cấp nút SOS nổi bật trên màn hình chính yêu cầu bấm giữ liên tục 3 giây để kích hoạt, sau đó mở cửa sổ đếm ngược 5 giây cho phép hủy trước khi phát cảnh báo.
- **Main Flow**:
  1. Người dùng bấm và giữ nút SOS trên màn hình chính liên tục đủ `3000 ms`.
  2. Ứng dụng rung phản hồi (haptic), chuyển sang trạng thái `COUNTDOWN` và đếm ngược 5 giây (`5 -> 0`) kèm nút `'HỦY SOS'`.
  3. Hết `5000 ms` không bấm hủy -> chuyển trạng thái SOS sang `ACTIVE` và gọi luồng `FR-006`.
- **Alternate Flows**:
  - Nhả tay trước `3000 ms`: Đặt lại tiến trình về `0`, giữ trạng thái `IDLE`.
  - Bấm `'HỦY SOS'` trong `5000 ms`: Hủy kích hoạt, ghi log `SOS_CANCELLED_IN_COUNTDOWN`, quay về `IDLE`.
- **Exception Flows**:
  - GPS chưa khóa được tọa độ mới nhưng có tọa độ cũ: Phát SOS với tọa độ cuối cùng và `is_stale_location = true`.
  - Thiết bị chưa từng có tọa độ GPS nào (máy mới cài/từ chối quyền): Vẫn cho phép phát SOS với `latitude = null`, `longitude = null` và `location_unavailable = true`.
  - Chưa có liên hệ khẩn cấp: Khi online vẫn gửi SOS lên server (tạo link web) và cảnh báo người dùng.
- **Data Attributes**:
  - `hold_duration_ms`: Integer (`>= 0`, trigger threshold `3000`, ephemeral).
  - `cancel_window_ms`: Integer (`0..5000`, default `5000`, ephemeral).
  - `sos_state`: Enum (`IDLE|COUNTDOWN|ACTIVE|RESOLVED`, required, default `IDLE`).
- **Business Rule `BR-005`**: `hold_duration >= 3000 ms`; `cancel_window = 5000 ms`. Không chặn SOS khi thiếu GPS hoặc thiếu danh bạ. Ví dụ: giữ 2500 ms rồi thả -> không kích hoạt; giữ 3000 ms -> đếm ngược 5s.
- **Acceptance Criteria**:
  - **Given** người dùng ở màn hình chính và thiết bị chưa từng có tọa độ GPS
    **When** giữ nút SOS đủ 3 giây và không bấm Hủy trong 5 giây
    **Then** trạng thái SOS vẫn chuyển `ACTIVE` với `location_unavailable = true` và kích hoạt `FR-006`.
  - **Given** màn hình đang đếm ngược SOS ở giây thứ 2
    **When** người dùng bấm `'HỦY SOS'`
    **Then** đếm ngược dừng, trạng thái về `IDLE` và không phát cảnh báo.
- **NFR Links**: `NFR-001`.

#### FR-006: Phát cảnh báo SOS đa kênh Online (bất đồng bộ) và SMS Fallback khi Offline
- **Sources**: `REQ-005`
- **Actors**: Hệ thống Mobile App, FastAPI Backend, Người thân khẩn cấp
- **Preconditions**: SOS vừa chuyển sang trạng thái `ACTIVE`.
- **Requirement Statement**: Hệ thống SHALL lưu phiên SOS và trả link theo dõi ngay lập tức khi có mạng (đồng thời gửi SMS Gateway bất đồng bộ), hoặc mở `expo-sms` composer khi mất mạng và xử lý đồng bộ bù khi có mạng.
- **Main Flow**:
  1. Ứng dụng thu thập GPS (hoặc `location_unavailable = true`), `battery_level`, `recorded_at`, `trip_id`, `EmergencyCard` và kiểm tra mạng qua `NetInfo`.
  2. Nếu `NetInfo` báo có mạng: gọi `POST /api/v1/sos/trigger` kèm `client_id` (timeout `5000 ms`).
  3. Backend lưu `SosSession` (tối đa 1 `ACTIVE`/user) với `tracking_token` 32-byte, đặt `delivery_status = PENDING`, trả `HTTP 201 Created` ngay lập tức và đưa tác vụ gửi SMS qua `SMSGatewayAdapter` vào hàng đợi nền.
  4. Tác vụ nền gửi SMS tới từng liên hệ khẩn cấp kèm tọa độ, % pin, thời điểm cập nhật cuối và `tracking_url`, sau đó cập nhật `delivery_status = SENT` (hoặc `PARTIAL_FAILED`).
- **Alternate Flows**:
  - `NetInfo` báo offline hoặc API timeout `> 5000 ms`: Lập tức (`< 1000 ms`) mở `expo-sms` composer điền sẵn mảng SĐT người thân và mẫu SMS (link Google Maps hoặc `'Chua xac dinh GPS'` nếu `location_unavailable=true`), rồi chuyển sang `SCR-SOS-04` có nút `'Gửi lại SMS'` phòng trường hợp người dùng đóng nhầm composer.
  - Đồng bộ bù khi có mạng lại sau SOS Offline: Nếu phiên chưa kết thúc trên máy, gửi `POST /api/v1/sos/trigger` (`triggered_offline=true`) để tạo `SosSession` và gửi SMS follow-up kèm `tracking_url`; nếu đã kết thúc trên máy (`resolved_offline=true`), lưu lịch sử `RESOLVED` (`delivery_status = SKIPPED`) và không gửi cảnh báo mới.
- **Exception Flows**:
  - `SMSGatewayAdapter` lỗi ở tác vụ nền: Retry 3 lần (`1s, 2s, 4s`); nếu vẫn lỗi đặt `delivery_status = PARTIAL_FAILED`.
  - Không có liên hệ khẩn cấp khi Offline: Hiển thị `ERR_SOS_NO_CONTACTS_OFFLINE` và gợi ý gọi 113/115.
- **Data Attributes**:
  - `client_id`: UUID (required, idempotency key per `(user_id, client_id)`).
  - `trip_id`: UUID (optional, default `null`).
  - `latitude` / `longitude`: Double (`-90..90` / `-180..180`, optional, `null` khi `location_unavailable = true`).
  - `location_unavailable`: Boolean (required, default `false`).
  - `battery_level`: Integer (`0..100`, required).
  - `is_stale_location`: Boolean (required, default `false`).
  - `triggered_offline`: Boolean (required, default `false`).
  - `resolved_offline`: Boolean (required, default `false`).
  - `recorded_at`: DateTime ISO-8601 UTC (required).
- **Business Rule `BR-006`**: Kiểm tra `NetInfo` trước khi gọi API; timeout `5000 ms`. Mẫu tin Online: `'[COT MOC SOS] <full_name> can ho tro luc <HH:mm>. Vi tri: <lat>,<lng | Chua xac dinh GPS> | Pin: <battery>% | Theo doi: <tracking_url>'`. Mẫu Follow-up offline sync: `'[COT MOC SOS - CAP NHAT LINK] <full_name> da kich hoat SOS offline luc <HH:mm>. Theo doi: <tracking_url>'`.
- **Acceptance Criteria**:
  - **Given** thiết bị online, pin 42%, tọa độ `(21.028511, 105.804817)`, có 2 liên hệ khẩn cấp
    **When** SOS kích hoạt
    **Then** `POST /api/v1/sos/trigger` trả `HTTP 201` ngay với `delivery_status = PENDING` và `tracking_url`; tác vụ nền gọi `SMSGatewayAdapter` gửi tin tới 2 liên hệ.
  - **Given** thiết bị offline, pin 15%, có liên hệ `'+84987654321'`
    **When** SOS kích hoạt và người dùng đóng nhầm cửa sổ SMS composer
    **Then** ứng dụng chuyển sang `SCR-SOS-04` hiển thị trạng thái SOS Offline và nút `'Gửi lại SMS'`.
  - **Given** một SOS Offline đã kết thúc trên máy (`resolved_offline = true`) trước khi có mạng
    **When** thiết bị có mạng trở lại và đồng bộ bù
    **Then** Backend tạo `SosSession` trạng thái `RESOLVED` (`delivery_status = SKIPPED`) và KHÔNG gửi cảnh báo mới.
- **NFR Links**: `NFR-001`, `NFR-003`.

#### FR-007: Trang Web theo dõi trực tiếp cho người thân qua Token tạm thời
- **Sources**: `REQ-006`
- **Actors**: Người thân (không cần đăng nhập/cài app), Chủ tài khoản
- **Preconditions**: Có `SosSession` với `tracking_token` hợp lệ.
- **Requirement Statement**: FastAPI backend SHALL cung cấp trang web công khai theo `tracking_token` tạm thời hiển thị vị trí cuối cùng, trạng thái SOS, mức pin và vệt di chuyển gần nhất mà người thân không cần cài app.
- **Main Flow**:
  1. Người thân mở `GET /track/{tracking_token}` trên trình duyệt.
  2. FastAPI tra cứu `tracking_token` trong `tbl_sos_sessions`.
  3. Trả về trang HTML nhẹ (`HTTP 200 OK`) hiển thị tọa độ cuối cùng (hoặc `'Chưa có tín hiệu GPS'` nếu `location_unavailable=true`), trạng thái SOS (`ACTIVE`/`RESOLVED`), `% pin`, `updated_at`, thẻ y tế/xe (CHỈ KHI `status == ACTIVE`) và tối đa 50 điểm vệt di chuyển gần nhất.
  4. Trang tự làm mới qua `GET /api/v1/track/{tracking_token}/status` mỗi 15 giây.
- **Alternate Flows**:
  - SOS chuyển `RESOLVED` (chưa quá 24h): Trang web hiển thị `'Đã an toàn (RESOLVED)'`, ẩn thẻ y tế/xe, và khóa vệt di chuyển + vị trí cuối tại thời điểm `<= ended_at` để không lộ vị trí sau khi đã an toàn.
- **Exception Flows**:
  - `tracking_token` không tồn tại: Trả `HTTP 404 Not Found` (`ERR_TRACK_TOKEN_NOT_FOUND`).
  - `tracking_token` đã hết hạn (`now > expires_at`) hoặc bị thu hồi (`revoked_at IS NOT NULL`): Trả `HTTP 410 Gone` (`ERR_TRACK_TOKEN_EXPIRED`).
- **Data Attributes**:
  - `tracking_token`: String (32-byte URL-safe, 43 chars, required).
  - `status`: Enum (`ACTIVE|RESOLVED`, output).
  - `trail`: Array<LatLngTimestamp> (max 50 items, filtered by `recorded_at <= ended_at` when `RESOLVED`, output).
  - `emergency_card`: Object (chỉ trả về khi `status == ACTIVE`, nullable).
- **Business Rule `BR-007`**: `tracking_token` 32-byte URL-safe. Nếu `ACTIVE`: hiển thị thẻ y tế và cập nhật trail liên tục (tối đa 72h). Nếu `RESOLVED`: ẩn thẻ y tế, chỉ trả về điểm có `recorded_at <= ended_at`, và link hết hạn sau `ended_at + 24h`.
- **Acceptance Criteria**:
  - **Given** phiên SOS `ACTIVE` với `tracking_token` hợp lệ, tọa độ `(21.028511, 105.804817)`, pin 35%
    **When** truy cập `GET /track/{tracking_token}`
    **Then** trả `HTTP 200 OK` với HTML hiển thị `ACTIVE`, tọa độ, pin `35%`, thẻ y tế và vệt di chuyển.
  - **Given** phiên SOS đã `RESOLVED` lúc `18:00` và chuyến đi ghi thêm breadcrumb lúc `18:05`
    **When** gọi `GET /api/v1/track/{tracking_token}/status` lúc `18:10`
    **Then** trả `RESOLVED`, ẩn thẻ y tế và chỉ trả các điểm có `recorded_at <= 18:00`.
  - **Given** `tracking_token` không tồn tại hoặc quá hạn 24h
    **When** truy cập `GET /track/{tracking_token}`
    **Then** trả `HTTP 404` (`ERR_TRACK_TOKEN_NOT_FOUND`) hoặc `HTTP 410` (`ERR_TRACK_TOKEN_EXPIRED`).
- **NFR Links**: `NFR-001`, `NFR-002`.

#### FR-008: Hẹn giờ Check-in an toàn (Dead Man's Switch)
- **Sources**: `REQ-007`
- **Actors**: Người dùng đã đăng nhập, Scheduler nền trên FastAPI
- **Preconditions**: Người dùng đã đăng nhập; hệ thống kiểm tra có ít nhất 1 liên hệ khẩn cấp (nếu chưa có thì cảnh báo trước khi đặt).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng đặt mốc thời gian dự kiến an toàn và tự động phát cảnh báo kèm tọa độ cuối cùng cho người thân nếu quá hạn mà người dùng không xác nhận 'Tôi an toàn'.
- **Main Flow**:
  1. Người dùng đặt `deadline_at` (`now + 5m <= deadline_at <= now + 72h`), ghi chú lộ trình (tùy chọn) và bấm Bắt đầu đếm giờ.
  2. Ứng dụng gửi `POST /api/v1/safety-timers` kèm tọa độ hiện tại; backend tạo bản ghi `ARMED` (tối đa 1 timer `ARMED`/user). Nếu `deadline_at - now > 10 phút`, app đặt lịch nhắc trước 10 phút; nếu `<= 10 phút`, app bỏ qua lịch nhắc và hiện toast nhắc nhớ.
  3. Trong khi `ARMED`, app cập nhật vị trí mỗi 5 phút qua `PUT /api/v1/safety-timers/{id}/location` và gọi `GET /api/v1/safety-timers/active` khi mở app.
  4. Quá `deadline_at` trong vòng `<= 60 giây` mà trạng thái vẫn là `ARMED`: Scheduler thực hiện compare-and-set nguyên tử (`ARMED -> EXPIRED_ALERTED`), tạo `SosSession` (hoặc gắn vào `SosSession ACTIVE` hiện có) với `trigger_source = DEAD_MAN_SWITCH` và phát cảnh báo tới người thân.
- **Alternate Flows**:
  - Bấm `'Tôi an toàn'` hoặc Gia hạn khi đang Online: `POST /api/v1/safety-timers/{id}/checkin` (atomic `ARMED -> CHECKED_IN`) hoặc `/extend`.
  - Bấm `'Tôi an toàn'` hoặc Gia hạn khi đang Offline: Lưu hành động vào SQLite (`sync_status = PENDING`), hiển thị `'Chờ đồng bộ — cần mạng để xác nhận với server'` và tự gửi khi có mạng.
  - Hủy hẹn giờ: `POST /api/v1/safety-timers/{id}/cancel` -> `CANCELLED`.
- **Exception Flows**:
  - `deadline_at` ở quá khứ, `< now + 5m`, hoặc `> now + 72h`: `HTTP 422 Unprocessable Entity` (`ERR_TIMER_INVALID_DEADLINE`).
  - Tạo timer mới khi đã có timer `ARMED`: `HTTP 409 Conflict` (`ERR_TIMER_ALREADY_ARMED`).
  - Check-in sau khi scheduler đã chuyển `EXPIRED_ALERTED`: `HTTP 409 Conflict` (`ERR_TIMER_ALREADY_EXPIRED`).
- **Data Attributes**:
  - `deadline_at`: DateTime ISO-8601 UTC (required, `now + 5m <= deadline_at <= now + 72h`).
  - `note`: String (0..200 chars, optional, default `null`).
  - `extend_minutes`: Integer (Enum `{30, 60}`, required for extend).
  - `last_latitude` / `last_longitude`: Double (optional, updated every 5m).
- **Business Rule `BR-008`**: Tối đa 1 timer `ARMED`/user. `now + 5m <= deadline_at <= now + 72h`. Độ trễ cảnh báo `<= 60s`. Chuyển trạng thái bằng atomic compare-and-set trên `status == 'ARMED'`. Ví dụ: `deadline = 18:00:00`, scheduler quét `18:00:15` -> check-in đến `18:00:10` vẫn thành `CHECKED_IN`; đến `18:00:30` -> `409 ERR_TIMER_ALREADY_EXPIRED`.
- **Acceptance Criteria**:
  - **Given** safety timer đặt `deadline_at = 18:00:00` với tọa độ cuối `(21.1, 105.8)`
    **When** đồng hồ server vượt `18:00:00` trong vòng 60 giây mà chưa check-in
    **Then** server chuyển `EXPIRED_ALERTED`, tạo `SosSession` (`DEAD_MAN_SWITCH`) và phát cảnh báo kèm tọa độ `(21.1, 105.8)`.
  - **Given** người dùng đặt safety timer với `deadline = now + 5 phút`
    **When** timer được kích hoạt
    **Then** hệ thống không tạo local notification trong quá khứ và hiển thị toast nhắc trực tiếp trên màn hình.
  - **Given** safety timer `deadline_at = 18:00:00` đã chuyển `EXPIRED_ALERTED` lúc `18:00:15`
    **When** người dùng gửi check-in lúc `18:00:30`
    **Then** trả `HTTP 409 Conflict` với mã `ERR_TIMER_ALREADY_EXPIRED`.
- **NFR Links**: `NFR-002`.

#### FR-009: Lưu vết hành trình nền tối ưu pin (Breadcrumb Trail)
- **Sources**: `REQ-008`
- **Actors**: Dịch vụ nền Mobile App, FastAPI Backend
- **Preconditions**: Có một chuyến đi ở trạng thái `ACTIVE`.
- **Requirement Statement**: Hệ thống SHALL ghi nhận tọa độ GPS theo chu kỳ tối ưu pin khi chuyến đi đang chạy, lưu cục bộ trên thiết bị và đồng bộ theo lô lên server khi có mạng.
- **Main Flow**:
  1. Khi chuyến đi `ACTIVE`, dịch vụ nền thu thập GPS (`lat`, `lng`, `altitude_m`, `speed_kmh`, `accuracy_m`, `battery_level`, `recorded_at`).
  2. Loại bỏ điểm có `accuracy_m > 100m`; điều chỉnh tần suất: `15s` khi `speed >= 2.0 km/h`, `120s` khi `speed < 2.0 km/h`.
  3. Lưu điểm hợp lệ vào SQLite với `sync_status = PENDING`.
  4. Khi có mạng và đủ lô 10 điểm (hoặc mỗi 60s), gửi `POST /api/v1/trips/{trip_id}/breadcrumbs` và cập nhật `sync_status = SYNCED`.
- **Alternate Flows**:
  - Mất mạng kéo dài: Lưu toàn bộ trong SQLite và đồng bộ bù theo thứ tự thời gian (sau khi `Trip` cha đã `SYNCED`).
- **Exception Flows**:
  - Từ chối quyền Background Location: Hiển thị `ERR_LOCATION_PERMISSION_DENIED` trên `SCR-TRIP-01` và hướng dẫn mở Cài đặt; chuyến đi vẫn tạo được nhưng không ghi breadcrumb nền.
  - Hệ điều hành tạm dừng dịch vụ nền: Khi mở lại app, kiểm tra chuyến `ACTIVE` trong SQLite và tự khởi động lại dịch vụ nền.
  - Điểm GPS có `accuracy_m > 100m`: Loại bỏ điểm nhiễu; lỗi 5xx/mạng khi đồng bộ thì giữ `sync_status = PENDING`.
- **Data Attributes**:
  - `client_id`: UUID (required, unique per `(user_id, client_id)`).
  - `latitude`: Double (`-90..90`, required).
  - `longitude`: Double (`-180..180`, required).
  - `altitude_m`: Double (optional, default `null`).
  - `speed_kmh`: Double (`>= 0`, optional, default `null`).
  - `accuracy_m`: Double (`>= 0`, required, filter `<= 100`).
  - `battery_level`: Integer (`0..100`, required).
  - `recorded_at`: DateTime ISO-8601 UTC (required).
- **Business Rule `BR-009`**: Chu kỳ = `15s` nếu `speed >= 2.0 km/h`, `120s` nếu `speed < 2.0 km/h`; lọc bỏ `accuracy_m > 100m`. Ví dụ: `speed = 45 km/h, accuracy_m = 12` -> ghi mỗi 15s; `accuracy_m = 250` -> bỏ qua.
- **Acceptance Criteria**:
  - **Given** chuyến đi `ACTIVE` đang offline
    **When** ghi nhận 3 điểm GPS hợp lệ (`accuracy_m = 10`) rồi có mạng trở lại
    **Then** 3 điểm lưu SQLite trước và tự đồng bộ lên `POST /api/v1/trips/{trip_id}/breadcrumbs` (`HTTP 200 OK`).
  - **Given** điểm GPS có `accuracy_m = 250`
    **When** bộ lọc xử lý
    **Then** điểm bị loại bỏ, không lưu vào SQLite.
- **NFR Links**: `NFR-003`, `NFR-004`.

---

### Module 3: Nhật ký hành trình & Chia sẻ (`trip_journal`)

#### FR-010: Quản lý vòng đời chuyến đi và lịch sử (Bắt đầu / Tạm dừng / Kết thúc)
- **Sources**: `REQ-009`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã đăng nhập (online hoặc offline).
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng Bắt đầu, Tạm dừng, Tiếp tục và Kết thúc chuyến đi, tự động tính tổng quãng đường (km) và thời gian di chuyển để xem lại trong lịch sử.
- **Main Flow**:
  1. Người dùng nhập tên chuyến đi (tùy chọn, mặc định `'Chuyến đi YYYY-MM-DD HH:mm'`) và bấm `'Bắt đầu chuyến đi'`.
  2. Ứng dụng tạo chuyến đi `ACTIVE` trong SQLite và đồng bộ `POST /api/v1/trips`.
  3. Người dùng có thể bấm `'Tạm dừng'` (`ACTIVE -> PAUSED`) hoặc `'Tiếp tục'` (`PAUSED -> ACTIVE`).
  4. Bấm `'Kết thúc chuyến đi'` -> chuyển `COMPLETED`, tính tổng `distance_km` (Haversine) và `duration_seconds` (không tính thời gian `PAUSED`).
- **Alternate Flows**:
  - Xem lịch sử: Tab Nhật ký hiển thị danh sách chuyến đi đã hoàn thành kèm tên, ngày thực hiện (`started_at`), `distance_km` và `duration_seconds`.
- **Exception Flows**:
  - Tạo chuyến đi mới khi đang có chuyến `ACTIVE` hoặc `PAUSED`: Chặn với `HTTP 409 Conflict` (`ERR_TRIP_ALREADY_ACTIVE`); trạng thái chuyến hiện tại không đổi.
  - Chuyển trạng thái không hợp lệ: `HTTP 409 Conflict` (`ERR_TRIP_INVALID_STATE_TRANSITION`).
- **Data Attributes**:
  - `client_id`: UUID (required, unique per `(user_id, client_id)`).
  - `title`: String (1..120 chars, optional, default `'Chuyến đi YYYY-MM-DD HH:mm'`).
  - `status`: Enum (`ACTIVE|PAUSED|COMPLETED`, required, default `ACTIVE`).
  - `distance_km`: Decimal(10,2) (`>= 0.00`, default `0.00`).
  - `duration_seconds`: Integer (`>= 0`, default `0`).
- **Business Rule `BR-010`**: Tối đa 1 chuyến `ACTIVE`/`PAUSED` mỗi user tại 1 thời điểm. `distance_km` tính bằng tổng Haversine các cặp breadcrumb liên tiếp (làm tròn 2 chữ số thập phân). Ví dụ: `(21.000, 105.800)` -> `(21.009, 105.800)` = `1.00 km`.
- **Acceptance Criteria**:
  - **Given** không có chuyến đi nào đang chạy, bắt đầu lúc `08:00:00`
    **When** ghi 2 breadcrumb `(21.000, 105.800)` và `(21.009, 105.800)`, tạm dừng `08:10:00..08:20:00` (600s), rồi kết thúc lúc `08:30:00`
    **Then** trạng thái chuyển `ACTIVE -> PAUSED -> ACTIVE -> COMPLETED`, `distance_km = 1.00 km` và `duration_seconds = 1200`.
  - **Given** đang có chuyến `T-001` ở trạng thái `ACTIVE`
    **When** cố gắng tạo chuyến đi mới `T-002`
    **Then** từ chối với `HTTP 409 Conflict` và mã `ERR_TRIP_ALREADY_ACTIVE`.
- **NFR Links**: `NFR-003`.

#### FR-011: Check-in ảnh & ghi chú gắn tọa độ GPS với hàng đợi Offline
- **Sources**: `REQ-010`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đang có chuyến đi ở trạng thái `ACTIVE` hoặc `PAUSED`.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng chụp/chọn ảnh và nhập ghi chú gắn đúng tọa độ GPS hiện tại trong chuyến đi, lưu hàng đợi cục bộ khi mất sóng và tự đồng bộ khi có mạng.
- **Main Flow**:
  1. Trong chuyến đi `ACTIVE`/`PAUSED`, bấm Check-in, chụp/chọn ảnh (JPEG/PNG) và nhập ghi chú (`<= 500` ký tự).
  2. Nén ảnh xuống tối đa `1920px` cạnh dài (`JPEG 85%`), gắn GPS hiện tại (hoặc last known với `is_stale_location = true`) và render watermark (`FR-012`).
  3. Lưu ảnh và metadata vào SQLite với `sync_status = PENDING`.
  4. Khi có mạng (và `Trip` cha đã `SYNCED`), worker tải lên `POST /api/v1/trips/{trip_id}/checkins` và cập nhật `sync_status = SYNCED`.
- **Alternate Flows**:
  - Check-in khi offline: Hiển thị ngay trên bản đồ/danh sách với huy hiệu `'Chờ đồng bộ'`, tự upload khi có mạng.
- **Exception Flows**:
  - Ảnh sai định dạng (không phải JPEG/PNG) hoặc sau khi nén xuống 1920px vẫn `> 10 MB`: Từ chối lưu với `ERR_CHECKIN_INVALID_IMAGE` (`HTTP 422 Unprocessable Entity` trên server).
  - Ghi chú `> 500` ký tự: Từ chối lưu với `ERR_CHECKIN_NOTE_TOO_LONG` (`HTTP 422` trên server).
  - Chưa từng có tọa độ GPS nào trên máy: Chặn lưu với `ERR_CHECKIN_NO_GPS`.
  - Upload lỗi mạng sau 3 lần retry (`5s, 15s, 45s`): Giữ `sync_status = PENDING` và thử lại khi có sự kiện mạng; nếu server trả `4xx` thì đánh dấu `FAILED_PERMANENT`.
- **Data Attributes**:
  - `client_id`: UUID (required, unique per `(user_id, client_id)`).
  - `image_path`: File/String (JPEG/PNG, max 1920px longest edge, <= 10 MB after compression, required).
  - `note`: String (0..500 chars, optional, default `null`).
  - `latitude` / `longitude`: Double (required).
  - `is_stale_location`: Boolean (required, default `false`).
  - `altitude_m`: Double (optional, default `null`).
- **Business Rule `BR-011`**: Ghi chú `<= 500` ký tự; ảnh nén về max `1920px` cạnh dài (`JPEG 85%`) và sau nén `<= 10 MB` (JPEG/PNG). Ví dụ: ảnh gốc 12 MB -> nén còn 2.4 MB JPEG -> hợp lệ.
- **Acceptance Criteria**:
  - **Given** chuyến đi `ACTIVE` ở vùng mất sóng
    **When** chụp ảnh check-in với ghi chú `'Đỉnh đèo Mã Pí Lèng'`
    **Then** lưu hàng đợi với `sync_status = PENDING`, hiện huy hiệu `'Chờ đồng bộ'`; khi có mạng tự đồng bộ lên server (`HTTP 201`).
  - **Given** ghi chú dài 600 ký tự
    **When** bấm lưu Check-in
    **Then** từ chối với `HTTP 422` / lỗi cục bộ mã `ERR_CHECKIN_NOTE_TOO_LONG`.
- **NFR Links**: `NFR-003`.

#### FR-012: Gắn watermark thông số lên ảnh Check-in
- **Sources**: `REQ-011`
- **Actors**: Hệ thống Mobile App
- **Preconditions**: Người dùng vừa chụp/chọn và nén ảnh trong luồng `FR-011`.
- **Requirement Statement**: Hệ thống SHALL tự động gắn lớp phủ watermark lên ảnh check-in gồm Tên địa điểm (hoặc tọa độ GPS), Độ cao (m) và Ngày giờ chụp theo múi giờ thiết bị trước khi lưu và đồng bộ.
- **Main Flow**:
  1. Xác định nguồn thông số: Nếu chụp từ Camera, dùng GPS hiện tại, thời gian thiết bị hiện tại và độ cao làm tròn số nguyên (`Math.round`); nếu chọn từ Thư viện (Gallery), ưu tiên đọc EXIF `DateTimeOriginal` & EXIF GPS/Altitude nếu có, nếu thiếu thì dùng thời gian & GPS thiết bị hiện tại.
  2. Nếu online, gọi OpenStreetMap Nominatim (`timeout 2000 ms`, cache 24h theo tọa độ 4 chữ số thập phân) để lấy `location_name` (cắt tối đa 40 ký tự + `'...'` nếu dài hơn); nếu offline/timeout dùng `'lat, lng'` 6 chữ số thập phân.
  3. Vẽ dải watermark bán trong suốt ở góc dưới ảnh theo định dạng `'<Địa điểm | Tọa độ> | <Độ cao nguyên> m | <YYYY-MM-DD HH:mm>'` và lưu làm ảnh check-in chính thức.
- **Alternate Flows**:
  - Offline hoặc Nominatim timeout `> 2000 ms`: Hiển thị tọa độ `'21.028511, 105.804817'`.
  - `altitude_m` là `null`: Hiển thị `'-- m'`.
- **Exception Flows**:
  - Lỗi render đồ họa: Ghi log `ERR_WATERMARK_RENDER_FAILED` và giữ ảnh gốc kèm metadata văn bản.
- **Data Attributes**:
  - `location_name`: String (0..200 chars in DB, truncated to 40 chars on image, optional).
  - `altitude_display`: String (`Math.round(altitude_m) + ' m'` or `'-- m'`, computed).
  - `captured_at_local`: String (`YYYY-MM-DD HH:mm`, device local timezone, required).
- **Business Rule `BR-012`**: Watermark gồm 3 phần: `'<Địa điểm (<=40 chars) | Tọa độ> | <Math.round(altitude_m)> m | <YYYY-MM-DD HH:mm (Local TZ)>'`. Không dùng dấu phẩy phân cách hàng nghìn cho độ cao. Ví dụ: `'Đèo Ô Quy Hồ | 2000 m | 2026-11-25 10:30'`.
- **Acceptance Criteria**:
  - **Given** chụp ảnh tại `(22.356410, 103.776520)`, độ cao `2000.4 m`, lúc `2026-11-25 10:30` khi offline
    **When** xử lý ảnh check-in
    **Then** ảnh kết quả có watermark chứa `'22.356410, 103.776520 | 2000 m | 2026-11-25 10:30'`.
  - **Given** người dùng chọn ảnh từ Thư viện (Gallery) có EXIF `DateTimeOriginal = '2026-11-24 15:20'` nhưng không có EXIF GPS
    **When** render watermark
    **Then** watermark dùng thời gian EXIF `'2026-11-24 15:20'` và tọa độ GPS hiện tại của thiết bị.
- **NFR Links**: `NFR-003`.

#### FR-013: Export ảnh tổng kết hành trình (Poster 9:16 hoặc 1:1) có che 1–2 km đầu/cuối
- **Sources**: `REQ-012`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Chuyến đi đã hoàn thành (`status == COMPLETED`) và có ít nhất 2 ảnh check-in.
- **Requirement Statement**: Hệ thống SHALL cho phép người dùng chọn 2–4 ảnh check-in nổi bật của chuyến đi đã hoàn thành, chọn tỷ lệ 9:16 hoặc 1:1 và tùy chọn ẩn 1–2 km đầu/cuối cung đường để xuất ảnh tổng kết trên nền tối giản offline.
- **Main Flow**:
  1. Từ Chi tiết chuyến đi (`COMPLETED`), bấm `'Xuất ảnh hành trình'`.
  2. Chọn 2–4 ảnh check-in, chọn tỷ lệ `9:16` (`1080x1920 px`) hoặc `1:1` (`1080x1080 px`), chọn mức che đầu/cuối `privacy_trim_km` trong `{0, 1, 2}` km.
  3. Hệ thống tính `effective_trim = min(privacy_trim_km, 0.25 * distance_km)` cho mỗi đầu để luôn giữ lại ít nhất 50% cung đường, vẽ đường polyline lên nền bản đồ tối giản offline kèm lưới ảnh (2 ảnh: chia đôi; 3 ảnh: 1 lớn trên + 2 nhỏ dưới; 4 ảnh: lưới 2x2), tổng `distance_km` và thời gian di chuyển.
  4. Xem trước poster và lưu về máy hoặc chia sẻ qua OS Share Sheet.
- **Alternate Flows**:
  - Chuyến đi ngắn (`0.25 * distance_km < privacy_trim_km`): Giới hạn mức che ở `0.25 * distance_km` mỗi đầu và hiển thị thông báo giải thích.
- **Exception Flows**:
  - Chọn `< 2` hoặc `> 4` ảnh: Từ chối với `ERR_EXPORT_INVALID_PHOTO_COUNT`.
  - Chuyến đi chưa hoàn thành (`status != COMPLETED`): Vô hiệu hóa nút Xuất với mã `ERR_EXPORT_TRIP_NOT_COMPLETED`.
  - Từ chối quyền lưu thư viện ảnh: Hiển thị `ERR_EXPORT_STORAGE_PERMISSION_DENIED` và gợi ý mở Cài đặt, vẫn cho phép OS Share Sheet.
- **Data Attributes**:
  - `selected_photo_ids`: Array<UUID> (`2..4` items, required).
  - `aspect_ratio`: Enum (`9:16|1:1`, required, default `9:16`).
  - `privacy_trim_km`: Integer (Enum `{0, 1, 2}`, required, default `1`).
- **Business Rule `BR-013`**: `2 <= selected_photos <= 4`; tỷ lệ `{'9:16', '1:1'}`; `privacy_trim_km in {0, 1, 2}`. `effective_trim = min(privacy_trim_km, 0.25 * distance_km)` mỗi đầu. Ví dụ: chuyến `2.00 km`, trim `1 km` -> `effective_trim = min(1, 0.50) = 0.50 km` mỗi đầu -> vẽ `1.00 km` ở giữa; chuyến `4.00 km`, trim `2 km` -> `effective_trim = 1.00 km` mỗi đầu -> vẽ `2.00 km` ở giữa.
- **Acceptance Criteria**:
  - **Given** chuyến đi `COMPLETED` dài `2.00 km` có 3 ảnh check-in
    **When** chọn 2 ảnh, tỷ lệ `1:1`, che `1 km` đầu/cuối và bấm Xuất
    **Then** áp dụng `effective_trim = 0.50 km` mỗi đầu, vẽ đoạn giữa `1.00 km` trên ảnh `1080x1080 px`.
  - **Given** người dùng chỉ chọn 1 ảnh
    **When** bấm Xuất ảnh hành trình
    **Then** từ chối với mã `ERR_EXPORT_INVALID_PHOTO_COUNT`.
- **NFR Links**: `NFR-002`.

#### FR-014: Tra cứu, cập nhật Heartbeat, kết thúc phiên SOS và thu hồi link theo dõi
- **Sources**: `REQ-005`, `REQ-006`
- **Actors**: Người dùng đã đăng nhập
- **Preconditions**: Đã đăng nhập; có phiên SOS `ACTIVE` (do nút SOS hoặc Dead Man's Switch tạo).
- **Requirement Statement**: Hệ thống SHALL cho phép ứng dụng tra cứu phiên SOS đang hoạt động (kể cả do Dead Man's Switch tạo), cập nhật vị trí/pin định kỳ, kết thúc phiên SOS hoặc thu hồi tức thì link Web Tracking.
- **Main Flow**:
  1. Khi mở app hoặc nhận thông báo timer quá hạn, ứng dụng gọi `GET /api/v1/sos/active` để lấy `sos_id`, `tracking_url` và `delivery_status`.
  2. Khi `SosSession` đang `ACTIVE`, ứng dụng gửi `POST /api/v1/sos/{sos_id}/heartbeat` mỗi 30 giây kèm `latitude`, `longitude`, `battery_level`, `recorded_at`.
  3. Khi bấm `'Kết thúc SOS'`, ứng dụng gọi `POST /api/v1/sos/{sos_id}/resolve`; backend đặt `status = RESOLVED`, `ended_at = now`, `expires_at = ended_at + 24h`.
  4. Khi bấm `'Thu hồi link theo dõi'`, ứng dụng gọi `POST /api/v1/sos/{sos_id}/revoke-link`; backend đặt `revoked_at = now` và `expires_at = now`.
- **Alternate Flows**:
  - Mất mạng khi gửi heartbeat: Lưu tạm điểm mới nhất vào SQLite và gửi khi có mạng lại.
- **Exception Flows**:
  - Gọi resolve/revoke cho `sos_id` của user khác: `HTTP 403 Forbidden` (`ERR_FORBIDDEN_RESOURCE`).
  - Gọi heartbeat hoặc resolve cho phiên SOS đã `RESOLVED`: `HTTP 409 Conflict` (`ERR_SOS_NOT_ACTIVE`).
- **Data Attributes**:
  - `sos_id`: UUID (required, path param).
  - `latitude` / `longitude`: Double (required for heartbeat).
  - `battery_level`: Integer (`0..100`, required for heartbeat).
  - `recorded_at`: DateTime ISO-8601 UTC (required for heartbeat).
- **Business Rule `BR-014`**: Mỗi user có tối đa 1 `SosSession ACTIVE` tại 1 thời điểm. Phiên `ACTIVE` tự động chuyển `RESOLVED` sau tối đa 72 giờ nếu không kết thúc thủ công. Heartbeat gửi mỗi 30s khi SOS `ACTIVE`.
- **Acceptance Criteria**:
  - **Given** Dead Man's Switch vừa hết hạn trên server và tạo `SosSession ACTIVE`
    **When** ứng dụng gọi `GET /api/v1/sos/active`
    **Then** Backend trả `HTTP 200 OK` kèm `sos_id` và `tracking_url` để người dùng xem và kết thúc trên `SCR-SOS-04`.
  - **Given** phiên SOS đang `ACTIVE`
    **When** chủ tài khoản gọi `POST /api/v1/sos/{sos_id}/revoke-link`
    **Then** trả `HTTP 200 OK` và mọi truy cập `GET /track/{tracking_token}` sau đó trả về `HTTP 410 Gone`.
- **NFR Links**: `NFR-001`, `NFR-002`.

---

## 6. Non-Functional Requirements (ISO/IEC 25010)

| NFR ID | Characteristic | Sub-Characteristic | Target Metric / Acceptance Threshold | Verification Method |
|---|---|---|---|---|
| **NFR-001** | Performance | Time Behavior | FastAPI REST API (gồm `POST /api/v1/sos/trigger` bất đồng bộ) `p95 < 300 ms`; Offline SOS SMS fallback `< 1000 ms` | Load/API timing test & unit timer test |
| **NFR-002** | Security | Confidentiality & Access Control | Password hashed (bcrypt/argon2), JWT in SecureStore, 32-byte tracking token, login `<= 5 req/min/IP` (`429`), tracking `<= 120 req/min/(token, IP)` & `<= 20 req/min/IP` cho 404/410 (`429`), owner check (`403`) | Security, CGNAT rate-limit & ownership test |
| **NFR-003** | Reliability | Fault Tolerance | Zero data loss offline via SQLite queue; idempotent sync by `(user_id, client_id)` (`200 OK` replay); Trip -> Breadcrumb/Checkin sync order | Offline queue & duplicate-sync test |
| **NFR-004** | Efficiency | Resource Utilization | Background breadcrumb tracking `<= 5%` battery/hour on iPhone 13 (iOS 17+) and Pixel 6 (Android 13+), screen off, other apps closed, starting charge `>= 80%` | Battery & sampling-interval simulation test |

---

## 7. Assumptions, Dependencies & Constraints

### 7.1 Assumptions Index (All Confirmed by User)
- **ASM-001**: Đăng ký/đăng nhập dùng SĐT hoặc Email + mật khẩu (`8..128` ký tự, >= 1 chữ cái và >= 1 chữ số), cấp JWT lưu SecureStore.
- **ASM-002**: Khi Offline phát SOS, app mở `expo-sms` composer điền sẵn danh sách SĐT người thân và nội dung chuẩn; khi có mạng lại sẽ đồng bộ bù `POST /api/v1/sos/trigger`.
- **ASM-003**: `tracking_token` là chuỗi ngẫu nhiên 32-byte URL-safe, hết hạn sau 24 giờ kể từ khi kết thúc SOS (tối đa 72h nếu chưa resolve) hoặc thu hồi ngay.
- **ASM-004**: Safety Timer tối đa 72 giờ, nhắc trước 10 phút (bỏ qua nếu `<= 10` phút), gia hạn +30/+60 phút; scheduler quét và phát cảnh báo quá hạn trong `<= 60 giây`.
- **ASM-005**: Breadcrumb mặc định 15s khi di chuyển (`>= 2 km/h`) và 120s khi đứng yên; Web Tracking poll mỗi 15s và hiển thị tối đa 50 điểm gần nhất.
- **ASM-006**: Export Poster dùng mức che rời rạc `{0, 1, 2}` km và vẽ cung đường polyline trên nền bản đồ tối giản để chạy 100% offline.
- **ASM-007**: `SMSGatewayAdapter` dùng giao thức REST SMS Việt Nam (eSMS/SpeedSMS) ở production và `MockSMSGatewayAdapter` trong dev/test; Push notification tới người thân hoãn sang Phase 2.

### 7.2 Dependencies & External Interfaces
- **DEP-001**: OS Location / GPS, Background Location & Battery APIs.
- **DEP-002**: `expo-sms` Composer, Local Notifications, Camera/Gallery & Share Sheet.
- **DEP-003**: `SMSGatewayAdapter` & OpenStreetMap Nominatim (`timeout 2000 ms`, `<= 1 req/s`, `User-Agent: CotMocApp/1.0`, cache 24h).

### 7.3 Design Constraints
- **CON-001**: Mobile dùng React Native + TypeScript (`npm test`, `npm run typecheck`, `npm run lint`).
- **CON-002**: Backend dùng FastAPI + Python (`pytest`, `python -m compileall .`).

---

## 8. Open Questions & Ambiguities Register

| Question ID | Description | Owner | Status | Resolution |
|---|---|---|---|---|
| **OQ-001** | Cơ chế xác thực cho Đăng ký / Đăng nhập (REQ-001)? | User / PO | `RESOLVED` | Dùng Mật khẩu (SĐT hoặc Email + Password) với JWT lưu SecureStore. |
| **OQ-002** | Hành vi SMS Fallback khi mất mạng (REQ-005) và kênh thông báo Online? | User / PO | `RESOLVED` | Offline mở `expo-sms` + đồng bộ bù; Online dùng `SMSGatewayAdapter` bất đồng bộ (hoãn Push sang Phase 2). |
| **OQ-003** | Thời hạn hiệu lực (TTL) của URL theo dõi trực tiếp (REQ-006)? | User / PO | `RESOLVED` | Hết hạn sau 24 giờ kể từ khi kết thúc SOS, hoặc thu hồi ngay khi tắt chia sẻ. |
| **OQ-004** | Hiển thị thẻ y tế & biển số xe trên trang Web Tracking công khai? | User / PO | `RESOLVED` | Hiển thị CHỈ KHI `SOS.status == ACTIVE` (ẩn hoàn toàn khi `RESOLVED`). |

---

## 9. Requirements Traceability Matrix (RTM) Anchor
Chi tiết toàn bộ 18 source IDs (`REQ-001`..`REQ-018`) được lập bảng 1-1 tại `artifacts/rtm.md`.

---

## 10. Review Responses (SA_REVIEW Round 2 — `F-001..F-017`)
- **F-001**: Đã bổ sung `GET /api/v1/sos/active` và `GET /api/v1/safety-timers/active`, quy tắc tối đa 1 `ACTIVE` `SosSession`, tự động `RESOLVED` sau 72h, bỏ trạng thái `CANCELLED` thừa trên `SosSession`, bổ sung luồng offline `'Tôi an toàn'`/`extend` và atomic compare-and-set cho `SafetyTimer`.
- **F-002**: Đã loại bỏ `PushAdapter` khỏi Phase 1 MVP (`ASM-007`), chuẩn hóa `+84` cho SĐT danh bạ (`FR-003`), quy định rõ mẫu tin follow-up cho `triggered_offline = true` và bỏ qua gửi tin nếu `resolved_offline = true`.
- **F-003**: Đã chuyển gửi SMS Gateway trong `POST /api/v1/sos/trigger` sang bất đồng bộ (`delivery_status = PENDING` trên `201 Created`) để đồng nhất với `NFR-001` `p95 < 300ms`.
- **F-004**: Đã sửa công thức cắt thành `effective_trim = min(privacy_trim_km, 0.25 * distance_km)` kèm ví dụ biên `2.00 km` và `4.00 km` trong `FR-013`.
- **F-005**: Đã ánh xạ đầy đủ 28 mã lỗi trong `fsd.md` §3, bổ sung States & Data Contracts cho `SCR-TRIP-02`/`SCR-TRIP-03`, và bổ sung các nút điều khiển chuyến đi trong `SCR-TRIP-01`.
- **F-006**: Đã bổ sung luồng SOS khi chưa từng có GPS (`location_unavailable = true`, tọa độ nullable, mẫu SMS không có link Maps).
- **F-007**: Đã bổ sung chế độ **Limited Offline-SOS Mode** khi `refresh_token > 30 ngày` ở chế độ offline (`FR-002`).
- **F-008**: Đã quy định rõ nguồn thời gian/GPS cho Camera vs Gallery (EXIF), làm tròn `Math.round(altitude_m)` và cắt ngắn `location_name` tối đa 40 ký tự (`FR-012`).
- **F-009**: Đã giới hạn dữ liệu trail trên Web Tracking theo `recorded_at <= ended_at` khi SOS đã `RESOLVED` (`FR-007`).
- **F-010**: Đã điều chỉnh rate limit tracking thành `120 req/min/(token, IP)` và `20 req/min/IP` cho lookup 404/410 để hỗ trợ CGNAT (`NFR-002`).
- **F-011**: Đã giới hạn khóa idempotent theo `(user_id, client_id)` và trả `HTTP 200 OK` khi replay (`data-dictionary.md`, `NFR-003`).
- **F-012**: Đã ghi nhận giới hạn Nominatim (`1 req/s`, `User-Agent`, cache 24h) và dùng `expo-sms` hỗ trợ mảng nhiều SĐT trên iOS & Android (`integration-matrix.md`).
- **F-013**: Đã bổ sung `GET /api/v1/me` và `POST /api/v1/auth/logout` (`FR-002`, `integration-matrix.md`).
- **F-014**: Đã bổ sung trạng thái sau khi mở/đóng nhầm SMS Composer với nút `'Gửi lại SMS'` trên `SCR-SOS-04`.
- **F-015**: Đã chỉ định thiết bị tham chiếu iPhone 13 (iOS 17+) và Pixel 6 (Android 13+) với điều kiện đo cụ thể trong `NFR-004`.
- **F-016**: Đã sửa ánh xạ FSD trong `rtm.md`, thêm `location_permission` vào `SCR-TRIP-01` và cập nhật `Status: SUBMITTED`, `Run ID: cot-moc-mvp-v3`.
- **F-017**: Đã quy định bỏ qua nhắc nhở trước 10 phút nếu `deadline_at - now <= 10 phút` và hiện toast trực tiếp (`FR-008`).
