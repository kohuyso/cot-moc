# Requirements Traceability Matrix (RTM)

## Metadata
- **System**: Cột Mốc (`cot-moc`)
- **Run ID**: `cot-moc-mvp-v2`
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`, `sdlc-qa-review`
- **Standard Conformance**: `ISO/IEC/IEEE 29148:2018 §8.5`

---

## 1. Bi-Directional Traceability Matrix

| Source Clause (`docs/URD.md`) | Stakeholder Need | Software Requirement (SRS) | Functional Design (FSD) | Data Entity / Table | Test Case (Planned) | Implementation Artifact | Traceability Status |
|---|---|---|---|---|---|---|---|
| `REQ-001` | Đăng ký, đăng nhập SĐT/email và lưu phiên an toàn | `FR-001`, `FR-002`, `NFR-002` | `SCR-AUTH-01` | `tbl_users`, `tbl_refresh_tokens` | `planned: auth register/login/offline session` | - | Traced |
| `REQ-002` | Thêm/sửa/xóa tối đa 5 liên hệ khẩn cấp | `FR-003`, `NFR-003` | `SCR-AUTH-02`, `SCR-AUTH-03` | `tbl_emergency_contacts` | `planned: contacts CRUD & limit 5` | - | Traced |
| `REQ-003` | Lưu thẻ thông tin y tế & xe đính kèm SOS | `FR-004`, `NFR-003` | `SCR-AUTH-02` | `tbl_emergency_cards` | `planned: emergency card CRUD` | - | Traced |
| `REQ-004` | Nút SOS 1 chạm (giữ 3s + đếm ngược hủy 5s) | `FR-005`, `NFR-001` | `SCR-SOS-01` | `tbl_sos_sessions` | `planned: SOS hold 3s & cancel 5s` | - | Traced |
| `REQ-005` | Cảnh báo đa kênh Online & SMS Fallback Offline | `FR-006`, `FR-014`, `NFR-001` | `SCR-SOS-01`, `SCR-SOS-04` | `tbl_sos_sessions` | `planned: online trigger, offline SMS & deferred sync` | - | Traced |
| `REQ-006` | Trang Web theo dõi trực tiếp qua token tạm thời | `FR-007`, `FR-014`, `NFR-001`, `NFR-002` | `SCR-SOS-02`, `SCR-SOS-04` | `tbl_sos_sessions`, `tbl_sos_locations` | `planned: web tracking, heartbeat, resolve, revoke` | - | Traced |
| `REQ-007` | Hẹn giờ Check-in an toàn (Dead Man's Switch) | `FR-008`, `NFR-002` | `SCR-SOS-03` | `tbl_safety_timers` | `planned: timer arm, checkin, extend, cancel & expiry` | - | Traced |
| `REQ-008` | Lưu vết hành trình nền tối ưu pin & đồng bộ | `FR-009`, `NFR-003`, `NFR-004` | `SCR-TRIP-01` | `tbl_trip_breadcrumbs` | `planned: adaptive interval, permission & battery` | - | Traced |
| `REQ-009` | Bắt đầu/Tạm dừng/Kết thúc chuyến đi & lịch sử | `FR-010`, `NFR-003` | `SCR-TRIP-01`, `SCR-TRIP-04` | `tbl_trips` | `planned: trip lifecycle & Haversine distance` | - | Traced |
| `REQ-010` | Check-in ảnh + ghi chú gắn GPS với hàng đợi offline | `FR-011`, `NFR-003` | `SCR-TRIP-02`, `SCR-TRIP-04` | `tbl_trip_checkins` | `planned: offline checkin queue, compress & sync` | - | Traced |
| `REQ-011` | Gắn watermark địa điểm/tọa độ, độ cao, ngày giờ | `FR-012`, `NFR-003` | `SCR-TRIP-02` | `tbl_trip_checkins` | `planned: watermark format, Nominatim & null altitude` | - | Traced |
| `REQ-012` | Export poster 9:16 hoặc 1:1 che 1-2 km đầu/cuối | `FR-013`, `NFR-002` | `SCR-TRIP-03`, `SCR-TRIP-04` | `tbl_trips`, `tbl_trip_breadcrumbs`, `tbl_trip_checkins` | `planned: poster export, 25% trim cap & layout` | - | Traced |
| `REQ-013` | Tải gói Offline theo cung đường | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |
| `REQ-014` | Danh bạ cứu hộ & sửa xe dọc tuyến Offline | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |
| `REQ-015` | Bản đồ cây xăng & điểm nghỉ | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |
| `REQ-016` | Tự động tô màu tỉnh thành Offline | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |
| `REQ-017` | Bản đồ kỷ niệm theo tỉnh | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |
| `REQ-018` | Profile thống kê thành tích | - | - | - | - | - | Excluded: Phase 2 (user confirmed) |

---

## 2. Requirements Traceability Coverage Metrics

| Metric | Target | Actual (count / total) | Evaluation |
|---|---|---|---|
| **Source IDs in scope (REQ-001..REQ-012) traced to an FR** | 100% | `12 / 12` | `[x]` |
| **Source IDs excluded with a user-confirmed reason (REQ-013..REQ-018)** | listed | `6 / 18` | `[x]` |
| **FRs/NFRs with main flow, exception flow and 2+ acceptance criteria** | 100% | `18 / 18` (`FR-001..FR-014`, `NFR-001..NFR-004`) | `[x]` |
| **Out-of-scope items confirmed by the user** | 100% | `6 / 6` | `[x]` |

---

## 3. Discrepancy & Orphan Analysis
- **Unmapped Source Requirements**: None (12 traced + 6 user-confirmed excluded = 18/18 in `docs/URD.md`).
- **Orphan Functional Specifications**: None.
- **Retired / Superseded Requirements**: None.
