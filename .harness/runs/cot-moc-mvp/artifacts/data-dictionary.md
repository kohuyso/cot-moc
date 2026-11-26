# Business Data Dictionary: Cột Mốc MVP

## Metadata
- **System**: Cột Mốc (`cot-moc`)
- **Module**: `auth_profile`, `sos_safety`, `trip_journal`
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`
- **Standard Conformance**: `ISO/IEC 11179-3:2023 & ISO/IEC/IEEE 29148:2018`

---

## 1. Domain Entities & Bounded Contexts

| Bounded Context | Entity Name | Database Table | Primary Key | Description & Business Purpose |
|---|---|---|---|---|
| `AuthProfile` | `User` | `tbl_users` | `user_id (UUID)` | Tài khoản người dùng đăng nhập bằng SĐT hoặc Email. |
| `AuthProfile` | `EmergencyContact` | `tbl_emergency_contacts` | `contact_id (UUID)` | Danh bạ người thân khẩn cấp (tối đa 5 liên hệ/user). |
| `AuthProfile` | `EmergencyCard` | `tbl_emergency_cards` | `card_id (UUID)` | Thẻ thông tin y tế và phương tiện đính kèm khi phát SOS. |
| `SosSafety` | `SosSession` | `tbl_sos_sessions` | `sos_id (UUID)` | Phiên cảnh báo khẩn cấp kèm `tracking_token` công khai. |
| `SosSafety` | `SafetyTimer` | `tbl_safety_timers` | `timer_id (UUID)` | Bộ đếm hẹn giờ check-in an toàn (Dead Man's Switch). |
| `TripJournal` | `Trip` | `tbl_trips` | `trip_id (UUID)` | Chuyến đi phượt với trạng thái, quãng đường và thời gian. |
| `TripJournal` | `TripBreadcrumb` | `tbl_trip_breadcrumbs` | `breadcrumb_id (UUID)` | Tọa độ GPS ghi nhận nền trong chuyến đi. |
| `TripJournal` | `TripCheckin` | `tbl_trip_checkins` | `checkin_id (UUID)` | Điểm check-in ảnh (đã gắn watermark) và ghi chú. |

---

## 2. Logical Data Dictionary

### 2.1 `User` (`tbl_users`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `UserId` | `user_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh duy nhất tài khoản |
| `Phone` | `phone` | `VARCHAR` | 20 | Yes | **UK** | `NULL` | SĐT chuẩn E.164 (`+84...`), bắt buộc nếu `email` null |
| `Email` | `email` | `VARCHAR` | 255 | Yes | **UK** | `NULL` | Email chữ thường, bắt buộc nếu `phone` null |
| `PasswordHash` | `password_hash` | `VARCHAR` | 255 | No | None | - | Mật khẩu băm bcrypt/argon2 |
| `FullName` | `full_name` | `VARCHAR` | 100 | No | None | - | Tên hiển thị |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm tạo UTC |

### 2.2 `EmergencyContact` (`tbl_emergency_contacts`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `ContactId` | `contact_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh liên hệ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Tham chiếu `tbl_users.user_id` |
| `Name` | `name` | `VARCHAR` | 100 | No | None | - | Tên người thân |
| `Phone` | `phone` | `VARCHAR` | 20 | No | None | - | SĐT nhận SMS/thông báo |
| `Relationship` | `relationship` | `VARCHAR` | 50 | No | None | - | Mối quan hệ (Bố/Mẹ, Vợ/Chồng...) |
| `ClientId` | `client_id` | `UUID` | 16B | Yes | **UK** | `NULL` | Khóa idempotent khi đồng bộ offline |

### 2.3 `EmergencyCard` (`tbl_emergency_cards`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `CardId` | `card_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh thẻ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, UK** | - | 1-1 với `tbl_users.user_id` |
| `BloodType` | `blood_type` | `VARCHAR` | 10 | No | None | `'UNKNOWN'` | `{A+,A-,B+,B-,AB+,AB-,O+,O-,UNKNOWN}` |
| `DrugAllergies` | `drug_allergies` | `VARCHAR` | 500 | Yes | None | `NULL` | Dị ứng thuốc |
| `MedicalConditions` | `medical_conditions` | `VARCHAR` | 500 | Yes | None | `NULL` | Bệnh nền |
| `VehiclePlate` | `vehicle_plate` | `VARCHAR` | 20 | Yes | None | `NULL` | Biển số xe |
| `VehicleModel` | `vehicle_model` | `VARCHAR` | 100 | Yes | None | `NULL` | Loại xe / mẫu xe |

