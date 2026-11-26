# Architecture Review Findings: [Feature / Change Name]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DD]`
- **Reviewer**: `sdlc-sa-review`
- **Reviewed Artifacts**: `artifacts/requirement-analysis.md`, `artifacts/solution-design.md`
- **Review Round**: `[1 | 2]`
- **Verdict**: `APPROVE | PUSHBACK | ESCALATE`

---

## 1. Review Summary & High-Level Evaluation
[Independent critical assessment of the technical proposal. Does it preserve system integrity, prevent unnecessary complexity, and satisfy non-functional requirements?]

---

## 2. Review Findings & Challenges

### Finding ARC-001: [Title]
- **Category**: `Architecture Conformance | Interface Contract | Data Integrity | Resilience | Security | Performance`
- **Severity**: `BLOCKER | HIGH | MEDIUM | LOW | INFO`
- **Affected Section / Component**: `[e.g., AD-001 in solution-design.md / Service B]`
- **Identified Gap / Risk**: [Concrete technical critique: why will this fail under production conditions or diverge from architecture invariants?]
- **Required Correction**: [Exact modification required before approval]

### Finding ARC-002: [Title]
- **Category**: `Interface Contract`
- **Severity**: `HIGH`
- **Affected Section / Component**: `[e.g., §4.1 API Contracts]`
- **Identified Gap / Risk**: [e.g., Missing backward compatibility for existing clients]
- **Required Correction**: [Version the endpoint or preserve existing optional fields]

---

## 3. Rubric Evaluation
| Architecture Dimension | Evaluation | Comments |
|---|---|---|
| **User Intent & Clarification Integrity** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Verify fidelity to original request.md; zero open questions remain; all assumptions confirmed] |
| **System Boundaries & Coupling** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **API & Contract Compatibility** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **Data Ownership & Persistence** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **Failure Modes & Resilience** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **NFR Feasibility (Latency/Scale)** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **Security & Privacy Posture** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |
| **Observability & Operability** | ✅ Pass / ⚠️ Concern / ❌ Fail | [Comments] |

---

## 4. Decision & Handoff
- **User Intent Verified**: `[true | false]`
- **Unresolved Open Questions Count**: `[0 | N]`
- **Final Verdict**: `[APPROVE | PUSHBACK | ESCALATE]`
- **Next Transition Action**:
  - If `APPROVE`: Request transition `approve` (to `SA_DESIGN` or next phase).
  - If `PUSHBACK`: Request transition `pushback` with `loop="BA_SA"` (round `[N]` of 2).
  - If `ESCALATE`: Output `artifacts/escalation-report.md` if retry ceiling is reached.
