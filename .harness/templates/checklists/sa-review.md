# Architecture Review Checklist: Solution Architecture & Technical Design

**Target Artifacts**: `artifacts/solution-design.md`, `artifacts/architecture-review.md`
**Reviewer Role**: `sdlc-sa-review`
**Marker Semantics**: Mark `[x]` only after confirming the architectural criterion is verified.

---

## 1. System Context & Component Boundaries
- [ ] `CHK-SA-001`: Are impacted modules explicitly identified with clear boundary invariants?
- [ ] `CHK-SA-002`: Does the design avoid tight coupling, leaky abstractions, or circular dependencies?
- [ ] `CHK-SA-003`: Are existing subsystem responsibilities respected without creating architectural god-nodes?

## 2. Architectural Decisions & Invariants
- [ ] `CHK-SA-004`: Does every Architecture Decision (`AD-xxx`) declare its `Binds`, `Prevents`, and `Enforceable Rule`?
- [ ] `CHK-SA-005`: Are considered alternatives documented with explicit, objective technical reasons for rejection?
- [ ] `CHK-SA-006`: Is the solution brownfield-compatible with existing frameworks and database engines?

## 3. Interfaces, Persistence & Backward Compatibility
- [ ] `CHK-SA-007`: Are API endpoints and internal signatures strictly typed with input validation?
- [ ] `CHK-SA-008`: Is backward compatibility preserved for existing clients, or is a versioning strategy defined?
- [ ] `CHK-SA-009`: Is data ownership clear (single source of truth for persistent entities)?
- [ ] `CHK-SA-010`: Are database migrations safe, indexed appropriately, and rollback-capable?

## 4. Resilience & NFR Realization
- [ ] `CHK-SA-011`: Are failure modes for external dependencies handled via timeouts, fallbacks, or circuit breakers?
- [ ] `CHK-SA-012`: Does the design demonstrate concrete mechanisms to meet throughput and latency NFRs?
- [ ] `CHK-SA-013`: Are structured logging, trace propagation, and health check endpoints accounted for?

## 5. Security Architecture & Threat Surface (STRIDE / OWASP)
- [ ] `CHK-SA-014`: Does `solution-design.md` explicitly model the threat surface, authentication handshakes, token validation, and RBAC/ABAC authorization guards?
- [ ] `CHK-SA-015`: Are secrets, API keys, and credentials completely isolated via environment variables / KMS, and sensitive data encrypted at rest and in transit?
- [ ] `CHK-SA-016`: Are OWASP Top 10 mitigations specified (parameterized queries for SQL injection, anti-CSRF tokens, input validation, rate limiting)?
- [ ] `CHK-SA-017`: Does the deliverable include full IEEE 1016 / Kruchten 4+1 HLD views (Logical, Process/Sequence, Physical) and TSD specifications (API & DB schemas)?

## 6. User Intent & Clarification Integrity
- [ ] `CHK-SA-018`: Has the SRS been cross-referenced against the raw request (`request.md`) to verify zero scope distortion or unauthorized feature omission?
- [ ] `CHK-SA-019`: Are 100% of open questions in `requirement.json` verified to have `status == "RESOLVED"`?
- [ ] `CHK-SA-020`: Have all technical and business assumptions been confirmed by the user (`confirmed_by_user == true`) rather than fabricated by the author?

## 7. Enterprise Deliverable & Adversarial Review
- [ ] `CHK-SA-021`: Has SA reviewed the complete quintet (SRS, FSD, Data Dictionary, Integration Matrix, RTM) or the comprehensive baseline review artifact (`artifacts/baseline-review.md` / `artifacts/urd-traceability-and-reconciliation.md`)?
- [ ] `CHK-SA-022`: Are FSD state machines, form validation rules, and domain error codes validated for deadlocks, race conditions, and UX completeness?
- [ ] `CHK-SA-023`: Are Data Dictionary entities, field types, and constraints verified against database scaling, normalization, and index strategy?
- [ ] `CHK-SA-024`: Are all external systems in the Integration Matrix challenged with concrete failure modes (timeouts, network partitions, idempotent retries, outbox reconciliation)?
- [ ] `CHK-SA-025`: Does SA issue a strict PUSHBACK if an enterprise project was collapsed into a single superficial requirement without detailed specification or baseline audit?
- [ ] `CHK-SA-026`: Mọi màn hình tương tác trong FSD có đầy đủ Bảng danh mục trường (Field Inventory Table), Nguồn Master Data và Ánh xạ Bảng DB hay không? Nếu thiếu, BẮT BUỘC đánh lỗi mức BLOCKER và PUSHBACK.