### 2.4 `SosSession` (`tbl_sos_sessions`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `SosId` | `sos_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh phiên SOS |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Người phát SOS |
| `TrackingToken` | `tracking_token` | `VARCHAR` | 64 | No | **UK** | - | Token 32-byte URL-safe cho web tracking |
| `Status` | `status` | `VARCHAR` | 20 | No | **IDX** | `'ACTIVE'` | `ACTIVE` \| `RESOLVED` \| `CANCELLED` |
| `TriggerSource` | `trigger_source` | `VARCHAR` | 24 | No | None | `'MANUAL_BUTTON'` | `MANUAL_BUTTON` \| `DEAD_MAN_SWITCH` |
| `Latitude` | `latitude` | `DOUBLE` | 8B | No | None | - | Vĩ độ cuối cùng |
| `Longitude` | `longitude` | `DOUBLE` | 8B | No | None | - | Kinh độ cuối cùng |
| `BatteryLevel` | `battery_level` | `INTEGER` | 4B | No | None | - | Phần trăm pin (`0..100`) |
| `ExpiresAt` | `expires_at` | `TIMESTAMPTZ` | 8B | Yes | None | `NULL` | `ended_at + 24h` khi kết thúc |

### 2.5 `SafetyTimer` (`tbl_safety_timers`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `TimerId` | `timer_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh hẹn giờ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Chủ sở hữu timer |
| `DeadlineAt` | `deadline_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | - | Mốc giờ phải check-in an toàn |
| `Status` | `status` | `VARCHAR` | 24 | No | **IDX** | `'ARMED'` | `ARMED` \| `CHECKED_IN` \| `EXPIRED_ALERTED` \| `CANCELLED` |
| `LastLatitude` | `last_latitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Vĩ độ gần nhất trước deadline |
| `LastLongitude` | `last_longitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Kinh độ gần nhất trước deadline |

### 2.6 `Trip`, `TripBreadcrumb`, `TripCheckin`
- **`tbl_trips`**: `trip_id (PK)`, `user_id (FK)`, `client_id (UK)`, `title (VARCHAR 120)`, `status (ACTIVE|PAUSED|COMPLETED)`, `distance_km (DECIMAL 10,2)`, `duration_seconds (INT)`, `started_at`, `ended_at`.
- **`tbl_trip_breadcrumbs`**: `breadcrumb_id (PK)`, `trip_id (FK)`, `client_id (UK)`, `latitude (DOUBLE)`, `longitude (DOUBLE)`, `altitude_m (DOUBLE NULL)`, `speed_kmh (DOUBLE NULL)`, `accuracy_m (DOUBLE)`, `battery_level (INT)`, `recorded_at (TIMESTAMPTZ)`.
- **`tbl_trip_checkins`**: `checkin_id (PK)`, `trip_id (FK)`, `client_id (UK)`, `latitude (DOUBLE)`, `longitude (DOUBLE)`, `altitude_m (DOUBLE NULL)`, `location_name (VARCHAR 200 NULL)`, `note (VARCHAR 500 NULL)`, `image_path (VARCHAR 500)`, `captured_at (TIMESTAMPTZ)`.

---

## 3. Permissible Value Sets & Business Integrity Rules
- **INV-DAT-001**: Mỗi `user_id` chỉ có tối đa 5 bản ghi trong `tbl_emergency_contacts`.
- **INV-DAT-002**: Mỗi `user_id` chỉ có tối đa 1 bản ghi trong `tbl_trips` ở trạng thái `ACTIVE` hoặc `PAUSED`.
- **INV-DAT-003**: Toàn bộ đồng bộ từ Mobile lên Backend sử dụng `client_id` để đảm bảo idempotency (`ON CONFLICT (client_id) DO NOTHING`).
