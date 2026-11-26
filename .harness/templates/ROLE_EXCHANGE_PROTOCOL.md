# Role Exchange Protocol & Handoff Specification

## 1. Governance Principles

1. **Producer / Challenger Separation**: Every stage involves a distinct Producer (who crafts an artifact) and an independent Challenger (who critiques and verifies the artifact).
2. **Zero Self-Approval**: No agent or role may review, approve, or sign off on its own work.
3. **Single Writer of State**: The Harness Controller alone writes `.harness/runs/<run-id>/state.json` and `.harness/runs/<run-id>/events.jsonl`. No role may edit state directly.
4. **Isolated Context**: Challengers evaluate deliverables using fresh context, inspecting artifacts and objective evidence rather than conversational narrative.
5. **Bounded Disagreement**: Review loops have deterministic retry ceilings. When exhausted, actors must not continue arguing; they must produce an escalation report and hand off to human governance.
6. **Adversarial Verification & Runtime Readiness**: Challengers (especially QA and Code Review) must verify real runtime behavior and configuration integrity. Green unit tests with 100% mocks do not satisfy quality gates if application startup fails, configs contain unmapped dummy placeholders, or runtime smoke tests crash.
7. **Mandatory Stakeholder Clarification Gate**: When requirements contain open questions or lack essential domain constraints, `sdlc-ba-analysis` is strictly forbidden from making unconfirmed guesses or calling `submit_srs`. The authoring role must halt and solicit direct user clarification in chat. All `open_questions` in `requirement.json` must reach `status: RESOLVED` and assumptions must be confirmed by the stakeholder (`confirmed_by_user: true`) before the `submit_srs` gate permits transition to `SA_REVIEW`.
8. **Autonomous Inner Loop Convergence (Loop-until-Green)**: In `DEV_CODING` phase and pushback remediation, agents MUST autonomously loop between code/fixture modifications and test executions until the entire test suite achieves exit code 0. Agents are strictly forbidden from conversational turn-yielding or pausing mid-debugging to report partial progress to the user (e.g. "Fixed 1 test, 5 left"). The agent only reports to the user after full test suite convergence (100% green) and gate transition, or upon hitting an unresolvable structural escalation ceiling.
9. **Zero Scope Truncation Without Stakeholder Consent**: No role (especially `sdlc-ba-analysis`) may move user requirements, screens, tabs, or requested capabilities into `out_of_scope` without explicit user confirmation in chat. All items in `out_of_scope` must be structured with `confirmed_by_user: true` and a documented reason. Gate `submit_srs` strictly blocks any unconfirmed out-of-scope entries (`unconfirmed_out_of_scope`).
10. **Mandatory Real E2E UI Verification for Frontend Changes**: Whenever a run modifies UI/Frontend code (or the project declares frontend components), `sdlc-qa-review` is strictly forbidden from bypassing browser tests or classifying UI requirements as `UNIT` or `INTEGRATION`. The run must verify requirements with `tier: "E2E_UI"`, execute real browser runners (`playwright`, `cypress`, etc.) with exit code 0, capture screenshots/traces, and verify clean browser console logs. Faking coverage (`e2e_coverage_rate: 100`, `browser_console_clean: true`) without executed browser test logs is strictly rejected by the gate (`rejected:missing_frontend_e2e_execution`, `rejected:fake_e2e_coverage_without_browser_execution`).
11. **Mandatory Granular Test Cases & Full Regression Verification**: Every run containing functional requirements (`requirement.json`) MUST author a machine-readable test cases registry (`artifacts/test-cases.json` conforming to `test-cases.schema.json`).
    - **100% Requirement Coverage**: Every functional requirement (`FR-xxx`) must map to at least one test case (`TC-xxx`).
    - **Prohibition of Dummy Build Steps**: Build, compilation, or bundle commands (e.g. `FE-TS-COMPILE`, `VITE-BUILD`, `BE-BUILD-TEST`, `NPM-BUILD`, `DOTNET-BUILD`, `TSC`) are build sanity checks, NOT test cases. Using build step names as test IDs is strictly rejected (`rejected:build_step_cannot_be_test_id`).
    - **Full Regression Suite**: Whenever a run operates in `maintain_upgrade` mode or modifies existing features, test cases must include explicit regression suites (`type: "REGRESSION"`). Test execution must run both newly added test cases and all existing baseline test cases. Bypassing regression checks or only running new test cases is prohibited.
    - **Deterministic QA Cross-Check**: `sdlc-qa-review` verified requirements in `artifacts/qa-verdict.json` must cross-reference valid, registered `test_id`s in `artifacts/test-cases.json`. Unregistered test IDs will trigger gate rejection (`unregistered_test_id_in_qa_verdict`).

