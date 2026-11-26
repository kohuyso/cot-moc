# Architecture Review - cot-moc-mvp-v5

- Reviewer: independent_sa_reviewer
- Verdict: ESCALATE (round 3)
- User intent verified: True
- Findings: 10

## Summary

Round 3 of BA_SA, on inputs identical to the v3/v4 attempts that ended with reviewer_exit_code:2 and no verdict. Coverage matches the harness evidence: 18 source IDs, 12 traced, 6 Phase-2 IDs excluded with user confirmation, 0 uncovered; rtm.md has 18 rows. OQ-001..004 are RESOLVED and ASM-001..007 confirmed. All 3 modules (auth_profile, sos_safety, trip_journal) have SRS sections and FSD screens. I opened all 14 FRs and each meets the depth contract (main flow, alternate and exception flows, typed data, rule with worked example, at least 2 ACs including a negative). The earlier round-2 findings are largely fixed: async SOS dispatch, min(trim, 0.25*d), 28-code error mapping, active SOS/timer GET endpoints, Limited Offline-SOS mode. Two HIGH gaps remain on the safety path. (1) The offline SMS content is undefined, and no SMS carries the emergency card that REQ-005 and REQ-003 require. (2) The deferred offline SOS is sent last in the offline sync order, after trips, breadcrumbs and photo uploads. MEDIUM gaps: duplicate SOS trigger, offline resolve, gallery-photo location source and stale-GPS threshold, web trail data source and missing columns, client-side Nominatim policy, and inherited run-id headers (the fork lineage in state.json makes this mechanical). review_rounds.BA_SA is already 2 and the earlier extension has been used, so the loop ceiling is exhausted and this escalates to a human decision instead of a further pushback.

## Findings

### F-001 [HIGH] requirement-depth
- Evidence: srs.md FR-006 alternate flow line 257 'mo expo-sms composer dien san mang SDT nguoi than va mau SMS (link Google Maps hoac Chua xac dinh GPS)'; BR-006 line 272 defines only the Online and Follow-up templates; URD.md:22 'SMS chua toa do GPS (dang link Google Maps) + % pin + thong tin khan cap'; URD.md:16 'de dinh kem khi phat SOS'; NFR-001 AC 'Trinh soan SMS voi noi dung day du'
- Description: The offline SMS, the only channel when there is no data, has no defined template. No template includes the emergency card (blood type, drug allergies, medical conditions, plate, vehicle), although FR-006 step 1 collects EmergencyCard and REQ-005 requires 'thong tin khan cap' in the offline SMS. In the online path the card is shown only on the web page; it is never included in any SMS. No rule covers SMS length or encoding: drug_allergies and medical_conditions can each be 500 characters, and Vietnamese diacritics force UCS-2, which allows only 70 characters per segment. 'Thoi diem cap nhat cuoi' (REQ-005) is also ambiguous: the template prints the trigger time, not the time of the last GPS fix when is_stale_location = true. A developer cannot build the offline SMS, and a tester cannot verify 'noi dung day du'.
- Required remediation: Define the exact offline SMS template: Google Maps URL format, battery %, time of the last GPS fix, and the card fields (blood type, allergies, conditions, plate, vehicle model). Add a truncation and ordering rule with a maximum length or segment count, and an encoding rule (for example, strip diacritics to GSM-7). State whether the online gateway SMS also carries a short card summary. Add acceptance criteria with concrete values, including a 500-character allergy field and a no-GPS case. Update NFR-001 and the FSD SCR-SOS-01/SCR-SOS-04 accordingly.

### F-002 [HIGH] failure-mode
- Evidence: integration-matrix.md §3.1 'Contacts & EmergencyCard -> SafetyTimers -> Trips -> Breadcrumbs & Checkins -> (5) Deferred SOS'; §3.2 retry 5s, 15s, 45s; srs.md FR-006 alternate 'Dong bo bu khi co mang lai sau SOS Offline ... gui POST /api/v1/sos/trigger (triggered_offline=true) de tao SosSession va gui SMS follow-up kem tracking_url'
- Description: When connectivity returns after an offline SOS, the deferred POST /sos/trigger, which creates the tracking link and the follow-up SMS to relatives, is queued last. It waits behind trip records, possibly thousands of breadcrumbs, and multipart photo uploads of up to 10 MB each with retry backoff. On a weak 2G/3G signal, relatives may wait minutes for the live tracking link. Safety-critical traffic is placed behind journal traffic.
- Required remediation: Give deferred SOS, SOS heartbeats/resolve and safety-timer actions top priority in the sync order, after contacts and the emergency card but before trips, breadcrumbs and check-ins. Send trip_id as null or back-fill it later so SOS does not depend on trip sync. Add an acceptance criterion: with N pending photos and breadcrumbs, the deferred SOS request is sent first, within a stated time after connectivity returns.

