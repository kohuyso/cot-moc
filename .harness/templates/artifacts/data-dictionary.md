# Business Data Dictionary: [System / Module Name]

## Metadata
- **System**: [System Name]
- **Module**: [Module Name]
- **Date**: [YYYY-MM-DD]
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`
- **Standard Conformance**: `ISO/IEC 11179-3:2023 (Metadata Registry) & ISO/IEC/IEEE 29148:2018 §9.5.3.4`

---

## 1. Domain Entities & Bounded Contexts (ISO/IEC 11179 §6)

| Bounded Context | Entity Name | Database Table | Primary Key | Description & Business Purpose |
|---|---|---|---|---|
| `TripManagement` | `TripRequest` | `tbl_trip_request` | `request_id (UUID)` | Core aggregate root representing travel authorization lifecycle. |
| `TripManagement` | `TripLeg` | `tbl_trip_leg` | `leg_id (UUID)` | Individual travel segment with origin, destination, and schedule. |
| `ExpensePolicy` | `PolicyRate` | `tbl_policy_rate` | `rate_id (BIGINT)` | Versioned cost threshold parameters by CTTV and employee grade. |

---

## 2. Logical Data Dictionary (Entity Attribute Specifications)

### 2.1 Entity: `TripRequest` (`tbl_trip_request`)
| Attribute Name | Physical Column | Data Type | Length / Precision | Nullable | Key Type | Default Value | Business Definition & Domain Constraints | Authoritative Source |
|---|---|---|---|---|---|---|---|---|
| `RequestId` | `request_id` | `UUID` | 16 bytes | No | **PK** | `gen_random_uuid()` | Immutable unique identifier for the trip request | Local System |
| `RequestNumber` | `request_num` | `VARCHAR` | 32 | No | **UK** | Auto-sequence | Permanent human-readable code (`TRP-YYYY-XXXXX`). Never reused | Local System |
| `CompanyCode` | `cttv_code` | `VARCHAR` | 16 | No | **FK, IDX** | - | Multi-tenancy partition key. Maps to corporate CTTV list | Corporate IAM / HR |
| `RequesterId` | `requester_id` | `VARCHAR` | 64 | No | **FK, IDX** | - | Corporate SSO User ID of the creator | Corporate SSO |
| `StatusCode` | `status_code` | `VARCHAR` | 24 | No | **IDX** | `'DRAFT'` | Finite state machine code (see §3 Permissible Value Sets) | Local System |
| `EstimatedAmount`| `est_amount` | `DECIMAL` | (18, 2) | No | None | `0.00` | Sum of policy-based estimated expenses in base currency | Calculated |
| `PolicyVersion` | `policy_ver` | `VARCHAR` | 16 | No | None | - | Snapshot of policy version applied at time of submission | Policy Module |
| `IsDeleted` | `is_deleted` | `BOOLEAN` | 1 byte | No | None | `false` | Soft-delete flag; records retain for 10-year audit compliance | System Audit |
| `CreatedAt` | `created_at` | `TIMESTAMPTZ`| 8 bytes | No | None | `CURRENT_TIMESTAMP` | UTC creation timestamp | System Clock |

---

## 3. Permissible Value Sets (Enumerations & Lookup Sets) (ISO/IEC 11179 §8)

### 3.1 Enumeration: `TripStatusCode`
| Code | Display Label (VI) | Business Semantics | Permitted Next States |
|---|---|---|---|
| `DRAFT` | Bản nháp | Initial editable state by requester | `SUBMITTED`, `CANCELLED` |
| `PENDING_STEP1` | Chờ quản lý duyệt | Routed to direct manager based on org hierarchy | `PENDING_FINAL`, `REJECTED` |
| `PENDING_FINAL` | Chờ duyệt cấp cao | Awaiting financial or division director approval | `APPROVED`, `REJECTED` |
| `APPROVED` | Đã phê duyệt | Final approval committed; budget hold active | `IN_PROGRESS`, `CANCELLED` |
| `SETTLING` | Đang quyết toán | Post-trip expense reconciliation in progress | `CLOSED` |
| `CLOSED` | Đã hoàn tất | Financial settlement completed and archived | None (Terminal) |
| `REJECTED` | Bị từ chối | Rejected by approver; editable for re-submission | `SUBMITTED`, `CANCELLED` |

---

## 4. Business Integrity Rules & Relational Invariants (ISO 29148 §9.5.3.4)

- **INV-DAT-001 (Permanent Identity)**: `request_num` is permanently immutable and MUST never be recycled, even after hard deletion or archive.
- **INV-DAT-002 (Multi-Tenancy Isolation)**: All persistent queries, joins, and report views MUST include `cttv_code` filter at the database or ORM level.
- **INV-DAT-003 (Policy Snapshot Integrity)**: When `status_code` moves from `DRAFT` to `PENDING_STEP1`, the active policy version and currency exchange rate MUST be snapshotted; subsequent rate changes MUST NOT alter existing trip estimates.
- **INV-DAT-004 (Audit Trail Invariant)**: Audit records are append-only. Application identities are explicitly denied `UPDATE` or `DELETE` permissions on ledger tables.
