# Architecture Review - cot-moc-mvp-v2

- Reviewer: independent_sa_reviewer
- Verdict: ESCALATE (round 2)
- User intent verified: True
- Findings: 17

## Summary

Round 2 of BA_SA. Coverage is correct and matches the harness evidence: 12/18 traced, 6 excluded with user confirmation, 0 uncovered; rtm.md has 18 rows. OQ-001..OQ-004 are RESOLVED and ASM-001..ASM-006 confirmed. Headers carry run id cot-moc-mvp-v2. All 14 FRs and 4 NFRs meet the structural depth contract. Round-1 findings ARC-002..ARC-016 are substantially fixed; ARC-001 (FSD) only partly. Five HIGH findings remain: (F-001) gaps in the SOS and safety-timer lifecycle: the app cannot find or resolve an SOS created by an expired timer, an ACTIVE SOS has no maximum lifetime, nothing limits a user to one ACTIVE SOS, CANCELLED is never reached, and offline 'Toi an toan' is undefined; (F-002) the push channel cannot be built and the behaviour of a deferred offline SOS is unclear; (F-003) NFR-001 p95 < 300 ms on POST /sos/trigger conflicts with synchronous notification in the same call; (F-004) the FR-013 trim rule hides the whole route at distance = 2 x trim; (F-005) FSD error mapping covers 10 of 28 codes and the trip screens lack states, data contracts and controls. BA_SA already had one pushback round, so per sdlc-sa-review this escalates to a human decision rather than a second pushback.

## Findings

### F-001 [HIGH] requirement-depth
- Evidence: srs.md FR-008 step 4 'Scheduler server ... tu dong tao SosSession voi trigger_source = DEAD_MAN_SWITCH'; FR-014 resolve requires sos_id; integration-matrix.md 2.2 has no GET for an active SOS or active timer; data-dictionary.md 2.5 status 'ACTIVE | RESOLVED | CANCELLED' with expires_at NULL until ended_at; fsd.md 1.2 SosSession diagram has no CANCELLED transition
- Description: The SOS and safety-timer lifecycle is not closed. (a) When a timer expires the server creates a SosSession, but the app has no endpoint to learn its sos_id. The user therefore cannot resolve it or revoke its link from SCR-SOS-04, and a false alarm cannot be cleared. (b) An ACTIVE SosSession has expires_at = NULL and no maximum lifetime, so its public link and medical card (shown while ACTIVE, per OQ-004) stay live until the user acts. (c) No rule limits a user to one ACTIVE SOS, so a manual SOS plus a timer expiry, or two triggers, create duplicate sessions and duplicate alerts. (d) The server status CANCELLED, and heartbeat's ERR_SOS_NOT_ACTIVE for CANCELLED, are never reached by any flow. (e) FR-008 does not say what happens when the user presses 'Toi an toan' or extends the timer while offline, which is the normal case in no-signal areas. (f) It is not defined whether a check-in after deadline_at but before the scheduler runs (for example 18:00:10) is accepted. The FSD says '<= deadline' (time rule) while the exception is keyed on EXPIRED_ALERTED (state rule), and no atomic transition is specified.
- Required remediation: Add GET /api/v1/sos/active and GET /api/v1/safety-timers/active (or push the sos_id to the device) so the app can show and resolve a timer-created SOS. Add a rule that a user has at most one ACTIVE SosSession, with the behaviour when a timer expires during a manual SOS. Define a maximum ACTIVE lifetime or auto-expiry. Define or remove CANCELLED. Specify offline check-in and extend (local queue plus deferred POST, and what the user sees). Define deadline semantics (state-based with an atomic ARMED-to-X compare-and-set). Add acceptance criteria for each.

### F-002 [HIGH] integration
- Evidence: srs.md FR-006 step 3 'PushAdapter (neu lien he la user da dang ky)'; data-dictionary.md has no device/push-token table; integration-matrix.md 2.1 has no device-token registration endpoint; FR-003 contact phone regex '^\+?[0-9]{10,15}$' with no +84 normalisation vs FR-001 user phone normalised to +84; FR-006 alternate 'Worker dong bo gui bu POST /api/v1/sos/trigger ... de backend tao SosSession va tracking_url'
- Description: The REQ-005 online channel cannot be built from the spec. Push to a registered relative needs a device push token, a registration endpoint, a storage table and a provider (FCM/APNs); none is specified. Matching a contact to a registered user needs a phone-number rule, but contact phones are not normalised to +84 while user phones are. The SMS gateway provider is unnamed: only an adapter and mock are defined. When an offline-triggered SOS is synced later (triggered_offline = true), the spec does not say whether the backend sends relatives a new alert with the tracking_url. Nor does it say what happens if the user resolved or cancelled locally before connectivity returned. Relatives either never get the REQ-005 tracking link or get a stale, possibly false alarm.
- Required remediation: Either remove push from MVP with user confirmation, or specify the device-token entity, the POST /api/v1/devices endpoint, the provider, and the contact-to-user matching rule with E.164 normalisation of contact phones. Name the production SMS gateway, or record its selection as a confirmed assumption. Define the notification behaviour for triggered_offline = true (send a follow-up containing the tracking_url, with the message template) and for an SOS resolved locally before sync. Add acceptance criteria for each.