---

## 2. Standard Handoff Envelope

Every agent-to-agent deliverable or review verdict must be accompanied by this standardized envelope in markdown frontmatter or structured event payload:

```yaml
envelope:
  run_id: "run-001"
  from_role: "sdlc-ba-analysis"
  to_role: "sdlc-sa-review"
  phase: "BA_DRAFT"
  artifact: "artifacts/requirement-analysis.md"
  decision: "SUBMIT" # SUBMIT | APPROVE | PUSHBACK | ESCALATE
  round: 1
  findings: []
  required_changes: []
  evidence:
    - "artifacts/intake.md"
  status: "PENDING_REVIEW"
  timestamp: "2026-10-05T10:00:00Z"
```

### Envelope Fields:
- `run_id`: Unique identifier of the active run.
- `from_role`: Authoring role producing the handoff.
- `to_role`: Target role designated to receive the deliverable.
- `phase`: Current lifecycle phase per harness state machine.
- `artifact`: Path to primary artifact produced under `.harness/runs/<run-id>/`.
- `decision`: Action code (`SUBMIT`, `APPROVE`, `PUSHBACK`, `ESCALATE`).
- `round`: Sequence iteration for the current review loop (1-indexed).
- `findings`: List of structured review findings (required on `PUSHBACK`).
- `required_changes`: Exact actionable remedies needed for remediation.
- `evidence`: File paths or command execution IDs proving the claims.
- `status`: Handoff state (`PENDING_REVIEW`, `ACCEPTED`, `REJECTED`, `ESCALATED`).
- `timestamp`: UTC timestamp in ISO 8601 format.

---

## 3. Workflow Operating Modes & Preconditions

The SDLC Harness operates under two distinct lifecycle modes configured at run initialization:

### 3.1 Mode: `new_build`
Used for net-new systems or green-field features.
- Initial Phase: `BA_DRAFT` (or `INTAKE`).
- Requirements Handoff: Requires non-empty `artifacts/requirement-analysis.md` before executing `submit_srs`.

### 3.2 Mode: `maintain_upgrade`
Used for existing production services, refactoring, and bug fixes.
- **Mandatory Precondition**: Prior to calling `submit_srs`, the producer MUST generate `artifacts/impact-analysis.md` (minimum 20 characters) along with `artifacts/requirement-analysis.md`.
- `artifacts/impact-analysis.md` must document:
  - Downstream and upstream caller blast radius.
  - API and schema backward-compatibility assessments.
  - Storage/migration risks and zero-downtime constraints.
  - Regression test targets.
- Calling `submit_srs` without `artifacts/impact-analysis.md` will be strictly blocked by the controller (`missing:artifacts/impact-analysis.md`).

---

## 4. Canonical Producer - Challenger Exchange Matrix

