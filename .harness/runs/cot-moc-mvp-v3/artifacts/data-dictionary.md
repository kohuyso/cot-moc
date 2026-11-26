# Business Data Dictionary: Cột Mốc MVP

## Metadata
- **Run ID**: `cot-moc-mvp-v3`
- **System**: Cột Mốc (`cot-moc`)
- **Module**: `auth_profile`, `sos_safety`, `trip_journal`
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`
- **Status**: `SUBMITTED`
- **Standard Conformance**: `ISO/IEC 11179-3:2023 & ISO/IEC/IEEE 29148:2018`

---

## 1. Domain Entities & Bounded Contexts

| Bounded Context | Entity Name | Database Table | Primary Key | Description & Business Purpose |
|---|---|---|---|---|
| `AuthProfile` | `User` | `tbl_users` | `user_id (UUID)` | Tài khoản người dùng đăng nhập bằng SĐT hoặc Email. |
| `AuthProfile` | `RefreshToken` | `tbl_refresh_tokens` | `token_id (UUID)` | Quản lý refresh token và thu hồi phiên đăng nhập. |
| `AuthProfile` | `EmergencyContact` | `tbl_emergency_contacts` | `contact_id (UUID)` | Danh bạ người thân khẩn cấp (tối đa 5 liên hệ/user). |
| `AuthProfile` | `EmergencyCard` | `tbl_emergency_cards` | `card_id (UUID)` | Thẻ thông tin y tế và phương tiện đính kèm khi phát SOS. |
| `SosSafety` | `SosSession` | `tbl_sos_sessions` | `sos_id (UUID)` | Phiên cảnh báo khẩn cấp kèm `tracking_token` công khai. |
| `SosSafety` | `SosLocation` | `tbl_sos_locations` | `location_id (UUID)` | Lịch sử cập nhật vị trí/pin khi phiên SOS đang ACTIVE. |
| `SosSafety` | `SafetyTimer` | `tbl_safety_timers` | `timer_id (UUID)` | Bộ đếm hẹn giờ check-in an toàn (Dead Man's Switch). |
| `TripJournal` | `Trip` | `tbl_trips` | `trip_id (UUID)` | Chuyến đi phượt với trạng thái, quãng đường và thời gian. |
| `TripJournal` | `TripBreadcrumb` | `tbl_trip_breadcrumbs` | `breadcrumb_id (UUID)` | Tọa độ GPS ghi nhận nền trong chuyến đi. |
| `TripJournal` | `TripCheckin` | `tbl_trip_checkins` | `checkin_id (UUID)` | Điểm check-in ảnh (đã gắn watermark) và ghi chú. |

---

## 2. Logical Data Dictionary (Backend Database)

### 2.1 `User` (`tbl_users`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `UserId` | `user_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh duy nhất tài khoản |
| `Phone` | `phone` | `VARCHAR` | 20 | Yes | **UK** | `NULL` | SĐT chuẩn E.164 (`+84...`), bắt buộc nếu `email` null |
| `Email` | `email` | `VARCHAR` | 255 | Yes | **UK** | `NULL` | Email chữ thường, bắt buộc nếu `phone` null |
| `PasswordHash` | `password_hash` | `VARCHAR` | 255 | No | None | - | Mật khẩu băm bcrypt/argon2 |
| `FullName` | `full_name` | `VARCHAR` | 100 | No | None | - | Tên hiển thị |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm tạo UTC |

### 2.2 `RefreshToken` (`tbl_refresh_tokens`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `TokenId` | `token_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh token |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Tham chiếu `tbl_users.user_id` |
| `TokenHash` | `token_hash` | `VARCHAR` | 255 | No | **UK** | - | SHA-256 hash của refresh token |
| `ExpiresAt` | `expires_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | - | Thời điểm hết hạn (30 ngày) |
| `RevokedAt` | `revoked_at` | `TIMESTAMPTZ` | 8B | Yes | None | `NULL` | Thời điểm thu hồi khi đăng xuất |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm cấp |

### 2.3 `EmergencyContact` (`tbl_emergency_contacts`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `ContactId` | `contact_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh liên hệ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Tham chiếu `tbl_users.user_id` |
| `Name` | `name` | `VARCHAR` | 100 | No | None | - | Tên người thân |
| `Phone` | `phone` | `VARCHAR` | 20 | No | None | - | SĐT chuẩn hóa E.164 (`+84...`) |
| `Relationship` | `relationship` | `VARCHAR` | 50 | No | None | - | Mối quan hệ |
| `ClientId` | `client_id` | `UUID` | 16B | Yes | **UK(user_id, client_id)** | `NULL` | Khóa idempotent theo từng user |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm tạo |

