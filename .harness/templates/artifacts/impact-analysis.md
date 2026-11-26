# Maintain & Upgrade Impact Analysis: [System / Change Title]

## Metadata
| Field | Value |
|---|---|
| **Run ID** | `[run-id]` |
| **Change Type** | `bugfix | refactor | enhancement | upgrade` |
| **System** | `[target-system-name]` |
| **Author** | `[author-role, e.g. sdlc-ba-analysis / sdlc-sa-design]` |
| **Date** | `[YYYY-MM-DD]` |
| **Status** | `DRAFT | REVIEWED | APPROVED` |

---

## 1. Scope & Intent of Modification
- **Problem Statement / Trigger**: [Describe the incident, tech debt, upstream dependency change, or feature request motivating this modification]
- **Modification Objective**: [Clear statement of desired outcome and what behavior is being added, fixed, or updated]
- **Target Components / Repositories**: [List specific services, packages, libraries, or directories directly affected]
- **Out of Scope**: [Explicit boundaries — what is intentionally NOT being touched]

---

## 2. Blast Radius & Call Hierarchy
### 2.1 Direct Call Hierarchy
- **Caller Modules (Upstream)**:
  - `[Module/Service A]`: [How it invokes the modified component, call frequency, dependency type]
  - `[Module/Service B]`: [How it invokes the modified component, call frequency, dependency type]
- **Callee Dependencies (Downstream)**:
  - `[Dependency X]`: [External APIs, shared libraries, microservices consumed]
  - `[Dependency Y]`: [Third-party SDKs, platform services]

### 2.2 Affected Endpoints & Public Interfaces
| Endpoint / Interface | Method / Signature | Change Nature | Invariant Preservation |
|---|---|---|---|
| `/api/v1/[resource]` | `POST` | Signature unchanged / payload extended | Existing clients receive identical response shape |
| `[ClassName.method]` | `(arg1: str) -> bool` | Internal logic modified | Error conditions unchanged |

---

## 3. Data & Storage Schema Impact
### 3.1 Database & Persistence Alterations
- **Tables / Collections**: `[table_name or N/A]`
- **Column / Field Modifications**:
  - `[column_name]`: `[type, nullable, default value, migration requirement]`
- **Indexes & Query Performance**: [Impact on query execution plans or existing indexes]

### 3.2 Serialization, Wire Format & Cache Invariants
- **Serialization Formats**: [JSON, Protobuf, Avro impacts — enum changes, optional/required fields]
- **Cache Keys & Invalidation**:
  - Cache Key Pattern: `[cache:prefix:{id}]`
  - Invalidation Strategy: [TTL expiration, explicit purge on write, versioned key prefix]

---

## 4. Integration & Contract Compatibility
- **Breaking Changes**: `YES | NO`
- **Backward Compatibility Evaluation**:
  - [Explain how older clients or consumers continue functioning without forced simultaneous deployment]
- **Wire Contract Compatibility**:
  - [Field deprecation policy, tolerant reader compliance, dual-write or transitional fallbacks]
- **Partner / Third-Party Integration Impact**:
  - [External consumers, webhooks, upstream vendor APIs affected]

---

## 5. Security & Compliance Implications
- **Authentication & Authorization**:
  - [Are permission checks, RBAC roles, or token validation touched?]
- **Data Privacy & Classification**:
  - [Does this change process PII, secrets, credentials, or sensitive data?]
- **Attack Surface Modification**:
  - [New inputs, deserialization points, network endpoints, or external dependencies]
- **Audit & Compliance Invariants**:
  - [Logging requirements, audit trail preservation, regulatory considerations]

---

## 6. Rollback & Contingency Strategy
- **Rollback Mechanism**: `Automated Canary Abort | Feature Flag Toggle | Blue-Green Switch | Manual Git Revert`
- **Data Rollback Feasibility**:
  - [Can migrations be reversed without data loss? Is dual-read/dual-write needed during cutover?]
- **Detection & Trigger Criteria**:
  - Error rate threshold: `> 1% error rate over 5 minutes`
  - Latency SLA: `p95 > 250ms`
- **Contingency Action Steps**:
  1. [Step 1: Disable feature flag or trigger deployment rollback]
  2. [Step 2: Verify traffic drains cleanly to previous version]
  3. [Step 3: Post-incident telemetry verification]

---

## 7. Verification & Regression Test Matrix
| Verification Layer | Target Scope | Test Suite / Command | Pass Criteria |
|---|---|---|---|
| **Unit Tests** | Modified functions & edge cases | `pytest tests/unit/` | 100% pass, no test skips |
| **Integration Tests** | Blast radius boundaries & callee APIs | `pytest tests/integration/` | All contract fixtures pass |
| **Regression Suite** | Existing callers & unchanged endpoints | `pytest tests/regression/` | Zero regression failures |
| **Performance / Smoke** | Latency & resource consumption | `locust / k6 / smoke check` | Within baseline thresholds |
