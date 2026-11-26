# Code Review Checklist: Source Code & Implementation Diffs

**Target Artifact**: `artifacts/code-review.md`
**Reviewer Role**: `sdlc-code-review` (Independent Reviewer)
**Standards Alignment**: ISO/IEC/IEEE 29119 (Software Testing), IEEE 1028 (Software Reviews and Audits)
**Marker Semantics**: Mark `[x]` only when the code implementation passes independent inspection.

---

> [!IMPORTANT]
> **Adversarial Scope Gate & Deterministic Remediation**:
> Code Review mandates strict evaluation of `scope_coverage`. Every functional requirement (`FR-xxx`) from SRS must be checked for concrete implementation in the diff.
> If any FR is missing, partially implemented, stubbed, or has `implemented: false`, the reviewer **MUST NOT APPROVE**; the reviewer **MUST issue `PUSHBACK` with loop `DEV_REVIEW`** (`sdlc pushback --loop DEV_REVIEW`) accompanied by an actionable finding detailing the omission.

---

## 1. Requirement Scope & Functional Completeness (Active Cross-Check)
- [ ] `CHK-CR-001`: Are 100% of functional requirements (`FR-xxx`) from `artifacts/requirement-analysis.md` actively cross-checked and itemized in `code-review.json.scope_coverage`?
- [ ] `CHK-CR-002`: Are administrative features, management panels, and user-facing tabs/views fully implemented without omitted routes or placeholder stubs?
- [ ] `CHK-CR-003`: Are all declared API endpoints, routes, controllers, and service methods concretely implemented with request validation and proper response serialization?
- [ ] `CHK-CR-004`: Are application startup hooks, service registrations, dependency injection bindings, and background workers properly wired without runtime initialization gaps?

## 2. Conformance & Scope Confinement
- [ ] **Gate chạy qua harness sau diff**: `COMMAND_EXECUTED` cho từng gate (`lint`, `test`) với `exit_code: 0`, timestamp __ sau `diff.patch`; số test pass/fail trong report khớp output đã seal.
- [ ] Diff không chứa build output (`__pycache__/`, `*.pyc`, `bin/`, `obj/`) và không chứa ngôn ngữ ngoài stack đã khai trong `commands`.
- [ ] Mỗi task trong plan: file `Create` có mặt __/__, file `Test` có mặt __/__; không stub (entity rỗng, service 1 method) được báo là "đã triển khai".
- [ ] `CHK-CR-005`: Does the actual git diff stay strictly within the files declared in the approved implementation plan?
- [ ] `CHK-CR-006`: Does the diff match the author's claims in `implementation-report.md` without secret scope expansion, phantom changes, or dead code?
- [ ] `CHK-CR-007`: Did the author refrain from opportunistic refactoring of unrelated legacy code?

## 3. Correctness & Error Handling
- [ ] `CHK-CR-008`: Does the code satisfy all functional requirements and business rules without logical bugs or off-by-one errors?
- [ ] `CHK-CR-009`: Are edge cases (null/None, empty strings, boundary numbers, malformed input, concurrent access) handled safely?
- [ ] `CHK-CR-010`: Are errors caught and wrapped into domain types without swallowing exceptions, silent failures, or leaking internal stack traces?

## 4. Regression & Deletion Checks
- [ ] `CHK-CR-011`: Were modified or deleted lines verified against callers and consumers to prevent silent breaking changes?
- [ ] `CHK-CR-012`: Are existing regression test suites still passing without modification or deletion of their assertions?

## 5. Security, Authentication & Session Integrity
- [ ] `CHK-CR-013`: Are authentication handshakes, session cookies, and authorization guards fully integrated and enforced across all protected endpoints?
- [ ] `CHK-CR-014`: Are session/auth cookies configured with security attributes (`HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`) to prevent credential leakage and XSS/CSRF exposure?
- [ ] `CHK-CR-015`: Are queries parameterized and user inputs sanitized (zero SQL/command injection, zero unescaped HTML/XSS)?
- [ ] `CHK-CR-016`: Are secrets, tokens, API keys, and credentials completely absent from source code, configuration files, and commit history?
- [ ] `CHK-CR-017`: Are database queries efficient without N+1 query patterns or unbounded table scans?

## 6. Test Quality
- [ ] `CHK-CR-018`: Do unit tests assert real business outcomes rather than testing mocks or trivially asserting `True`?
- [ ] `CHK-CR-019`: Did tests fail before the fix was introduced (Red-Green verification)?

## 7. Scope Coverage Evaluation & Adversarial Pushback
- [ ] `CHK-CR-020`: Has every FR from SRS been confirmed with concrete implementation in the diff (`implemented: true` with non-empty evidence files) in `code-review.json.scope_coverage`?
- [ ] `CHK-CR-021`: If ANY FR is missing, incomplete, or marked `implemented: false`, has the reviewer issued a deterministic `PUSHBACK` with loop `DEV_REVIEW` (`sdlc pushback --loop DEV_REVIEW`) containing an actionable remediation finding?