### 2.4 `EmergencyCard` (`tbl_emergency_cards`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `CardId` | `card_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh thẻ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, UK** | - | 1-1 với `tbl_users.user_id` |
| `BloodType` | `blood_type` | `VARCHAR` | 10 | No | None | `'UNKNOWN'` | `{A+,A-,B+,B-,AB+,AB-,O+,O-,UNKNOWN}` |
| `DrugAllergies` | `drug_allergies` | `VARCHAR` | 500 | Yes | None | `NULL` | Dị ứng thuốc |
| `MedicalConditions` | `medical_conditions` | `VARCHAR` | 500 | Yes | None | `NULL` | Bệnh nền |
| `VehiclePlate` | `vehicle_plate` | `VARCHAR` | 20 | Yes | None | `NULL` | Biển số xe |
| `VehicleModel` | `vehicle_model` | `VARCHAR` | 100 | Yes | None | `NULL` | Loại xe / mẫu xe |
| `UpdatedAt` | `updated_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm cập nhật cuối |

### 2.5 `SosSession` (`tbl_sos_sessions`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `SosId` | `sos_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh phiên SOS |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Tối đa 1 phiên `ACTIVE`/user |
| `TripId` | `trip_id` | `UUID` | 16B | Yes | **FK, IDX** | `NULL` | Chuyến đi đang chạy (nếu có) |
| `ClientId` | `client_id` | `UUID` | 16B | Yes | **UK(user_id, client_id)** | `NULL` | Khóa idempotent theo từng user |
| `TrackingToken` | `tracking_token` | `VARCHAR` | 64 | No | **UK** | - | Token 32-byte URL-safe |
| `Status` | `status` | `VARCHAR` | 20 | No | **IDX** | `'ACTIVE'` | `ACTIVE` \| `RESOLVED` |
| `TriggerSource` | `trigger_source` | `VARCHAR` | 24 | No | None | `'MANUAL_BUTTON'` | `MANUAL_BUTTON` \| `DEAD_MAN_SWITCH` |
| `DeliveryStatus` | `delivery_status` | `VARCHAR` | 24 | No | None | `'PENDING'` | `PENDING` \| `SENT` \| `PARTIAL_FAILED` \| `FAILED` \| `SKIPPED` |
| `Latitude` | `latitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Null nếu `location_unavailable = true` |
| `Longitude` | `longitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Null nếu `location_unavailable = true` |
| `IsStaleLocation` | `is_stale_location` | `BOOLEAN` | 1B | No | None | `false` | `true` nếu dùng last known GPS |
| `LocationUnavailable` | `location_unavailable` | `BOOLEAN` | 1B | No | None | `false` | `true` nếu chưa từng có GPS |
| `BatteryLevel` | `battery_level` | `INTEGER` | 4B | No | None | - | Phần trăm pin (`0..100`) |
| `StartedAt` | `started_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm kích hoạt SOS |
| `UpdatedAt` | `updated_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm cập nhật vị trí cuối |
| `EndedAt` | `ended_at` | `TIMESTAMPTZ` | 8B | Yes | None | `NULL` | Thời điểm kết thúc (`RESOLVED` hoặc auto-resolve 72h) |
| `RevokedAt` | `revoked_at` | `TIMESTAMPTZ` | 8B | Yes | None | `NULL` | Thời điểm chủ tài khoản thu hồi link |
| `ExpiresAt` | `expires_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | `started_at + 96h` | `ended_at + 24h` (hoặc `revoked_at`, tối đa 72h ACTIVE + 24h) |

### 2.6 `SosLocation` (`tbl_sos_locations`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `LocationId` | `location_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh điểm vị trí SOS |
| `SosId` | `sos_id` | `UUID` | 16B | No | **FK, IDX** | - | Tham chiếu `tbl_sos_sessions.sos_id` |
| `Latitude` | `latitude` | `DOUBLE` | 8B | No | None | - | Vĩ độ |
| `Longitude` | `longitude` | `DOUBLE` | 8B | No | None | - | Kinh độ |
| `BatteryLevel` | `battery_level` | `INTEGER` | 4B | No | None | - | % pin tại thời điểm heartbeat |
| `RecordedAt` | `recorded_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | - | Index `(sos_id, recorded_at)` |

### 2.7 `SafetyTimer` (`tbl_safety_timers`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `TimerId` | `timer_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh hẹn giờ |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Tối đa 1 timer `ARMED`/user |
| `SosId` | `sos_id` | `UUID` | 16B | Yes | **FK** | `NULL` | Phiên SOS tạo ra nếu timer quá hạn |
| `DeadlineAt` | `deadline_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | - | Index `(status, deadline_at)` |
| `Note` | `note` | `VARCHAR` | 200 | Yes | None | `NULL` | Ghi chú lộ trình dự kiến |
| `Status` | `status` | `VARCHAR` | 24 | No | **IDX** | `'ARMED'` | `ARMED` \| `CHECKED_IN` \| `EXPIRED_ALERTED` \| `CANCELLED` |
| `LastLatitude` | `last_latitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Vĩ độ gần nhất trước deadline |
| `LastLongitude` | `last_longitude` | `DOUBLE` | 8B | Yes | None | `NULL` | Kinh độ gần nhất trước deadline |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm đặt timer |
| `UpdatedAt` | `updated_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm cập nhật cuối |

### 2.8 `Trip` (`tbl_trips`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `TripId` | `trip_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh chuyến đi |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Chủ sở hữu chuyến đi |
| `ClientId` | `client_id` | `UUID` | 16B | Yes | **UK(user_id, client_id)** | `NULL` | Khóa idempotent theo từng user |
| `Title` | `title` | `VARCHAR` | 120 | No | None | `'Chuyến đi...'` | Tên chuyến đi |
| `Status` | `status` | `VARCHAR` | 20 | No | **IDX** | `'ACTIVE'` | `ACTIVE` \| `PAUSED` \| `COMPLETED` |
| `DistanceKm` | `distance_km` | `DECIMAL` | (10,2) | No | None | `0.00` | Tổng quãng đường Haversine (`km`) |
| `DurationSeconds` | `duration_seconds` | `INTEGER` | 4B | No | None | `0` | Thời gian di chuyển (không tính `PAUSED`) |
| `StartedAt` | `started_at` | `TIMESTAMPTZ` | 8B | No | None | `CURRENT_TIMESTAMP` | Thời điểm bắt đầu |
| `EndedAt` | `ended_at` | `TIMESTAMPTZ` | 8B | Yes | None | `NULL` | Thời điểm kết thúc |

