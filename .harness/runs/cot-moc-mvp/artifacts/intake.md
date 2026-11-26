# SDLC Intake: Cột Mốc MVP (Phase 1: REQ-001 to REQ-012)

## Metadata
- **Run ID**: `cot-moc-mvp`
- **Date**: `2026-11-25`
- **Intake Author**: `sdlc-intake`
- **Target Project**: `c:\Users\JustHuy\Personal\cot-moc` (Cột Mốc / `cot-moc`)
- **Status**: `ACCEPTED`

## 1. Raw User Request
```text
docs/URD.md - Phase 1 (REQ-001 den REQ-012)
```

## 2. Business Context & Problem Statement
- **Background**: Travelers and motorbike backpackers ("người đi phượt") frequently ride through remote areas with unstable or no cellular coverage. They need a reliable survival safety mechanism (SOS alerting, offline SMS fallback, dead man's switch, live tracking for relatives) combined with a trip journal (offline-capable photo check-ins, route tracking, and shareable trip summary posters).
- **Stakeholders**:
  - **Primary End Users**: Motorbike travelers / backpackers using the mobile app.
  - **Secondary End Users**: Emergency contacts / relatives viewing live SOS tracking via web link or receiving SMS/push alerts.
  - **Project Owner / Maintainers**: `cot-moc` engineering team.
- **Expected Business Outcome**: Deliver the Phase 1 MVP covering user account & emergency profile, core SOS & live web tracking, and trip journaling & export, establishing an offline-first mobile app and FastAPI backend foundation.

## 3. Scope Boundary (Initial)
- **In-Scope** (Phase 1 MVP from `docs/URD.md`):
  - **Account & Emergency Profile**:
    - `REQ-001`: Registration / login via phone number or email with secure on-device session persistence.
    - `REQ-002`: Emergency contacts CRUD (up to 5 contacts: Name, Phone, Relationship).
    - `REQ-003`: Medical & vehicle info card (blood type, drug allergies, underlying conditions, license plate, vehicle type) attached to SOS alerts.
  - **Safety & Emergency Alerts (Core SOS)**:
    - `REQ-004`: One-touch SOS button on home screen (3-second press-and-hold to trigger + 5-second cancel countdown).
    - `REQ-005`: Multi-channel alert & SMS fallback (online: FastAPI push/notification with GPS, battery %, last updated time, web tracking link; offline: auto-fallback to SMS with Google Maps GPS link, battery %, and emergency info to emergency contacts).
    - `REQ-006`: Live web tracking page served by FastAPI via temporary session token URL (public, no app install required for relatives, showing last location, SOS status, battery, recent breadcrumb trail).
    - `REQ-007`: Safety check-in timer (Dead Man's Switch) that triggers alert with last known GPS if user does not confirm "I am safe" before deadline.
    - `REQ-008`: Background breadcrumb trail recording during active trip (battery-optimized frequency, local storage, sync to server when online).
  - **Trip Journal & Sharing**:
    - `REQ-009`: Trip management (Start / Pause / End trip; trip history list with total distance in `km` and duration).
    - `REQ-010`: Map check-in with photo + note at current GPS; offline queue with automatic sync when online.
    - `REQ-011`: Photo check-in watermark (location name or coordinates, altitude in `m`, capture timestamp).
    - `REQ-012`: Shareable trip summary poster export (select 2–4 highlight check-in photos, optional 1–2 km start/end privacy masking, 9:16 or 1:1 poster with drawn route + photos + total `km` + duration).
- **Explicit Non-Goals (Out-of-Scope for Phase 1)**:
  - `REQ-013` to `REQ-018` (Phase 2 features in `docs/URD.md`): Offline map/rescue package downloads, offline rescue/repair directory with community confirmation, gas station & rest stop map with low-fuel-corridor alerts, offline province boundary coloring, province memory map, and achievement stats profile (`x/63` provinces, max elevation, total days).

## 4. Known Constraints & Dependencies
- **Technical Constraints**:
  - **Mobile App** (`mobile/`): React Native with TypeScript, offline-first local storage (`npm test`, `npm run typecheck`, `npm run lint`).
  - **Backend & Web Tracking** (`backend/`): FastAPI (Python), REST API for data sync, multi-channel alerting, and lightweight web tracking page (`pytest`, `python -m compileall .`).
  - **UI**: `has_ui: true` (requires UI prototype/design verification in the SDLC pipeline).
- **Security & Compliance Requirements**:
  - Secure on-device session storage (`REQ-001`).
  - Temporary session token URL for public web tracking (`REQ-006`) to prevent unauthorized persistent access to user location.
  - Optional 1–2 km start/end route masking on exported trip posters (`REQ-012`) to protect home/private addresses.
- **Target Systems / Repositories**:
  - Single repository `cot-moc` with `backend/` and `mobile/` components (currently greenfield `new_build` with `docs/URD.md` and `.harness.yaml` initialized).

## 5. Intake Clarifications & Open Questions
- **Q-001**: Authentication mechanism for `REQ-001` (phone OTP vs. password-based login for phone/email) — *Status: Open (to be specified in BA_DRAFT)*
- **Q-002**: Offline SMS fallback behavior on iOS/Android (`REQ-005`) — OS-native SMS composer vs. background SMS permission on Android — *Status: Open (to be specified in BA_DRAFT)*
- **Q-003**: Temporary tracking token expiration / revocation policy (`REQ-006`) — *Status: Open (to be specified in BA_DRAFT)*

## 6. Downstream Handoff Recommendation
- **Recommended Path**: `STANDARD_SDLC` (Feature/Change — Phase 1 MVP greenfield build across `backend` and `mobile`)
- **Next Role**: `sdlc-ba-analysis`
- **Handoff Artifact**: `artifacts/intake.md`