| Stage | Producer Role | Challenger Role | Input Artifact(s) | Review / Verdict Artifact | Return Target (on Pushback) | Allowed Transition Action |
|---|---|---|---|---|---|---|
| **Intake & Scope** | `sdlc-intake` | `sdlc-ba-analysis` | User Request | `artifacts/intake.md` | User / Chat | `start_intake` |
| **Requirements** | `sdlc-ba-analysis` | `sdlc-sa-review` & `sdlc-po-review` | `artifacts/intake.md`<br>*(+ `impact-analysis.md` if `maintain_upgrade`)* | `artifacts/requirement-analysis.md`<br>`artifacts/product-review.md` | `sdlc-ba-analysis` | `submit_srs` / `approve` / `pushback` (`BA_SA`) |
| **Architecture** | `sdlc-sa-design` | `sdlc-tech-design-review` | `artifacts/requirement-analysis.md` | `artifacts/solution-design.md`<br>`artifacts/architecture-review.md` | `sdlc-sa-design` | `request_human_approval` |
| **UI Prototype** | `sdlc-ui-designer` | `sdlc-ui-reviewer` | `artifacts/solution-design.md`, `requirement.json` | `artifacts/ui-mockup.html`, `artifacts/ui-verdict.json` | `sdlc-ui-designer` | `submit_prototype` / `pushback` (`UI_REVIEW`) |
| **Implementation Plan** | `sdlc-planner` | `sdlc-sa-review` / Lead | `artifacts/solution-design.md` | `artifacts/implementation-plan.md` | `sdlc-planner` | `approve` (to `DEV_CODING`) |
| **Implementation** | `sdlc-implementer` | `sdlc-code-review` | `artifacts/implementation-plan.md` | `artifacts/implementation-report.md`, Git Diff | `sdlc-implementer` | `submit_diff` |
| **Code Review** | `sdlc-code-review` | Implementer / Controller | Git Diff, `implementation-report.md` | `artifacts/code-review.md` | `sdlc-implementer` | `approve` / `pushback` (`DEV_REVIEW`) |
| **Test Execution** | `sdlc-test-executor` | `sdlc-qa-review` | `artifacts/test-plan.md`, Git Diff | `artifacts/test-report.md` | `sdlc-implementer` or `sdlc-test-design` | `submit_test_report` |
| **QA Quality Audit** | `sdlc-qa-review` | Harness Controller | `artifacts/test-report.md`, `requirement-analysis.md` | `artifacts/qa-verdict.md` | `sdlc-implementer` | `approve` / `pushback` (`TEST_QA`) |
| **Security Audit** | `sdlc-security-review`| Harness Controller | Git Diff, `artifacts/solution-design.md` | `artifacts/security-review.md` | `sdlc-implementer` | `approve` / `pushback` |
| **PR Evidence & CI**| `sdlc-pr-evidence` | Human Gatekeeper | All Gate Artifacts | `artifacts/pr-evidence.md`<br>`artifacts/pr-evidence.json` | Various | `ci_passed` (to `PR_READY`) |

---

## 5. Adversarial Remediation Loops & Retry Enforcement

Review loops operate under an adversarial remediation protocol to ensure that defects, omissions, and verification gaps are deterministically addressed before code advances.

### 5.1 Adversarial Remediation Across Tiers

The SDLC Harness enforces two primary engineering remediation loops:

#### 1. Scope & Implementation Remediation (`DEV_REVIEW` Pushback Loop)
- **Producer**: `sdlc-implementer`
- **Challenger**: `sdlc-code-review`
- **Trigger**:
  - Code Review identifies any functional requirement (`FR-xxx`) from `artifacts/requirement-analysis.md` or `artifacts/requirement.json` that is unaddressed, omitted, or stubbed out in the diff (`implemented: false` in `artifacts/code-review.json.scope_coverage`).
  - Code Review discovers any finding with severity `BLOCKER` or `HIGH` (e.g. security vulnerability, missing auth flag, race condition, unintended scope deviation).
- **Protocol Action**:
  - Reviewer MUST NOT approve.
  - Reviewer issues:
    ```powershell
    python -m sdlc_harness.cli transition --run-id <run-id> --action pushback --loop DEV_REVIEW
    ```
- **State Reversion**: State machine transitions from `CODE_REVIEW` (or `DEV_REVIEW`) back to `DEV_CODING`.
- **Remediation Requirement**:
  - `sdlc-implementer` MUST read the exact findings in `artifacts/code-review.md` and `artifacts/code-review.json` (specifically `findings` and `scope_coverage`).
  - Implementer writes or modifies code to implement all missing requirements and resolve all blocker/high findings.
  - Implementer runs complete verification commands (linters, typechecks, tests) in an **Autonomous Inner Loop** (fix -> test -> fix -> rerun), without pausing or reporting partial progress, until all tests pass with exit code 0.
  - Implementer updates `artifacts/implementation-report.md` with remediation evidence.
  - Implementer re-submits via `submit_diff`.

#### 2. Multi-Tier Verification & Defect Remediation (`TEST_QA` Pushback Loop)
- **Producer**: `sdlc-test-executor` & `sdlc-implementer`
- **Challenger**: `sdlc-qa-review`
- **Trigger**:
  - Any `FR-xxx` requirement from `requirement.json` or `requirement-analysis.md` is omitted or lacks verified passing evidence in `artifacts/qa-verdict.json.verified_requirements` (status != `PASS` or `WAIVED`).
  - Any required test tier (`UNIT`, `INTEGRATION`, `E2E_UI`, `SECURITY`, `SMOKE`, `PERFORMANCE`) failed, was skipped, or is missing test evidence (e.g., frontend/UI changes without corresponding UI/E2E test runs).
  - Test execution logs in `test-execution-raw.json` show any non-zero exit code.
  - Runtime application startup / smoke test fails or crashes.
  - Configuration contains unresolved dummy placeholders (`[AZURE_...]`, `[DB_...]`).
  - Any unresolved `CRITICAL`, `HIGH`, or `BLOCKER` issues remain.
