# Baseline Documentation Review & Gap Analysis Report

## Metadata
- **System**: [System / Product Name]
- **Run ID**: `[run-id]`
- **Date**: [YYYY-MM-DD]
- **Auditor**: `sdlc-ba-analysis`
- **Challenger / Reviewer**: `sdlc-sa-review`
- **Target Source Document**: `[URD File Name & Version, e.g. URD v1.4 (Draft)]`
- **Standard Conformance**: `ISO/IEC/IEEE 29148:2018 §6.4 (Verification & Validation) & IIBA BABOK Guide v3 §5 (Requirements Life Cycle Management)`

---

## 1. Existing Documentation Inventory (BABOK v3 §5.3)

| Asset Category | File Path / Directory | Baseline Version / Date | Scope & Depth | Status |
|---|---|---|---|---|
| **SRS** | `srs/SRS-00..12_v0.6.md` | v0.6 (2026-10-05) | 13 detailed sub-system specs (~1.1 MB) | Valid Baseline |
| **FSD** | `fsd/FSD-00..12_v0.1.md` | v0.1 (2026-10-05) | 13 comprehensive functional screen specs (~7.5 MB)| Valid Baseline |
| **Data Model / DBD**| `database/Tu-dien-du-lieu_v0.1.md` | v0.1 (2026-10-05) | 361 KB detailed table dictionary & constraints | Valid Baseline |
| **UI Prototype** | `prototype_design/index.html` | v3.0 (2026-10-05) | Full interactive HTML mockup & screen map | Valid Baseline |

---

## 2. ISO/IEC/IEEE 29148 Conformance Audit (Quality Attributes)

| Evaluation Criterion (ISO 29148 §5.2.5) | Audit Finding on Existing Baseline | Compliance Status | Required Remediation |
|---|---|---|---|
| **Completeness** | Baseline covers 11 core functional domains thoroughly; however, recent changes in URD v1.4 (attendance radius 8km, retention 2yr) are not reflected in FSD-07. | **PARTIALLY COMPLIANT** | Update FSD-07 and validation rule table. |
| **Consistency** | Conflict detected between TDD §2.5 (AuditLog as SQL ledger) and DBD-00/RTM (AuditLog as standard table with DENY permissions). | **CONFLICT IDENTIFIED** | Resolve in favor of PO-approved DBD table schema (`DB-095`). |
| **Unambiguity** | Domain terms across SRS and FSD align with glossary; no conflicting synonyms detected. | **COMPLIANT** | Maintain Glossary in `requirement-analysis.md`. |
| **Verifiability / Testability**| FSD defines concrete HTTP status codes, error messages (ERR-xxx), and boundary constraints for each input. | **COMPLIANT** | Test designer can deterministically map test cases. |
| **Traceability** | RTM_DBD.md maps requirements to database columns; cross-functional traceability matrix exists. | **COMPLIANT** | Update crosswalk with URD v1.4 clause IDs. |

---

## 3. Bi-Directional Gap Analysis (Baseline vs Target URD v1.4)

| URD v1.4 Clause / ID | Feature / Rule Description | Baseline Status | Nature of Gap | Impact & Required Action |
|---|---|---|---|---|
| `UR-FUN-GPS-001` | Geofence attendance radius default: 8 km | Baseline FSD-07 had 5 km | **MODIFIED** | Update FSD-07 validation parameter and config table default. |
| `UR-FUN-GPS-005` | Legacy office check-in method | Present in old FSD | **RETIRED** | Mark requirement as DEPRECATED; do not implement in target code. |
| `UR-FUN-TRP-009` | Google Maps distance with manual fallback | Maps disabled in v1.1 | **RESTORED** | Restore Google Maps adapter; add mandatory justification for manual distance. |
| `UR-NFR-CMP-003` | Attendance evidence retention: 2 years | Baseline had 5 years | **MODIFIED** | Update data retention lifecycle job to purge GPS coords after 24 months. |

---

## 4. Technical Conflict & Architectural Risk Register

| Risk / Conflict ID | Description | Severity | Impacted Subsystem | Resolution / Architectural Guidance |
|---|---|---|---|---|
| `CONF-01` | Synchronous payment hold vs Outbox worker | **HIGH** | `ePayment Integration` | Reject synchronous remote call inside SQL transaction; enforce Outbox pattern. |
| `CONF-02` | Offline check-in sync vs server geofence | **MEDIUM** | `Mobile Mini-App` | GPS coords must be captured with device hardware timestamp; server re-validates. |

---

## 5. Architectural Readiness & SA Handoff Verdict

- **Overall Baseline Quality**: **HIGH GRADE (A-)** — Extensive upstream investment (FSD/SRS/DBD) is complete and well-structured.
- **Readiness Verdict**: **`READY_FOR_SA_DESIGN_WITH_GAPS`**
- **Prerequisites for SA Design**:
  1. Address the 4 identified gaps from URD v1.4 during technical solution design.
  2. Adopt PO-confirmed DBD database dictionary as authoritative persistence schema.
  3. Validate ePayment Outbox boundary to prevent distributed transaction deadlocks.
