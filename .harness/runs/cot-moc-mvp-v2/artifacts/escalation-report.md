# Escalation Report: BA_SA Review Loop Ceiling Reached

## Metadata
- **Run ID**: `cot-moc-mvp-v2`
- **Loop**: `BA_SA` (Round 2 of 2)
- **Date**: `2026-11-25`
- **Author**: `sdlc-ba-analysis`
- **Target Phase**: `SA_DESIGN` (blocked at `SA_REVIEW`)

---

## 1. Disagreement & Review History
- **Round 1 (`PUSHBACK`)**: 16 findings (`ARC-001`..`ARC-016`: 1 BLOCKER, 9 HIGH, 5 MEDIUM, 1 LOW). All 16 findings were addressed in `BA_REWORK` (`FR-014`, `NFR-004`, 11 screens in `fsd.md`, full data dictionary and API catalogue).
- **Round 2 (`ESCALATE`)**: Coverage is 100% (12/12 in-scope traced, 6/18 Phase 2 excluded with user confirmation, 0 uncovered). `ARC-002..ARC-016` were substantially resolved, leaving 5 HIGH findings (`F-001`..`F-005`) and 12 MEDIUM/LOW findings (`F-006`..`F-017`) before `SA_DESIGN`.

---

## 2. Root Cause Summary of Remaining 5 HIGH Findings
1. **`F-001` (SOS & Safety-Timer Lifecycle)**: Missing `GET /api/v1/sos/active` and `GET /api/v1/safety-timers/active` for timer-triggered SOS discovery, missing max 1 `ACTIVE` SOS rule and auto-expiry lifetime, unused `CANCELLED` state, undefined offline check-in/extend queue, and atomic deadline compare-and-set semantics.
2. **`F-002` (Online Channel & Deferred Offline SOS)**: `PushAdapter` lacks device token registration (`tbl_device_tokens`, `POST /api/v1/devices`) and `+84` normalization on contact phones; deferred `triggered_offline = true` SOS needs explicit follow-up alert or local-resolve skip rules.
3. **`F-003` (NFR-001 vs FR-006 Latency Conflict)**: `POST /api/v1/sos/trigger` cannot guarantee `p95 < 300ms` if it synchronously calls external SMS/Push gateways (5000ms timeout); notification dispatch should be asynchronous (`delivery_status = PENDING` on `201`).
4. **`F-004` (FR-013 Trim Boundary)**: `effective_trim = 0.25 * distance_km` when `distance_km < 2 * privacy_trim_km` leaves 0 km drawn at `distance_km = 2.00` (with 1 km trim); should be `effective_trim = min(privacy_trim_km, 0.25 * distance_km)` per end.
5. **`F-005` (FSD Completeness)**: Error-code mapping covers 10/28 codes; `SCR-TRIP-02` and `SCR-TRIP-03` need explicit States & Data Contracts; `SCR-TRIP-01` needs Start/Pause/Resume/End control entries.

---

## 3. Remediation Options for Human Decision
- **Option A — `GRANT_EXTENSION` (Recommended)**: Grant 1 retry extension to `BA_REWORK` so BA can cleanly resolve `F-001..F-017` (especially the 5 HIGH items: async SOS dispatch, active SOS/timer GET endpoints, `min(trim, 0.25 * distance)`, full 28-code FSD mapping, and removing/specifying Push) before `SA_DESIGN`.
- **Option B — `ACCEPT_RISK`**: Waive the remaining findings and advance directly to `SA_DESIGN` (SA will have to resolve the lifecycle & async dispatch gaps during architecture design).
- **Option C — `REJECT_AND_CLOSE`**: Terminate the run.