- **Protocol Action**:
  - QA Reviewer MUST NOT approve.
  - QA Reviewer issues:
    ```powershell
    python -m sdlc_harness.cli transition --run-id <run-id> --action pushback --loop TEST_QA
    ```
- **State Reversion**: State machine transitions from `QA_REVIEW` back to `DEV_CODING` for implementer and tester to remediate.
- **Remediation Requirement**:
  - `sdlc-implementer` and `sdlc-test-executor` inspect `artifacts/qa-verdict.md` and `artifacts/qa-verdict.json.issues`.
  - Implementer fixes underlying functional bugs or missing integration points.
  - Tester writes missing test scenarios across the required tiers (Unit, Integration, E2E/UI), re-runs test suites, captures clean execution logs, and updates `artifacts/test-report.md`.
  - Implementer and tester re-submit deliverables via the state machine until clean approval is achieved.

#### 3. Security & Vulnerability Remediation (`SECURITY_REVIEW` Pushback Loop)
- **Producer**: `sdlc-implementer`
- **Challenger**: `sdlc-security-review`
- **Trigger**:
  - Security Review detects any vulnerability with severity `BLOCKER`, `HIGH`, or `CRITICAL` (e.g. SQL injection, unvalidated redirect, secrets committed in code/config, missing auth/RBAC checks, insecure cookie flags).
  - Code Review discovers unresolved security findings before handoff.
- **Protocol Action**:
  - Security Reviewer MUST NOT approve.
  - Security Reviewer issues:
    ```powershell
    python -m sdlc_harness.cli transition --run-id <run-id> --action pushback --loop SECURITY_REVIEW
    ```
- **State Reversion**: State machine transitions from `SECURITY_REVIEW` back to `DEV_CODING`.
- **Remediation Requirement**:
  - `sdlc-implementer` inspects `artifacts/security-review.md` and `artifacts/security-review.json.findings`.
  - Implementer fixes all reported vulnerabilities (parameterizes queries, externalizes secrets to KMS/env, adds auth guards).
  - Implementer verifies fixes via tests, updates `artifacts/implementation-report.md` (`## 6. Pushback Remediation Log`), and runs `submit_diff`.
  - Flow re-enters review until zero `BLOCKER` or `HIGH` findings remain and verdict is `APPROVE`.

#### 4. UI Prototype & Design Finish Remediation (`UI_REVIEW` Pushback Loop)
- **Producer**: `sdlc-ui-designer`
- **Challenger**: `sdlc-ui-reviewer`
- **Trigger**:
  - Omission of any user-facing functional requirement (`FR-xxx`) from `requirement.json` in the mockup screens (`requirements_covered`).
  - Any of the 4 mandatory states (`normal`, `empty`, `loading`, `error`) is missing, incomplete, or non-functional in `states_validated`.
  - Generic AI slop aesthetics detected (default purple/cream palettes, clichéd templates, unstyled generic cards).
  - Dummy or lazy placeholder text (`lorem ipsum`, "Item 1", dummy zeros) instead of realistic domain data.
  - Mobile layout breakage or horizontal overflow at 375px viewport.
  - Accessibility violations (WCAG 2.1 AA text contrast failure, touch targets $< 44 \times 44\text{ px}$).
  - Any finding with severity `BLOCKER` or `HIGH` in `artifacts/ui-verdict.json`.
- **Protocol Action**:
  - Reviewer MUST NOT approve.
  - Reviewer issues:
    ```powershell
    python -m sdlc_harness.cli transition --run-id <run-id> --action pushback --loop UI_REVIEW
    ```
- **State Reversion**: State machine records pushback in loop `UI_REVIEW` and remains in `UI_PROTOTYPE` for `sdlc-ui-designer` to remediate.
- **Remediation Requirement**:
  - `sdlc-ui-designer` inspects `artifacts/ui-verdict.md` and `artifacts/ui-verdict.json.findings`.
  - Designer addresses all reported issues in `artifacts/ui-mockup.html` and `artifacts/ui-spec.md`.
  - Designer verifies all 4 states are interactive and mobile viewports are fully responsive.
  - Designer resubmits for re-review until verdict is `APPROVE`.