### 2.9 `TripBreadcrumb` (`tbl_trip_breadcrumbs`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `BreadcrumbId` | `breadcrumb_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh điểm breadcrumb |
| `TripId` | `trip_id` | `UUID` | 16B | No | **FK, IDX** | - | Index `(trip_id, recorded_at)` |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Chủ sở hữu (phục vụ idempotency) |
| `ClientId` | `client_id` | `UUID` | 16B | No | **UK(user_id, client_id)** | - | Khóa idempotent theo từng user |
| `Latitude` | `latitude` | `DOUBLE` | 8B | No | None | - | Vĩ độ (`-90..90`) |
| `Longitude` | `longitude` | `DOUBLE` | 8B | No | None | - | Kinh độ (`-180..180`) |
| `AltitudeM` | `altitude_m` | `DOUBLE` | 8B | Yes | None | `NULL` | Độ cao (`m`) |
| `SpeedKmh` | `speed_kmh` | `DOUBLE` | 8B | Yes | None | `NULL` | Vận tốc (`km/h`) |
| `AccuracyM` | `accuracy_m` | `DOUBLE` | 8B | No | None | - | Sai số GPS (`<= 100m`) |
| `BatteryLevel` | `battery_level` | `INTEGER` | 4B | No | None | - | % pin (`0..100`) |
| `RecordedAt` | `recorded_at` | `TIMESTAMPTZ` | 8B | No | **IDX** | - | Thời điểm ghi nhận |

