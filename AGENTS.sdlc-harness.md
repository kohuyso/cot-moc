# SDLC Harness Agent Instructions & Routing Protocol

## Core Governance Principles
1. **Single Writer of State**: Only the SDLC Harness Controller mutates run state (`.harness/runs/<run-id>/state.json`) and writes events (`events.jsonl`). Agents MUST NOT edit state files directly.
2. **Producer / Challenger Separation**: Deliverables created by producer roles are strictly reviewed by independent challenger roles. Zero self-approval is permitted. The orchestrating agent MUST NOT write `sa-review.json`, `design-verdict.json`, `test-verdict.json`, `code-review.json`, `qa-verdict.json` or `security-review.json` itself: run `sdlc-harness review --run-id <id>`, which starts the configured reviewer CLI as a separate process and seals its verdict. Large/enterprise runs are rejected unless `require_harness_review`, `require_tech_review` and `require_test_design` are on.
3a. **Own Work Only**: Every deliverable is written in this run from the sources. Copying `fsd.md`, `rtm.md`, designs or any artifact from another run is rejected (`reused_artifact`, `foreign_run_artifact`); inherit earlier work with `fork-run`. When `requirement_sources` is configured, every source requirement ID must be traced individually in `requirement.json`.
3b. **Missing Skill = Stop**: Each phase names its role skill (`sdlc-harness next --run-id <id>`). If the skill is not available to you, stop and tell the user; never improvise the role.
3. **Evidence-Based Gating**: Transitions require validated physical artifacts, passing schemas, and zero non-zero command exit codes.
4. **Autonomous Convergence Inner Loop (Loop-until-Green)**: During `DEV_CODING` and test remediation, agents MUST autonomously loop (fix code/fixtures -> rerun test runner) until all tests pass (`dotnet test` exit code 0). Agents are strictly forbidden from conversational turn-yielding or pausing between individual fixes to report incremental status to the user. Complete convergence is required before advancing.
5. **No Generated Artifacts**: Every file under `artifacts/` is written by the role skill from the sources. Writing a script that loops over `requirement.json` (or any list) to emit plans, designs, test cases or reviews is a violation of Own Work Only, whatever the script is called; the gates measure templated output (`templated_test_steps`, `plan_missing_requirement_coverage`, `reviewer_claim_mismatch`) and reject it.
6. **Reviewer Unavailable = Stop**: When `sdlc-harness review` fails (`reviewer_exit_code`, `reviewer_no_usage_evidence`, `reviewer_command_not_independent`, `reviewer_too_fast`), report it to the user and stop. Never change `reviewers`, never point the reviewer at a script in this project, never write the verdict file. The harness records every refusal (`REVIEW_REFUSED`).
7. **Gates Are Floors, Not Targets**: The completion criteria of a phase are the role skill and `sdlc-harness next`. Reading the harness source (`gates.py`) to find the minimum that passes, then producing exactly that, is a violation; a 20-character plan that passes a size check is still an empty plan.

---

## SDLC Controller CLI Usage
All workflow transitions and state queries MUST go through the Controller CLI:

1. **Initialize a Run (`init-run` or `start`)**:
   ```bash
   python -m sdlc_harness.cli init-run --project <project_path> --run-id <run_id> --request "<description>" [--mode new_build|maintain_upgrade]
   ```
2. **Query Run Status (`status`)**:
   ```bash
   python -m sdlc_harness.cli status --project <project_path> --run-id <run_id>
   ```
3. **Execute Allowlisted Quality Gate (`run-gate`)**:
   ```bash
   python -m sdlc_harness.cli run-gate --project <project_path> --run-id <run_id> --gate <command_key>
   ```
4. **Request Phase Transition (`transition`)**:
   ```bash
   python -m sdlc_harness.cli transition --project <project_path> --run-id <run_id> --action <action_name> [--loop <loop_name>]
   ```

---

## Operating Modes: `new_build` vs `maintain_upgrade`
- **`new_build`**: Green-field projects or standalone modules. Follows the standard pipeline from intake to PR evidence.
- **`maintain_upgrade`**: Modifications to existing codebases.
  - **Mandatory Precondition**: Prior to executing `submit_srs` from `BA_DRAFT` or `BA_REWORK`, the role MUST create `artifacts/impact-analysis.md` assessing blast radius, existing callers, backwards compatibility, and regression risks.

---

## Bounded Review Loops & Escalation
Review loops enforce strict round ceilings to eliminate infinite debates:
- **`BA_SA` (Requirements & System Architecture)**: Maximum 2 rounds.
- **`TECH_REVIEW` (Solution Design & Architectural Review)**: Maximum 2 rounds.
- **`UI_REVIEW` (UI Prototype & Interactive Visual Verification)**: Maximum 2 rounds.
- **`TEST_DESIGN_REVIEW` (Shift-Left Test Case Coverage & RTM Audit)**: Maximum 2 rounds.
- **`DEV_REVIEW` (Implementation & Code Review)**: Maximum 3 rounds.
- **`TEST_QA` (Test Execution & QA Verification)**: Maximum 3 rounds.
- **`SECURITY_REVIEW` (Application Security & Vulnerability Audit)**: Maximum 3 rounds.

When a retry ceiling is exhausted:
1. The active challenger issues `pushback`, which triggers automatic escalation to `HUMAN_APPROVAL`.
2. The active role must generate `artifacts/escalation-report.md` detailing disagreement history, root cause, and remediation options.
3. Automated transitions are halted until human intervention resolves the impasse.

---

## Modular Architecture & Fork-Join Support
For projects configured with `architecture: {style: modular_monolith | microservices}`:
1. **WBS Plans**: Can be submitted as separate modules under `artifacts/plans/plan-<module_or_service>.md`.
2. **Parallel Services Fork-Join**:
   - In `DEV_CODING`, each service submits independently: `transition --action submit_diff --service <service_name>`.
   - In `CODE_REVIEW`, each service is reviewed and approved independently: `transition --action approve --service <service_name>`.
   - The state machine automatically joins all services before advancing to `TEST_EXECUTION`.
3. **Architectural Fitness Gates**:
   - For Modular Monolith: Directly coupling to another module's internal namespaces (`.internal`, `/internal/`) is rejected.
   - For Microservices: Cross-database foreign keys in migration/DDL scripts (`references db_`, `references service_`) are strictly rejected.

---

## Human Governance & Decision Actions
When a run enters `HUMAN_APPROVAL`, human operators resolve the escalation using `human_decision`:
- `ACCEPT_RISK`: Resolves review disagreement and advances to target phase (`approver`, `reason`, and `evidence_ref` required). Cannot waive deterministic failures.
- `GRANT_EXTENSION`: Grants exactly 1 retry extension per loop (`max_extensions_per_loop: 1`).
- `REJECT_AND_CLOSE`: Terminates the run and marks phase as `CLOSED`.

CLI Command:
```bash
python -m sdlc_harness.cli transition --project <project_path> --run-id <run_id> --action human_decision --disposition ACCEPT_RISK|GRANT_EXTENSION|REJECT_AND_CLOSE --approver <name> --reason "<reason>" --evidence-ref "<ref>"
```

---

## Role Skills and Local Artifacts
Role skills are installed per user under `~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills` and `~/.gemini/config/skills` (`<skill-name>/SKILL.md`).
Offline templates, checklists, and schemas are located under `.harness/templates/`.
Deliverables and evidence reside under `.harness/runs/<run-id>/artifacts/`.