### F-003 [MEDIUM] business-rule
- Evidence: FR-006 step 3 'tối đa 1 ACTIVE/user'; FR-008 step 4 'hoặc gắn vào SosSession ACTIVE hiện có'; BR-014; integration-matrix.md §2.2 /sos/trigger lists no 409 or return-existing behaviour
- Description: The 'max 1 ACTIVE SosSession' rule has no defined behaviour on violation. A second manual trigger while one session is ACTIVE (a new client_id, for example after reinstall or a second device) has no response code, does not say whether it returns the existing session, and does not say whether relatives are alerted again. When the Dead Man's Switch attaches to an existing ACTIVE session, it is not stated whether a new alert is sent, which template is used, or how trigger_source is recorded.
- Required remediation: Specify the response for a trigger while a session is ACTIVE (for example 200 with the existing session and no new SMS, or 409 with a new error code mapped in the FSD). Specify the alert and template sent when the timer attaches to an ACTIVE session. Add acceptance criteria for both.

### F-004 [MEDIUM] requirement-depth
- Evidence: FR-014 alternate flow covers only offline heartbeat; FR-008 offline 'Toi an toan' queued; integration-matrix.md §3.3 '409 -> FAILED_PERMANENT ... thong bao nguoi dung'
- Description: If an SOS was created online and the user presses 'Toi da an toan' (resolve) or 'Thu hoi link' while offline, the behaviour is undefined: no queue, no UI state, and relatives keep seeing ACTIVE together with the medical card. Similarly, a queued offline timer check-in that syncs after the server already moved to EXPIRED_ALERTED gets 409 and is dead-lettered with a generic notice. The user is not told that relatives were alerted, nor prompted to resolve the auto-created SOS.
- Required remediation: Define offline resolve and revoke: local state, deferred POST, and what the UI shows. Define the handling of 409 ERR_TIMER_ALREADY_EXPIRED on deferred check-in: show the auto-created SOS via GET /sos/active and offer resolve. Add acceptance criteria.

### F-005 [MEDIUM] consistency
- Evidence: FR-011 'gan dung toa do GPS hien tai'/step 2 'gan GPS hien tai'; FR-012 step 1 'Gallery uu tien doc EXIF GPS'; fsd.md SCR-TRIP-02 latitude source 'Device GPS / EXIF'; FR-005/FR-011 'is_stale_location' without an age threshold
- Description: For gallery photos it is ambiguous whether the stored check-in latitude/longitude (map pin) is the current device position (FR-011 and REQ-010) or the EXIF position (FR-012 and the FSD). The watermark could show coordinates that differ from the pin. No threshold defines when a last-known fix is 'stale', and no limit says how long the app waits for a fresh fix before using it, for SOS or for check-in.
- Required remediation: State one rule for the stored check-in position and the watermark position, for camera and for gallery photos. Define the fresh-fix wait time and the age threshold for is_stale_location, and keep them compatible with the < 1000 ms offline SOS target. Add acceptance criteria.

### F-006 [MEDIUM] data-model
- Evidence: fsd.md SCR-SOS-02 breadcrumb_trail persistence 'tbl_trip_breadcrumbs / tbl_sos_locations'; tbl_sos_sessions has no triggered_offline/resolved_offline columns, while integration-matrix.md /sos/trigger accepts them and FR-006 AC 3 asserts them
- Description: The 50-point trail on the public page comes from two tables (trip breadcrumbs and SOS heartbeats) with no selection or merge rule. tbl_sos_sessions cannot store triggered_offline or resolved_offline, although the API accepts them and acceptance criteria depend on them.
- Required remediation: Define the trail source rule (for example, merge both tables ordered by recorded_at, de-duplicate, take the latest 50, use sos_locations when trip_id is null). Add triggered_offline and resolved_offline columns, or state how they are derived.

