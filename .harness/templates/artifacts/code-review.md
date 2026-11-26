# Code Review Report: [Feature / Change Name]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DD]`
- **Reviewer**: `sdlc-code-review`
- **Reviewed Commit / Diff**: `[commit-sha | git diff baseline]`
- **Review Round**: `[1 | 2 | 3]`
- **Verdict**: `APPROVE | PUSHBACK | ESCALATE`

---

## 1. Scope & Diff Summary
- **Files Changed**: `[N] files (+[lines] / -[lines])`
- **Declared Scope Adherence**: `[Compliant | Unintended Files Changed]`
- **Author Claims vs Actual Diff**: [Did the author deliver what was claimed without undeclared additions?]

---

## 2. Scope & Requirement Implementation Matrix (scope_coverage)

*Every functional requirement (`FR-xxx`) from `artifacts/requirement-analysis.md` / `requirement.json` must be cross-checked against the actual code diff. If any requirement is missing or incomplete, verdict must be `PUSHBACK` with loop `DEV_REVIEW`.*

| Requirement ID | Description / Feature | Implemented? | Evidence Files & Symbol References | Scope Notes |
|---|---|---|---|---|
| **FR-001** | [Core feature, e.g. Payment Authorization & Idempotency] | ✅ Yes | `src/payments/service.py:40-95`, `src/payments/router.py:15-38` | Fully implemented with request validation and idempotency key checking |
| **FR-002** | [Management route, e.g. Timeout Transaction Cron Reconciliation] | ✅ Yes | `src/payments/reconciliation.py:20-65` | Concrete cron worker implemented without stubs |
| **FR-003** | [Admin Panel / UI View] | ❌ No | *(None found in diff)* | Missing UI route and view component (triggers PUSHBACK) |

### Machine-Readable Scope Coverage (`code-review.json`)
The companion file `artifacts/code-review.json` must record `scope_coverage` matching the matrix above:

```json
{
  "reviewer_role": "sdlc-code-review",
  "verdict": "APPROVE",
  "round": 1,
  "summary": "Implementation satisfies all functional requirements with clean boundary adherence.",
  "scope_coverage": {
    "FR-001": {
      "implemented": true,
      "evidence_files": [
        "src/payments/service.py",
        "src/payments/router.py"
      ],
      "notes": "Payment authorization endpoint and idempotency check fully wired"
    },
    "FR-002": {
      "implemented": true,
      "evidence_files": [
        "src/payments/reconciliation.py"
      ],
      "notes": "Cron reconciliation job implemented"
    }
  },
  "findings": []
}
```

> [!IMPORTANT]
> **Adversarial Gate Rule**: If any requirement has `"implemented": false` or is omitted from the diff, `verdict` MUST be `"PUSHBACK"` and reviewer MUST invoke `sdlc pushback --loop DEV_REVIEW` with an actionable finding.

---

## 3. Structured Findings

### Finding CR-001: [Title]
- **Severity**: `BLOCKER | HIGH | MEDIUM | LOW | INFO`
- **Category**: `Correctness | Regression Risk | Security | Architecture Conformance | Error Handling | Test Coverage`
- **File & Line**: `src/package/module.py:42-58`
- **Description**: [Detailed technical explanation of the defect or regression risk]
- **Evidence / Proof**: [Code snippet, edge-case input triggering failure]
- **Required Remediation**: [Actionable fix instruction for the implementer]

### Finding CR-002: [Title]
- **Severity**: `HIGH`
- **Category**: `Error Handling`
- **File & Line**: `src/package/handler.py:112`
- **Description**: [Uncaught exception on empty network response]
- **Required Remediation**: [Wrap call in try/except block returning domain error]

---

## 4. Review Checklist & Evaluation Matrix
| Evaluation Dimension | Verdict | Evidence / Notes |
|---|---|---|
| **Requirement Coverage** | ✅ Pass / ❌ Fail | All FRs from approved plan implemented |
| **Correctness & Edge Cases** | ✅ Pass / ❌ Fail | Edge cases handled cleanly |
| **Regression Risks** | ✅ Pass / ❌ Fail | Existing callers unaffected, deletion check clean |
| **Architecture Conformance**| ✅ Pass / ❌ Fail | Follows AD rules and component boundaries |
| **Security & Data Safety** | ✅ Pass / ❌ Fail | Inputs sanitized, no secret leakage |
| **Test Quality & Coverage** | ✅ Pass / ❌ Fail | Real assertions present, tests fail without fix |
| **Maintainability** | ✅ Pass / ❌ Fail | Clean naming, no dead code or debug logs |

---

## 5. Decision & Handoff
- **Verdict**: `[APPROVE | PUSHBACK | ESCALATE]`
- **Next Action**:
  - If `APPROVE`: Request transition `approve` (proceed to `TEST_EXECUTION`).
  - If `PUSHBACK`: Request transition `pushback` with `loop="DEV_REVIEW"` (attempt `[N]` of 3). Implementer must remediate only listed findings.
  - If `ESCALATE`: Output `artifacts/escalation-report.md` (3 attempts exhausted).
