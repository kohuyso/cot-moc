# Technical Design Review Checklist: Independent Challenger Audit

**Target Artifacts**: `artifacts/solution-design.md`, `artifacts/decision-register.md`
**Reviewer Role**: `sdlc-tech-design-review` (Independent Architecture Challenger)
**Marker Semantics**: Mark `[x]` only after confirming the technical criterion is satisfied.

---

## 1. API Contract & Functional Completeness
- [ ] **Đếm thật**: số path trong `openapi.yaml` = __ (ghi vào `endpoints_reviewed`); số mã `API-*` của nguồn yêu cầu có `x-source-ref` = __/__; số bảng `tbl_*` trong data dictionary = __ (ghi vào `tables_reviewed`). Harness đối chiếu hai con số này.
- [ ] `CHK-TDR-001`: Does every user action and business flow in FSD have at least one explicit API endpoint in `solution-design.md`?
- [ ] `CHK-TDR-002`: Do request/response payloads cover 100% of mandatory input fields and business validation rules?
- [ ] `CHK-TDR-003`: Are domain error codes (`ERR-xxx`) from FSD mapped to concrete HTTP error responses (400, 404, 409, 422)?
- [ ] `CHK-TDR-004`: Does the API design enforce idempotency keys on all non-idempotent state-mutating requests (POST / PUT)?

## 2. Physical Database Schema & Data Integrity
- [ ] `CHK-TDR-005`: Are all business entities from `data-dictionary.md` materialized into concrete database tables?
- [ ] `CHK-TDR-006`: Are primary keys, foreign keys, and referential actions (CASCADE / RESTRICT) explicitly defined?
- [ ] `CHK-TDR-007`: Are appropriate B-tree or unique indexes specified for query filtering (especially high-frequency foreign keys and tenant codes)?
- [ ] `CHK-TDR-008`: Does every business table include multi-tenant scoping columns (`cttv_code` / `tenant_id`) where applicable?

## 3. Resilience, Distributed Patterns & NFR Realization
- [ ] `CHK-TDR-009`: Does the design avoid holding SQL transactions open during remote external service invocations (e.g. ePayment, Maps)?
- [ ] `CHK-TDR-010`: Is asynchronous integration backed by a persistent Outbox / Inbox worker with bounded exponential retries and dead-letter queues?
- [ ] `CHK-TDR-011`: Are throughput and p95 latency targets realistically supported by the caching and query execution plan?

## 4. Security Architecture & Threat Surface (STRIDE / OWASP)
- [ ] `CHK-TDR-012`: Are authentication handshakes, token scopes, and RBAC / ABAC authorization guards explicitly specified on every endpoint?
- [ ] `CHK-TDR-013`: Are credentials and API secrets isolated into secure vaulting / environment variables with zero hardcoded tokens?
- [ ] `CHK-TDR-014`: Are sensitive columns (passwords, payment tokens, PII) protected via hashing / Always Encrypted?

## 5. Architectural Invariants & ADR Register
- [ ] `CHK-TDR-015`: Are all critical architectural decisions documented in `artifacts/decision-register.md` (`AD-xxx`) with clear Binds / Prevents?
- [ ] `CHK-TDR-016`: Does the independent reviewer provide an unambiguous recommendation for the human decision-maker?

## 6. Boundaries, Compatibility & Operability
- [ ] `CHK-TDR-017`: Are impacted modules explicitly identified with clear boundary invariants, and does the design avoid tight coupling, leaky abstractions and circular dependencies?
- [ ] `CHK-TDR-018`: Are existing subsystem responsibilities respected, and is the design brownfield-compatible with existing frameworks and database engines?
- [ ] `CHK-TDR-019`: Is backward compatibility preserved for existing clients, or is a versioning strategy defined?
- [ ] `CHK-TDR-020`: Is data ownership clear (single source of truth for every persistent entity)?
- [ ] `CHK-TDR-021`: Are database migrations safe, indexed appropriately and rollback-capable?
- [ ] `CHK-TDR-022`: Are structured logging, trace propagation and health-check endpoints accounted for?
- [ ] `CHK-TDR-023`: Are OWASP Top 10 mitigations specified (parameterized queries, anti-CSRF, input validation, output encoding)?
- [ ] `CHK-TDR-024`: Does the deliverable include the HLD views (logical, process/sequence, physical/deployment) and technical specifications per module?

## 7. Design Traceability & Anti-Slop (apply only when `design_traceability` is enabled for the project)
- [ ] `CHK-TDR-025`: Are there zero placeholders (`...`, `TODO`, `TBD`, "to be updated later")? Every table and section contains a complete specification.
- [ ] `CHK-TDR-026`: Does the traceability matrix map each requirement to a REAL, distinct operation or handler and to a table that exists in the data model, with no single value dominating more than the configured share of rows?
- [ ] `CHK-TDR-027`: Is every state machine extracted from an authentic lifecycle of the requirements (real status names, triggers, guards) rather than boilerplate init/target states?
- [ ] `CHK-TDR-028`: Does the error/message catalog map every message of the requirements to a unique code, a realistic HTTP status (not one status for all) and specific remediation guidance?
- [ ] `CHK-TDR-029`: Does every requirement entity map to an explicit table, or to a column of an explicitly named existing parent table? No phantom entities, no vague phrases such as "embedded in aggregate".
- [ ] `CHK-TDR-030`: Does the contract file (OpenAPI/AsyncAPI) parse strictly without swallowed errors, with every operation declaring security and a 4xx error response?
