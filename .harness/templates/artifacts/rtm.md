# Requirements Traceability Matrix (RTM)

## Metadata
- **System**: [System Name]
- **Run ID**: `[run-id]`
- **Date**: [YYYY-MM-DD]
- **Author**: `sdlc-ba-analysis`
- **Reviewed By**: `sdlc-sa-review`, `sdlc-qa-review`
- **Standard Conformance**: `ISO/IEC/IEEE 29148:2018 §8.5 & IIBA BABOK Guide v3 §5.1 (Requirements Traceability)`

---

## 1. Bi-Directional Traceability Matrix (ISO 29148 §8.5)

> One row per individual source requirement ID (no ranges, no grouped rows). Replace the placeholder row.

| Source Clause (URD / Contract) | Stakeholder Need (BABOK v3) | Software Requirement (SRS FR/NFR) | Functional Design (FSD Screen / Action) | Data Entity / Table | Test Case (ISO 29119) | Implementation Artifact | Traceability Status |
|---|---|---|---|---|---|---|---|
| `[UR-xxx-001]` | [need, in one line] | `[FR-nnn]` | `[SCR-xxx-nn or section]` | `[entity]` | `[TC-xxx-nnn or planned: area]` | `[file once implemented, else -]` | `[Traced / Excluded: reason / Gap]` |

---

## 2. Requirements Traceability Coverage Metrics

| Metric | Target | Actual | Evaluation |
|---|---|---|---|
*Compute every figure from the table above (count rows). Do not type a percentage you did not count; `sdlc-harness trace-sources` prints the source figures.*

| Metric | Target | Actual (count / total) | Evaluation |
|---|---|---|---|
| **Source IDs traced to an FR** | 100% | `[n / N]` | `[ ]` |
| **Source IDs excluded with a user-confirmed reason** | listed | `[n]` | `[ ]` |
| **FRs with a main flow, an exception flow and 2+ acceptance criteria** | 100% | `[n / N]` | `[ ]` |
| **Out-of-scope items confirmed by the user** | 100% | `[n / N]` | `[ ]` |

---

## 3. Discrepancy & Orphan Analysis (BABOK v3 §5.1.4)
- **Unmapped Source Requirements**: `[list every ID, or "None" only if the count above is N / N]`
- **Orphan Functional Specifications**: `[list, or "None"]`
- **Retired / Superseded Requirements**: (e.g. `URD-GPS-005` - Old office check-in method was explicitly retired in URD v1.4 and marked deprecated in SRS).