### F-003 [HIGH] nfr-feasibility
- Evidence: NFR-001 AC 'Gui 100 yeu cau toi ... POST /api/v1/sos/trigger -> Do tre p95 duoi 300ms'; srs.md FR-006 steps 3-4 'Backend tao SosSession ... va gui thong bao ... Tra HTTP 201 ... delivery_status'; exception 'Backend van tra HTTP 201 Created voi delivery_status = PARTIAL_FAILED'; integration-matrix.md Notification Adapter timeout 5000 ms
- Description: FR-006 returns delivery_status, including PARTIAL_FAILED, in the 201 response, which means the backend calls the notification gateway (5000 ms timeout per contact) before replying. NFR-001 requires p95 < 300 ms on the same endpoint. With up to 5 contacts and real SMS gateway latency, both cannot be met, and the test is not deterministic. A slow synchronous send also pushes the app past its own 5000 ms timeout, causing an unnecessary SMS fallback and duplicate alerts.
- Required remediation: Make notification dispatch asynchronous: POST /sos/trigger persists the session and returns 201 with delivery_status = PENDING, and the delivery result is exposed later. Alternatively, exclude /sos/trigger from the 300 ms target and set a realistic bound. Update the FR-006 flows and exception, the NFR-001 acceptance criteria and the integration matrix consistently.

### F-004 [HIGH] business-rule
- Evidence: BR-013 'Neu distance_km < 2 * privacy_trim_km thi effective_trim = 0.25 * distance_km moi dau'
- Description: The trim rule breaks at the boundary. At distance_km = 2.00 with trim 1 the condition is false, so 1 km is cut from each end and 0 km of route is drawn (the same happens for 4.00 km with trim 2). Just below the boundary (1.99 km) about 1 km is drawn. Trips from 2x to about 2.5x the trim show less route than shorter trips, and at exactly 2x the poster has no route. A tester checking the boundary would find an empty polyline that the spec says is correct.
- Required remediation: Restate the rule so some route always remains visible, for example effective_trim = min(privacy_trim_km, 0.25 * distance_km) per end. Add boundary worked examples and acceptance criteria at distance = 2 x trim and 4 x trim.

### F-005 [HIGH] fsd-completeness
- Evidence: fsd.md section 3 maps 10 codes; SRS/requirement.json define 28 (missing e.g. ERR_AUTH_SESSION_EXPIRED, ERR_NETWORK_OFFLINE, ERR_CONTACT_INVALID_PHONE, ERR_PROFILE_INVALID_BLOOD_TYPE, ERR_PROFILE_FIELD_TOO_LONG, ERR_SOS_NO_CONTACTS_OFFLINE, ERR_TRACK_TOKEN_NOT_FOUND, ERR_TIMER_INVALID_DEADLINE, ERR_LOCATION_PERMISSION_DENIED, ERR_TRIP_INVALID_STATE_TRANSITION, ERR_CHECKIN_INVALID_IMAGE, ERR_CHECKIN_NO_GPS, ERR_EXPORT_TRIP_NOT_COMPLETED, ERR_EXPORT_STORAGE_PERMISSION_DENIED, ERR_FORBIDDEN_RESOURCE, ERR_RATE_LIMIT_EXCEEDED, ERR_SOS_NOT_ACTIVE, ERR_WATERMARK_RENDER_FAILED); SCR-TRIP-02 and SCR-TRIP-03 have no States or Data Contracts lines; SCR-TRIP-01 field inventory lists no Start/Pause/Resume/End controls
- Description: Round-1 BLOCKER ARC-001 asked for each screen's error code and message and its loading, empty and error states. The mapping covers only 10 of 28 domain codes, so most messages are undefined. This includes the safety-critical ERR_SOS_NO_CONTACTS_OFFLINE (the 113/115 prompt) and the permission-denied codes. SCR-TRIP-02 (check-in) and SCR-TRIP-03 (export) have no states (offline pending, saving, permission denied, preview) and no data contracts. SCR-TRIP-01 omits the core REQ-009 controls (Bat dau, Tam dung, Tiep tuc, Ket thuc) from its field inventory, although SCR-SOS-04 lists actions as fields. The trip-detail screen also lacks location_name and captured_at.
- Required remediation: Map every error code in the SRS to an HTTP status, a screen and a Vietnamese message. Add States and Data Contracts to SCR-TRIP-02 and SCR-TRIP-03. Add the trip control actions, with their enabled-state rules per Trip status, to SCR-TRIP-01.

