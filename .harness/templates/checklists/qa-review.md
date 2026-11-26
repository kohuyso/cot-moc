# QA Audit & Release Readiness Checklist

**Target Artifacts**: `artifacts/test-report.md`, `artifacts/qa-verdict.md`, `artifacts/qa-verdict.json`
**Reviewer Role**: `sdlc-qa-review` (Independent Reviewer)
**Standards Alignment**: ISO/IEC/IEEE 29119 (Software Testing - Concept, Test Processes, Verification), IEEE 1028 (Software Reviews and Audits)
**Marker Semantics**: Mark `[x]` only when quality assurance verification is complete.

> [!IMPORTANT]
> **Multi-Tier Quality Gate & Adversarial Pushback**:
> Approval requires verified test execution evidence across **ALL applicable tiers**:
> - `tier: UNIT`: Unit tests with real business logic assertions and boundary checks.
> - `tier: INTEGRATION`: API contract, database, and inter-service interaction tests.
> - `tier: E2E_UI`: Automated UI/browser tests (mandatory for web/UI components).
> - `tier: SMOKE`: Clean application bootstrap and runtime readiness without placeholder crashes.
> 
> If any tier has failed tests, unresolved defects, or missing test coverage for any FR, QA **MUST NOT APPROVE**; QA **MUST issue `REJECT` and push back with `loop="TEST_QA"`** (`sdlc pushback --loop TEST_QA`).

---

## 1. Execution Evidence & Objectivity
- [ ] `CHK-QA-001`: Was the test report generated from a fresh, complete execution run rather than cached results?
- [ ] `CHK-QA-002`: Are exit codes, durations, and output streams clearly documented for all test commands?
- [ ] `CHK-QA-003`: Are 100% of P0 and P1 test cases in `PASS` status?
- [ ] `CHK-QA-004`: Are there zero unexplained `BLOCKED` or `NOT_RUN` test cases?

## 2. Requirement Traceability & ISO 29119 Matrix Verification
- [ ] `CHK-QA-005`: Are 100% of functional requirements (`FR-xxx`) from `artifacts/requirement-analysis.md` and `artifacts/requirement.json` itemized in `qa-verdict.json.verified_requirements`?
- [ ] `CHK-QA-006`: Does every item in `qa-verdict.json.verified_requirements` map to passing test execution evidence with status `PASS` (zero unmapped, omitted, or failed requirements)?
- [ ] `CHK-QA-007`: Have all Given/When/Then acceptance criteria been verified against actual runtime test evidence rather than mock stubs or trivial assertions?
- [ ] `CHK-QA-008`: Did the test executor avoid reinterpreting requirements to turn failing tests green?

## 3. Multi-Tier & Comprehensive E2E Verification Evidence (Coverage >= 90%)
- [ ] `CHK-QA-016`: Unit test execution verified (`tier: UNIT`) with real business assertions and domain boundary tests?
- [ ] `CHK-QA-017`: Integration & API contract test execution verified (`tier: INTEGRATION`) covering inter-service boundaries, DB operations, and HTTP endpoints?
- [ ] `CHK-QA-018`: Browser Runtime E2E Automation: UI / End-to-End automation test execution verified (`tier: E2E_UI`) on real browser engines (Playwright, Cypress, or Headless Chromium) for all user-facing features?
- [ ] `CHK-QA-019`: Smoke / startup runtime verification verified (`tier: SMOKE`) ensuring application bootstraps cleanly without crashes or placeholder errors?
- [ ] `CHK-QA-020`: Adversarial Pushback Policy: If any tier has failed tests or missing coverage for any FR, has QA issued `REJECT` and pushed back with `loop="TEST_QA"` (`sdlc pushback --loop TEST_QA`) instead of approving?
- [ ] `CHK-QA-021`: Strict Anti-Build-As-Test Policy: CẤM TUYỆT ĐỐI công nhận `npm run build`, `vite build`, hoặc `tsc` là bằng chứng kiểm thử UI. Lệnh build chỉ kiểm tra tính hợp lệ cú pháp và đóng gói bundle, không thể thay thế việc chạy và tương tác trên trình duyệt thật.
- [ ] `CHK-QA-022`: Holistic E2E UI Coverage >= 90%: Kiểm thử tự động E2E phải bao phủ tối thiểu >= 90% toàn bộ tính năng và hành trình người dùng của hệ thống (User Journeys, form submit, button click, navigation, modal/dialog, CRUD operations, state updates, file upload/download, canvas/media rendering, dynamic DOM rendering).
- [ ] `CHK-QA-023`: Zero Browser Console Error: Xác nhận log console trình duyệt sạch 100% trong toàn bộ quá trình chạy test E2E (không có Uncaught TypeError, DOMException, CSS parsing/oklch runtime crash, hoặc unhandled promise rejections).
- [ ] `CHK-QA-024`: Real DOM & Artifact Assertions: Mọi kịch bản E2E phải có assertions rõ ràng trên DOM thật hoặc Browser Artifacts (phần tử hiển thị/ẩn, URL thay đổi, dữ liệu hiển thị đúng, file download sinh ra có dung lượng > 0 bytes) thay vì chỉ kiểm tra HTTP status hoặc component render cô lập.

## 4. Runtime & Configuration Readiness
- [ ] `CHK-QA-009`: Are there zero unresolved Blocker (`P0`) or High (`P1`) defects in the defect register?
- [ ] `CHK-QA-010`: Was runtime startup/smoke test executed against real application configuration (DI container bootstraps, endpoints respond without runtime crash)?
- [ ] `CHK-QA-011`: Are application configuration files free of unresolved dummy placeholders (e.g. `[AZURE_...]`, `[DB_...]`, invalid URIs/connection strings) that cause runtime crashes?
- [ ] `CHK-QA-012`: Did QA verify cross-component integration rather than relying solely on isolated unit tests with mock objects?
- [ ] `CHK-QA-013`: Are regression suites for existing, untouched workflows passing with 100% success?

## 5. Independent Governance
- [ ] `CHK-QA-014`: Did QA verify this artifact independently without having authored or executed the tests (no self-approval)?
- [ ] `CHK-QA-015`: Is any non-blocking residual risk explicitly documented with mitigation in the risk disclosure?
