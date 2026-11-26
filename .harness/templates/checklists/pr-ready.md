# Pull Request Readiness Checklist

**Target Artifact**: `artifacts/pr-evidence.md`
**Reviewer Role**: `sdlc-pr-evidence` / Human Gatekeeper
**Marker Semantics**: Mark `[x]` only when all deterministic gate evidence is present.

---

## 1. Governance & Quality Gates Verification
- [ ] `CHK-PR-001`: Has requirements analysis been approved by both SA and PO?
- [ ] `CHK-PR-002`: Has solution architecture received an independent SA `APPROVE` verdict?
- [ ] `CHK-PR-003`: Has code review received an independent reviewer `APPROVE` verdict with 0 Blocker/High issues?
- [ ] `CHK-PR-004`: Have all unit and integration test suites executed with 100% pass rate?
- [ ] `CHK-PR-005`: Has independent QA issued a formal `APPROVE` verdict?
- [ ] `CHK-PR-006`: Is the security review clean with 0 Blocker/High vulnerabilities?

## 2. Traceability & Integrity
- [ ] `CHK-PR-007`: Is the machine-readable traceability mapping complete (`Requirement -> Code -> Tests -> Evidence`)?
- [ ] `CHK-PR-008`: Does the VCS diff match the approved scope without extraneous file changes?
- [ ] `CHK-PR-009`: Are rollback and monitoring instructions documented?
- [ ] `CHK-PR-010`: Is human approval confirmed prior to merging (harness never self-merges)?
- [ ] `CHK-PR-011`: Are runtime smoke test and configuration sanity verified with zero unmapped environment placeholders?