### F-006 [MEDIUM] requirement-depth
- Evidence: FR-005 exception 'Dung toa do GPS cuoi cung da luu voi is_stale_location = true'; FR-006 data 'latitude: Double (... required)'; integration-matrix.md /sos/trigger requires latitude, longitude
- Description: An SOS has no defined behaviour when the device has never had a GPS fix (fresh install, location permission denied, no last-known location). The API requires latitude and longitude, so the safety-critical SOS would fail validation (422) or the SMS would carry an empty Maps link.
- Required remediation: Define the no-location SOS path: nullable coordinates with a location_unavailable flag, an SMS template without a Maps link, and a web page state. Add an acceptance criterion for it.

### F-007 [MEDIUM] requirement-depth
- Evidence: BR-002 'Phien dang nhap hop le khi offline neu SecureStore con refresh_token chua qua 30 ngay'
- Description: Once the refresh token is older than 30 days while the user is offline, BR-002 implies the login screen, which needs network. The spec does not say whether the SOS button and offline SMS fallback stay reachable. For a safety app, being locked out of SOS offline is a significant risk.
- Required remediation: State whether SOS, SMS fallback and local data stay accessible after offline session expiry, for example with a limited offline-SOS mode. Add an acceptance criterion at 31 days offline.

### F-008 [MEDIUM] requirement-depth
- Evidence: FR-011 'chup/chon anh (JPEG/PNG)'; FR-012 'Ngay gio theo mui gio local thiet bi'; data-dictionary.md tbl_trip_checkins.captured_at
- Description: FR-011 allows picking an existing gallery photo, but FR-012 does not say whether the watermark time and location come from the photo's EXIF data or from the current device time and GPS. REQ-011 asks for 'Ngay gio chup' (capture time) while REQ-010 asks for the current GPS. There is also no rule for rounding altitude (round or truncate), for the altitude reference (GPS ellipsoid height vs sea level), or for truncating a 200-character location_name on the image.
- Required remediation: Define the source of time, location and altitude for camera vs gallery photos, the altitude rounding and reference, and the truncation length for location_name. Add an acceptance criterion for a gallery photo.

### F-009 [MEDIUM] security-privacy
- Evidence: FR-007 step 3 'toi da 50 diem ... (tu tbl_trip_breadcrumbs neu co trip_id ...)'; alternate 'tiep tuc hien thi vi tri cuoi cho toi khi het han 24h'
- Description: After an SOS is RESOLVED, the trail still comes from the 50 most recent tbl_trip_breadcrumbs points of a trip that keeps recording. For 24 hours the public page keeps revealing the user's position after they declared themselves safe.
- Required remediation: Limit the trail and last location to points recorded at or before ended_at once the session is RESOLVED. Add an acceptance criterion for it.

### F-010 [MEDIUM] security-availability
- Evidence: NFR-002 'GET /track/{token} (30 req/phut/IP)'; integration-matrix.md lists 429 on /api/v1/track/{token}/status; FR-007 poll every 15 s
- Description: The 30 requests/min limit is per IP. Mobile carriers use CGNAT, so many unrelated relatives share one public IP, and each viewer polls 4 times a minute. Relatives could be blocked from the emergency page by HTTP 429 during an active SOS. It is also unclear whether the limit covers the status API.
- Required remediation: Rate-limit per token plus per IP with a higher ceiling (or limit only failed lookups to stop token enumeration). State which endpoints the limit covers, and add an acceptance criterion for several viewers on one IP.

### F-011 [MEDIUM] security
- Evidence: client_id 'UK' columns; INV-DAT-003 'ON CONFLICT (client_id) DO NOTHING'; NFR-003 'Server tra ve ban ghi da tao truoc do'
- Description: The idempotency key client_id is unique across all users and a replay returns the existing record. A request carrying another user's client_id would be treated as a duplicate and could return that user's record, or silently drop the caller's write. Idempotency should be scoped to the owner.
- Required remediation: Make idempotency keys unique per (user_id, client_id). On a conflict, return the existing record only when it belongs to the caller, otherwise 409. State the replay status code (200 vs 201).