### F-007 [MEDIUM] integration-feasibility
- Evidence: 'OpenStreetMap Nominatim | ... | App -> External | ... Gioi han <= 1 req/s, header User-Agent: CotMocApp/1.0, cache 24h'
- Description: Nominatim's public usage policy limits the whole application to 1 request per second. Each phone calling it directly cannot enforce an app-wide limit, so production use with many users breaks the policy, and the spec defines no fallback provider.
- Required remediation: Route reverse geocoding through a backend proxy with shared caching and rate limiting, or a self-hosted or commercial geocoder. Alternatively, record a user-confirmed assumption accepting the risk, with a degradation rule (fall back to coordinates).

### F-008 [MEDIUM] provenance
- Evidence: Run ID header 'cot-moc-mvp-v3' in srs.md, requirement-analysis.md, fsd.md, data-dictionary.md, integration-matrix.md and rtm.md; requirement.json OOS-001 reason 'cot-moc-mvp-v3'; srs.md §10 responds to v2 findings; state.json lineage parent_run cot-moc-mvp-v4 (fork chain v2->v3->v4->v5)
- Description: Every artifact names run cot-moc-mvp-v3, while this run is cot-moc-mvp-v5. state.json shows this run was created by a harness fork from v4 (itself forked from v3) with byte-identical artifacts, the sanctioned way to carry artifacts forward. The source version and module list match the configuration, so the content is not foreign. The headers are still stale.
- Required remediation: Update the Run ID headers and the requirement.json out-of-scope reasons to cot-moc-mvp-v5, or state the fork lineage explicitly in each header.

### F-009 [LOW] validation
- Evidence: FR-001 regex '^(\+84|0)[0-9]{9,10}$' vs BR-001 'bat dau bang 0 (10 so)'; FR-003 phone '10..15 digits, normalized to E.164 +84'
- Description: The FR-001 regex accepts 11-digit numbers starting with 0, while BR-001 says 10 digits. FR-003 allows 10 to 15 digits but defines normalisation only for Vietnamese numbers, so how a foreign relative's number is handled is unclear.
- Required remediation: Align the regex with BR-001 and define the handling of non-Vietnamese contact numbers (accept E.164 as-is, or reject).

### F-010 [LOW] business-rule
- Evidence: BR-010 'tong Haversine cac cap breadcrumb lien tiep'; integration-matrix.md /trips/{id}/complete accepts client-computed distance_km and duration_seconds
- Description: It is not stated whether the segment between the last point before a pause and the first point after resume counts toward distance_km. The server accepts client-computed totals without saying whether it validates or recomputes them.
- Required remediation: State the pause-gap rule with an example, and whether the server trusts or recomputes the totals.

## Sample verification

| ID | Result | Spec reference |
| --- | --- | --- |
| REQ-003 | PARTIAL | artifacts/srs.md#FR-004; artifacts/srs.md#FR-006 BR-006; artifacts/fsd.md SCR-AUTH-02 |
| REQ-004 | COVERED | artifacts/srs.md#FR-005; artifacts/fsd.md SCR-SOS-01 |
| REQ-006 | COVERED | artifacts/srs.md#FR-007, #FR-014; artifacts/fsd.md SCR-SOS-02; integration-matrix.md §2.2 |
| REQ-010 | COVERED | artifacts/srs.md#FR-011; artifacts/fsd.md SCR-TRIP-02; integration-matrix.md §2.3, §3 |
| REQ-001 | COVERED | artifacts/srs.md#FR-001, #FR-002; integration-matrix.md §2.1 |
| REQ-007 | COVERED | artifacts/srs.md#FR-008; artifacts/fsd.md SCR-SOS-03 |
| REQ-008 | COVERED | artifacts/srs.md#FR-009; NFR-004; artifacts/fsd.md SCR-TRIP-01 |
| REQ-005 | PARTIAL | artifacts/srs.md#FR-006; integration-matrix.md §1, §3 |
| REQ-012 | COVERED | artifacts/srs.md#FR-013; artifacts/fsd.md SCR-TRIP-03 |
| REQ-011 | COVERED | artifacts/srs.md#FR-012 |
| REQ-002 | COVERED | artifacts/srs.md#FR-003; artifacts/fsd.md SCR-AUTH-03; data-dictionary.md 2.3 |
| REQ-009 | COVERED | artifacts/srs.md#FR-010; artifacts/fsd.md SCR-TRIP-01, SCR-TRIP-04 |
