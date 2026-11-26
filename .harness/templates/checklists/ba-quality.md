# Requirements Quality Review Checklist: BA Deliverables

**Target Artifact**: `artifacts/requirement-analysis.md`
**Reviewer Role**: `sdlc-sa-review` / `sdlc-po-review`
**Marker Semantics**: Mark `[x]` only after confirming the requirement-quality criterion is satisfied. Leave `[ ]` if clarification or rework is needed.

---

## 1. Scope & Objective Clarity
- [ ] `CHK-BA-001`: Is the business objective quantified with measurable business impact rather than vague aspirations?
- [ ] `CHK-BA-002`: Are explicit Non-Goals documented to prevent scope creep during implementation?
- [ ] `CHK-BA-003`: Is the distinction between AS-IS (current state) and TO-BE (target state) unambiguous?

## 2. Requirement Completeness & Atomicity
- [ ] `CHK-BA-004`: Does every Functional Requirement possess a stable unique identifier (`FR-001`, `FR-002`...)?
- [ ] `CHK-BA-005`: Is every requirement atomic (specifies exactly one capability or business rule)?
- [ ] `CHK-BA-006`: Are all data entities, mandatory attributes, constraints, and formats explicitly listed?

## 3. Acceptance Criteria & Testability
- [ ] `CHK-BA-007`: Does every FR have at least one Given/When/Then acceptance scenario?
- [ ] `CHK-BA-008`: Are edge cases, null inputs, and boundary conditions explicitly specified with expected system responses?
- [ ] `CHK-BA-009`: Are error and failure flows defined with concrete domain error messages and status codes?
- [ ] `CHK-BA-010`: Can every acceptance criterion be validated deterministically by an automated test?

## 4. Vocabulary & Discipline
- [ ] `CHK-BA-011`: Are all domain nouns defined in the Glossary without conflicting synonyms?
- [ ] `CHK-BA-012`: Are unverified inferences tagged explicitly in the Assumptions Index (`ASM-xxx`) rather than stated as facts?
- [ ] `CHK-BA-013`: Are unknown requirements recorded as Open Questions (`OQ-xxx`) rather than guessed?

## 4b. Developer-Ready Depth (apply to every FR you open; an FR that fails any line is not done)
- [ ] `CHK-BA-017`: Does the FR list its source requirement IDs individually (no ranges, no "see URD")?
- [ ] `CHK-BA-018`: Is there a numbered main flow of at least 2 steps (actor action, system response)?
- [ ] `CHK-BA-019`: Are alternate flows given for every business variant (role, mode, optional step)?
- [ ] `CHK-BA-020`: Is there at least one exception flow with the system response, message or error code, and resulting state?
- [ ] `CHK-BA-021`: Does every input and output field have type, length or range, mandatory flag, default and validation?
- [ ] `CHK-BA-022`: Is every business rule a formula, table or decision list, with a worked example using real numbers?
- [ ] `CHK-BA-023`: Are state changes, notifications, audit events and integration side effects (with failure behaviour) stated?
- [ ] `CHK-BA-024`: Are there at least 2 Given/When/Then criteria with concrete values, one of them negative or boundary?
- [ ] `CHK-BA-025`: Is the text free of "fast", "appropriate", "as needed", "etc.", "similar to", "as per", "TBD"?
- [ ] `CHK-BA-026`: Dev-Ready Test: could a developer code and a tester test this FR from this entry alone, without asking anyone?

## 4c. Fit Between Sources and Specification
- [ ] `CHK-BA-027`: Is every source requirement ID traced to an FR or excluded with a user-confirmed reason (counts come from files, not claims)?
- [ ] `CHK-BA-028`: Does each module have its own SRS section and FSD section, with no module missing?
- [ ] `CHK-BA-029`: Is the SRS plus FSD of the same order of magnitude as the sources (a large source reduced to a short summary fails)?
- [ ] `CHK-BA-030`: Were the documents written for this run (run id, source versions and module names match; nothing carried over from another run)?
- [ ] `CHK-BA-031`: Does the RTM have one row per source ID, with coverage figures that match a count of those rows?

## 5. Enterprise & Large-Scale Project Protocol
- [ ] `CHK-BA-014`: For enterprise or multi-module projects, are requirements decomposed into clear feature modules rather than collapsed into a single monolithic FR?
- [ ] `CHK-BA-015`: If baseline documentation exists in the workspace (`srs/`, `fsd/`, `database/`, `prototype_design/`), has BA comprehensively audited and cross-referenced all of them against the input URD, identifying gaps, conflicts, and obsolete items in a baseline review report (`artifacts/baseline-review.md` or `artifacts/urd-traceability-and-reconciliation.md`)?
- [ ] `CHK-BA-016`: If no baseline exists, does BA deliver the complete specification quintet: (1) SRS, (2) FSD (`artifacts/fsd.md`), (3) Data Dictionary (`artifacts/data-dictionary.md`), (4) Integration Matrix (`artifacts/integration-matrix.md`), and (5) RTM (`artifacts/rtm.md`)?