### F-012 [MEDIUM] integration-feasibility
- Evidence: 'OpenStreetMap Nominatim | OSM Foundation | ... | 2000 ms'; 'OS SMS Composer | ... | Native SMS URI (sms:)'
- Description: The public Nominatim service limits use to 1 request per second per application, requires an identifying User-Agent and forbids heavy use. Calling it directly from every client in production breaks those terms, and there is no fallback provider. 'sms:' links with several recipients behave inconsistently (iOS and Android use different separators, and iOS links do not reliably accept several numbers). The 'hoat dong ca iOS & Android' promise in OQ-002 needs the native compose APIs instead.
- Required remediation: Record the Nominatim usage constraints (rate limit, User-Agent, caching, or a backend proxy or self-hosted instance). Specify the native SMS compose mechanism for multiple recipients on each platform.

### F-013 [MEDIUM] api-completeness
- Evidence: srs.md FR-002 step 4 'dong bo ho so ca nhan ve SQLite'; catalogue has only PUT /profile/emergency-card; data-dictionary.md tbl_refresh_tokens.revoked_at 'neu dang xuat/doi mat khau'
- Description: FR-002 syncs the profile to the device after login, but there is no GET /api/v1/me or GET /api/v1/profile/emergency-card. The data dictionary mentions logout and password change, but neither has an FR or endpoint.
- Required remediation: Add the GET endpoints that FR-002 step 4 needs. Either specify logout (POST /auth/logout, which revokes the refresh token and clears SecureStore and local data) or remove the reference.

### F-014 [MEDIUM] requirement-depth
- Evidence: FR-006 alternate 'mo OS SMS Composer ... dong thoi luu SQLite voi sync_status = PENDING'
- Description: The OS SMS composer needs the user to press Send, and the app cannot reliably tell whether the SMS was sent or dismissed. The spec gives no UI state or retry prompt if the user closes the composer, and does not say whether the app should reopen it or show 'SMS chua gui'.
- Required remediation: Define the post-composer state (a 'Gui lai SMS' action on SCR-SOS-04, plus the offline SOS state shown) and add an acceptance criterion for a dismissed composer.

### F-015 [MEDIUM] nfr-testability
- Evidence: NFR-004 '<= 5%/gio tren thiet bi tham chieu'
- Description: The reference device, OS version, screen state and GPS mode for the battery test are not named, so the <= 5%/hour target cannot be measured reproducibly.
- Required remediation: Name the reference devices (one iOS and one Android model and OS version) and the test conditions (screen off, other apps closed, starting charge level).

### F-016 [LOW] traceability
- Evidence: REQ-002 -> 'SCR-AUTH-02, SCR-AUTH-03' (SCR-AUTH-02 is the emergency card); REQ-008 -> 'SCR-TRIP-01' which has no permission or background-location fields; srs.md/fsd.md header 'Status: REWORK'
- Description: The RTM maps REQ-002 to the emergency-card screen, and maps REQ-008 to a screen that has no location-permission UI. The SRS and FSD headers still say Status: REWORK.
- Required remediation: Correct the FSD mappings in the RTM, add the permission-prompt UI for REQ-008, and update the document status.

### F-017 [LOW] edge-case
- Evidence: FR-008 'app dat lich nhac truoc 10 phut' with minimum deadline now + 5m
- Description: For deadlines less than 10 minutes away (the minimum is 5 minutes), the reminder time is already in the past. The behaviour (skip, or remind immediately) is not stated.
- Required remediation: State the reminder rule for short timers and add a boundary acceptance criterion (deadline = now + 5m).

## Sample verification

| ID | Result | Spec reference |
| --- | --- | --- |
| REQ-003 | COVERED | artifacts/srs.md#FR-004; fsd.md SCR-AUTH-02; data-dictionary.md 2.4 |
| REQ-009 | COVERED | artifacts/srs.md#FR-010; fsd.md SCR-TRIP-01 |
| REQ-004 | COVERED | artifacts/srs.md#FR-005 |
| REQ-010 | COVERED | artifacts/srs.md#FR-011; integration-matrix.md 2.3, 3 |
| REQ-007 | PARTIAL | artifacts/srs.md#FR-008 |
| REQ-001 | COVERED | artifacts/srs.md#FR-001, #FR-002 |
| REQ-011 | COVERED | artifacts/srs.md#FR-012 |
| REQ-005 | PARTIAL | artifacts/srs.md#FR-006 |
| REQ-006 | COVERED | artifacts/srs.md#FR-007, #FR-014; fsd.md SCR-SOS-02 |
| REQ-008 | COVERED | artifacts/srs.md#FR-009; NFR-004 |
| REQ-012 | PARTIAL | artifacts/srs.md#FR-013 |
| REQ-002 | COVERED | artifacts/srs.md#FR-003; fsd.md SCR-AUTH-03 |
