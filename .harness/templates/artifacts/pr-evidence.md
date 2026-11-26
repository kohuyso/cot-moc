# Pull Request Evidence Pack: [Feature / Change Title]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DDTHH:MM:SSZ]`
- **Author**: `sdlc-pr-evidence`
- **Target Branch**: `main | staging`
- **Feature Branch**: `[feature/branch-name]`
- **Harness Status**: `VERIFICATION_COMPLETE`

---

## 1. Executive Summary & Change Narrative
- **Change Purpose**: [What business or technical goal does this pull request achieve?]
- **Key Capabilities Added**:
  - [Capability 1 per FR-001]
  - [Capability 2 per FR-002]
- **Breaking Changes**: `None | Yes (described in Section 5)`

---

## 2. Gate Verification Evidence Matrix
*Machine-checkable summary compiled for deterministic harness gate evaluation:*

| Gate Name | Status | Artifact Reference | Verification Proof |
|---|---|---|---|
| `gate_ba_approval` | ✅ PASSED | `artifacts/requirement-analysis.md` | Approved by SA and PO |
| `gate_architecture_approval`| ✅ PASSED | `artifacts/architecture-review.md` | SA verdict APPROVE (Round 1) |
| `gate_implementation_plan` | ✅ PASSED | `artifacts/implementation-plan.md` | All tasks defined with TDD steps |
| `gate_code_review` | ✅ PASSED | `artifacts/code-review.md` | 0 BLOCKER, 0 HIGH findings |
| `gate_unit_tests` | ✅ PASSED | `artifacts/test-report.md#3.1` | Exit code 0, 100% pass |
| `gate_integration_tests` | ✅ PASSED | `artifacts/test-report.md#3.2` | Exit code 0, 100% pass |
| `gate_qa_verdict` | ✅ PASSED | `artifacts/qa-verdict.md` | QA verdict APPROVE |
| `gate_security_review` | ✅ PASSED | `artifacts/security-review.md` | 0 BLOCKER, 0 HIGH vulnerabilities |
| `gate_ci_pipeline` | ✅ PASSED | CI Runner Job `#12345` | Clean CI execution |

---

## 3. End-to-End Requirement Traceability
```json
{
  "FR-001": {
    "title": "User Registration",
    "architecture": ["AD-001"],
    "implementation": ["src/package/module.py:15-80"],
    "tests": ["TEST-001", "TEST-002"],
    "evidence": ["gate_unit_tests", "gate_qa_verdict"]
  },
  "FR-002": {
    "title": "Transaction Logging",
    "architecture": ["AD-002"],
    "implementation": ["src/package/logger.py:10-50"],
    "tests": ["TEST-003"],
    "evidence": ["gate_integration_tests", "gate_qa_verdict"]
  }
}
```

---

## 4. VCS Diff & File Impact Audit
- **Files Created**: `[file 1, file 2]`
- **Files Modified**: `[file 3]`
- **Files Deleted**: `[none]`
- **Total Lines**: `+[lines] / -[lines]`
- **Author Claims vs VCS Diff Verification**: `VERIFIED_MATCH`

---

## 5. Risk Assessment & Post-Deploy Monitoring
- **Deployment Plan**: [Standard automated pipeline deployment]
- **Rollback Procedure**: [Revert commit SHA, no database schema rollback required]
- **Telemetry to Monitor**: [Metrics dashboard URL / error rate thresholds]
- **Residual Risk**: [Documented and accepted by PO/Lead]

---

## 6. PR Publication Readiness
- **PR Title**: `feat(domain): [concise title conforming to conventional commits]`
- **PR Description**: [Standard formatted description ready for GitLab/GitHub]
- **Harness Transition Request**: `transition --action ci_passed` -> `PR_READY`
- **Governance Note**: *The harness never merges or deploys to production. Human approval is required to merge.*
