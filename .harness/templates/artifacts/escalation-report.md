# Escalation Report: [Issue / Deadlock Title]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DDTHH:MM:SSZ]`
- **Escalated By**: `[Role / Agent ID]`
- **Escalation Reason**: `RETRY_LIMIT_EXHAUSTED | UNRESOLVED_ARCHITECTURAL_CONFLICT | BLOCKING_EXTERNAL_DEPENDENCY`
- **Exhausted Loop**: `BA_SA (2 rounds) | DEV_REVIEW (3 rounds) | TEST_QA (3 rounds)`
- **Escalation Target**: `Human Approver / Engineering Lead`

---

## 1. Executive Summary & Deadlock Context
[Concise 1-2 paragraph description of the disagreement or failure pattern that caused the workflow to reach its retry ceiling. Explain why autonomous resolution was not possible without human guidance.]

---

## 2. Failure History & Iteration Audit

### Iteration 1
- **Producer Output**: [What was delivered]
- **Reviewer Critique**: [Why it was pushed back]
- **Attempted Resolution**: [What changes were made]

### Iteration 2
- **Producer Output**: [What was delivered]
- **Reviewer Critique**: [Why it was pushed back]
- **Attempted Resolution**: [What changes were made]

### Iteration 3 (if applicable)
- **Producer Output**: [What was delivered]
- **Reviewer Critique**: [Why it was pushed back]
- **Result**: Retry ceiling exhausted.

---

## 3. Root Cause Analysis
- **Underlying Cause**: `Ambiguous Requirement | Conflicting Technical Constraints | Legacy System Incompatibility | Scope Too Large`
- **Detailed Diagnosis**: [Explain the root technical or business divergence]
- **Is this a systemic or one-off issue?**: [Assessment]

---

## 4. Proposed Resolution Options
| Option | Description | Trade-offs & Risks | Recommended? |
|---|---|---|---|
| **Option A (Decompose)** | Split task into smaller independent sub-tasks | Extends schedule slightly, simplifies implementation | ⭐ Recommended |
| **Option B (Revise Architecture)** | Modify baseline architecture decision `AD-xxx` | Requires architectural re-review, solves root blocker | Viable |
| **Option C (Accept Limitation)** | Waive specific NFR / edge case with documented risk | Quickest path, leaves known minor limitation | Low priority only |
| **Option D (Abort / Rollback)** | Reject change and revert run state | Protects baseline, drops requested capability | Fallback |

---

## 5. Impact Assessment & Decision Required
- **Blocked Work**: [Which downstream tasks or teams are paused awaiting this decision]
- **Action Required From Human**: [Exact command or manual approval required to resume harness]