### 5.2 Bounded Disagreement & Retry Enforcement

Review loops are strictly bounded by the Harness Controller to prevent infinite circular debates:

1. **BA <-> SA Review Loop (`BA_SA`)**:
   - Limit: **2 rounds** max.
   - Round 1: SA evaluates `artifacts/requirement-analysis.md`. If issues exist, issues `pushback` with specific findings. BA refines in `BA_REWORK`.
   - Round 2: BA resubmits via `submit_srs`. If SA pushes back a second time, the state machine deterministically transitions to `HUMAN_APPROVAL` and forces generation of `artifacts/escalation-report.md`.
2. **UI Designer <-> UI Reviewer Loop (`UI_REVIEW`)**:
   - Limit: **2 rounds** max.
   - Round 1: Reviewer inspects prototype. If deficiencies exist, issues `pushback --loop UI_REVIEW`. Designer refines in `UI_PROTOTYPE`.
   - Round 2: If reviewer pushes back a second time, the retry ceiling is exhausted. The state machine deterministically escalates to `HUMAN_APPROVAL` / `ESCALATION_REQUIRED` and forces generation of `artifacts/escalation-report.md`.
3. **Developer <-> Code Review Loop (`DEV_REVIEW`)**:
   - Limit: **3 rounds** max.
   - On 3rd consecutive rejection, transition is escalated to human lead.
4. **Test <-> QA Audit Loop (`TEST_QA`)**:
   - Limit: **3 rounds** max.
   - On 3rd rejection, task is escalated with root cause failure analysis.
5. **Security Audit Loop (`SECURITY_REVIEW`)**:
   - Limit: **3 rounds** max.
   - On 3rd consecutive pushback, escalated to human security lead / human approval.

When a retry ceiling is reached:
- Actors MUST NOT submit further automated rework transitions.
- The active role MUST author `artifacts/escalation-report.md` containing failure history, root cause diagnosis, and 4 resolution options.
- The run enters `HUMAN_APPROVAL` state.

---

## 6. Human Governance & Decision Actions

When a run enters `HUMAN_APPROVAL`, autonomous loops pause. Human leads or operators resolve the escalation using explicit `human_decision` dispositions:

| Disposition | Target Phase | State Machine Effect | Usage / Intent |
|---|---|---|---|
| `ACCEPT_RISK` | Contextual (`SA_DESIGN`, `UI_PROTOTYPE`, `TEST_EXECUTION`, `CI_VERIFY`) | Transitions to `target_phase_on_accept`. Clears escalation context. | Human lead overrides review objection or accepts residual risk. Requires `approver`, `reason`, `evidence_ref`. Cannot waive deterministic failures. |
| `GRANT_EXTENSION` | Rework Phase (`BA_REWORK`, `UI_PROTOTYPE`, `DEV_CODING`) | Increments `extensions_granted`. Bounded by `max_extensions_per_loop: 1`. | Grants exactly 1 additional rework/review iteration. Requires `approver`, `reason`, `evidence_ref`. |
| `REJECT_AND_CLOSE` | `CLOSED` | Transitions directly to `CLOSED`. | Escalation cannot be resolved or feature is cancelled. Requires `approver` and `reason`. |

---

## 7. Machine-Checkable CI & Precondition Gates for `ci_passed`

Transitioning from `CI_VERIFY` to `PR_READY` via `ci_passed` requires strict machine verification:

1. **Evidence Artifacts**:
   - `artifacts/pr-evidence.md` or `artifacts/pr-evidence.json` must be present and non-empty.
2. **Schema & Contract Conformance**:
   - If `artifacts/pr-evidence.json` is present, it must validate against `pr-evidence.schema.json` with `gates_passed: true` and `traceability_complete: true`.
3. **QA Verdict**:
   - QA review verdict in `artifacts/qa-verdict.json` or `artifacts/qa-verdict.md` must be `APPROVE` or `APPROVE_WITH_RISK`. Any unaddressed `REJECT` verdict blocks `ci_passed`.
4. **Command Execution Zero Exit Codes**:
   - All quality commands recorded in `artifacts/test-execution-raw.json` must have an exit code of `0`. Any non-zero exit code immediately blocks the transition (`failed:test_execution_command_exit_code`).
5. **Quality Gate Outcomes**:
   - If `.harness.yaml` declares `quality_gates` (e.g. `["test"]`), all gates must be present and evaluated as `true` in `artifacts/gate-result.json`.