### 2.10 `TripCheckin` (`tbl_trip_checkins`)
| Attribute Name | Physical Column | Data Type | Length | Nullable | Key | Default | Business Definition & Constraints |
|---|---|---|---|---|---|---|---|
| `CheckinId` | `checkin_id` | `UUID` | 16B | No | **PK** | `gen_random_uuid()` | Định danh check-in |
| `TripId` | `trip_id` | `UUID` | 16B | No | **FK, IDX** | - | Tham chiếu `tbl_trips.trip_id` |
| `UserId` | `user_id` | `UUID` | 16B | No | **FK, IDX** | - | Chủ sở hữu |
| `ClientId` | `client_id` | `UUID` | 16B | No | **UK(user_id, client_id)** | - | Khóa idempotent theo từng user |
| `Latitude` | `latitude` | `DOUBLE` | 8B | No | None | - | Vĩ độ |
| `Longitude` | `longitude` | `DOUBLE` | 8B | No | None | - | Kinh độ |
| `IsStaleLocation` | `is_stale_location` | `BOOLEAN` | 1B | No | None | `false` | `true` nếu dùng last known GPS |
| `AltitudeM` | `altitude_m` | `DOUBLE` | 8B | Yes | None | `NULL` | Độ cao (`m`) |
| `LocationName` | `location_name` | `VARCHAR` | 200 | Yes | None | `NULL` | Tên địa điểm hoặc `NULL` nếu offline |
| `Note` | `note` | `VARCHAR` | 500 | Yes | None | `NULL` | Ghi chú của người dùng |
| `ImagePath` | `image_path` | `VARCHAR` | 500 | No | None | - | Đường dẫn tệp ảnh đã gắn watermark |
| `CapturedAt` | `captured_at` | `TIMESTAMPTZ` | 8B | No | None | - | Thời điểm chụp (EXIF hoặc thiết bị) |

---

## 3. Mobile SQLite Local Schema & Sync Columns
Mỗi bảng đồng bộ trên SQLite (`local_emergency_contacts`, `local_emergency_card`, `local_sos_sessions`, `local_safety_timers`, `local_trips`, `local_trip_breadcrumbs`, `local_trip_checkins`) bổ sung 3 cột:
- `client_id` (`TEXT UNIQUE NOT NULL`): UUIDv4 sinh tại thiết bị.
- `sync_status` (`TEXT NOT NULL DEFAULT 'PENDING'`): `'PENDING' | 'SYNCED' | 'FAILED_PERMANENT'`.
- `last_sync_error` (`TEXT NULL`): Mã lỗi HTTP 4xx nếu bị từ chối vĩnh viễn.

---

## 4. Business Integrity Rules & Relational Invariants
- **INV-DAT-001**: Mỗi `user_id` chỉ có tối đa 5 bản ghi trong `tbl_emergency_contacts`.
- **INV-DAT-002**: Mỗi `user_id` chỉ có tối đa 1 bản ghi `ACTIVE`/`PAUSED` trong `tbl_trips`, 1 bản ghi `ARMED` trong `tbl_safety_timers`, và 1 bản ghi `ACTIVE` trong `tbl_sos_sessions`.
- **INV-DAT-003**: Toàn bộ đồng bộ từ Mobile lên Backend sử dụng khóa duy nhất `(user_id, client_id)` (`ON CONFLICT (user_id, client_id) DO NOTHING`); khi replay trả `HTTP 200 OK` bản ghi thuộc về chính `user_id` đó.
