# Implementation Plan Review Checklist

**Target Artifact**: `artifacts/implementation-plan.md`
**Reviewer Role**: `sdlc-sa-review` / `sdlc-code-review`
**Marker Semantics**: Mark `[x]` only when the plan's feasibility and structure are satisfied.

---

## 1. Scope & File Confinement
- [ ] **Bao phủ yêu cầu**: số FR trong `requirement.json` = __; số FR được nêu tên trong một task = __ (phải bằng nhau; gate `plan_missing_requirement_coverage`).
- [ ] **Độ mịn task**: số task = __ ≥ ceil(FR / `quality_floor.plan_requirements_per_task`) = __; không task nào là "Module X" chung chung; mỗi task ≤ ~6 file `Create`/`Modify`.
- [ ] `sdlc-harness verify-plan --run-id <id>` output đính kèm, `passed: true`.
- [ ] `CHK-PLN-001`: Does every task declare exact file paths for creation, modification, and test coverage?
- [ ] `CHK-PLN-002`: Is the plan free of vague instructions like "handle edge cases", "add validation", or "write tests"?
- [ ] `CHK-PLN-003`: Are task boundaries right-sized so each task yields an independently testable deliverable?

## 2. Interface Contracts & Dependency Ordering
- [ ] `CHK-PLN-004`: Does every task specify explicit `Consumes` and `Produces` signatures and data models?
- [ ] `CHK-PLN-005`: Are tasks strictly ordered as an acyclic graph (DAG) where prerequisites execute first?
- [ ] `CHK-PLN-006`: Are method names and type signatures consistent across all neighboring tasks?

## 3. TDD & Verification Granularity
- [ ] `CHK-PLN-007`: Does every code task include explicit test-first steps (write failing test -> verify fail -> implement -> verify pass)?
- [ ] `CHK-PLN-008`: Are exact terminal verification commands provided for unit, integration, and linting suites?
- [ ] `CHK-PLN-009`: Does the Review Focus highlight the top 3-5 real-world failure modes for implementers?
- [ ] `CHK-PLN-010`: Is the plan proportioned appropriately (not an entire transcript of source code)?
