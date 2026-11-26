# SDLC Intake: [Change or Feature Title]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DD]`
- **Intake Author**: `[Role / Agent ID]`
- **Target Project**: `[Project Name / Path]`
- **Status**: `DRAFT | ACCEPTED | REJECTED`

## 1. Raw User Request
```text
[Exact verbatim user prompt or issue description without modification]
```

## 2. Business Context & Problem Statement
- **Background**: [Why is this change being requested? What problem does it solve?]
- **Stakeholders**: [Who requested this? Who are the primary end users? Who maintains this?]
- **Expected Business Outcome**: [What is the intended benefit or business value?]

## 3. Scope Boundary (Initial)
- **In-Scope**:
  - [Core capability or defect fix 1]
  - [Core capability or defect fix 2]
- **Explicit Non-Goals (Out-of-Scope)**:
  - [Nearby capability explicitly excluded from this increment]
  - [Unrelated refactoring or redesign excluded]

## 4. Known Constraints & Dependencies
- **Technical Constraints**: [Language version, database, framework, infrastructure limits]
- **Security & Compliance Requirements**: [Data privacy, auth requirements, audit logs if known]
- **Target Systems / Repositories**: [List of affected code repositories or subsystems]

## 5. Intake Clarifications & Open Questions
- **Q-001**: [Clarification question raised during intake] — *Answer / Status: [Resolved / Open]*
- **Q-002**: [Clarification question raised during intake] — *Answer / Status: [Resolved / Open]*

## 6. Downstream Handoff Recommendation
- **Recommended Path**: `FAST_PATH` (Defect/Small fix) | `STANDARD_SDLC` (Feature/Change)
- **Next Role**: `sdlc-ba-analysis`
- **Handoff Artifact**: `artifacts/intake.md`
