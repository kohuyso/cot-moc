# SRS: [Module Name]

> One file per module (`artifacts/srs/<module>.md`) for enterprise runs. Every FR below follows the depth contract
> in `sdlc-ba-analysis`. Replace every bracket; delete nothing that applies. A field that truly does not apply
> says "None" with the reason, it is not left out.

## Metadata
- **Module**: `[module name from .harness.yaml]`
- **Run ID**: `[run-id]`
- **Source documents and sections**: `[file: section, ...]`
- **Source IDs owned by this module**: `[count]` (listed individually in each FR's Sources line)
- **Status**: `DRAFT | SUBMITTED | REWORK | APPROVED`

## Module overview
[Two to five sentences: what this module is responsible for, who uses it, which other modules it depends on.]

## Glossary used in this module
| Term | Definition (no synonyms) |
|---|---|

---

## FR-[NNN]: [Title: one capability]
- **Sources**: `[UR-xxx-001, UR-xxx-002, BR-xx]` (each ID individually; no ranges)
- **Priority**: `P0 | P1 | P2 | P3`
- **Statement**: The system SHALL [one capability].
- **Actors and permissions**: [role: may ..., may not ...]
- **Preconditions**: [state and data that hold before it starts]

### Main flow
1. [Actor does X.]
2. [System validates Y and responds Z.]
3. [...]

### Alternate flows
- (a) [Variant: other role / other mode / optional step]: [what changes]

### Exception flows
- (a) [Failure or rejection or timeout]: [system response] / message `[text]` / error code `[ERR-XXX-nnnn]` / resulting state `[STATE]`
- (b) [...]

### Data
| Field | Type | Length / range | Mandatory | Default | Validation | Error |
|---|---|---|---|---|---|---|

### Business rules
- `[BR-xx]`: [rule as formula, table or decision list].
  **Worked example**: [inputs with real numbers] -> [result].

### State changes
| Entity | From | Event | To | Guard |
|---|---|---|---|---|

### Side effects
- Notifications: [who, when, channel]
- Audit: [event name, fields recorded]
- Integrations: [system, call, on failure ...]

### Acceptance criteria
1. **Given** [concrete state and values] **When** [action] **Then** [observable result with values].
2. **Given** [...] **When** [invalid input or failure] **Then** [rejection, message, code, state unchanged].

### NFR links
`[NFR-xxx-nn, ...]`

---

## Module NFRs
| ID | Characteristic | Target (number and unit) | Verification |
|---|---|---|---|

## Open questions for this module
| ID | Question | Owner | Status | Resolution (user-confirmed) |
|---|---|---|---|---|
