# Security & Risk Review: [Feature / Change Name]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DD]`
- **Reviewer**: `sdlc-security-review`
- **Scope**: `[Diff, Architecture Spec, Dependencies]`
- **Risk Profile**: `LOW (Internal/Refactor) | MEDIUM (API/Data) | HIGH (Auth/Payment/PII)`
- **Verdict**: `APPROVE | PUSHBACK | ESCALATE`

---

## 1. Security Context & Threat Surface
- **Change Characterization**: [e.g., Adding new REST API endpoint with user authentication]
- **Threat Surface Exposed**: [Public internet, internal microservice network, admin boundary]
- **Data Sensitivity**: [None | Internal | Confidential | PII / Financial]

---

## 2. Security Assessment by Control Domain

| Security Domain | Status | Observations / Evidence |
|---|---|---|
| **Authentication & Identity** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | Session/token handling verified |
| **Authorization & Access Control** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | Principle of least privilege enforced |
| **Input Validation & Sanitization** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | Parameterized queries, schema boundary |
| **Secrets & Credential Hygiene** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | No hardcoded tokens, keys from vault/env |
| **Sensitive Data Protection** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | PII masked in logs, encrypted at rest |
| **Injection Defense (SQL/Cmd/XSS)**| ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | Safe parsers used, no shell execution |
| **Dependency Vulnerabilities** | ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | Dependency audit / CVE scan clean |
| **Audit Logging & Security Events**| ✅ Clean / ⚠️ Concern / ❌ Fail / N/A | State changes and auth failures logged |

---

## 3. Security Findings

### Finding SEC-001: [Title]
- **Severity**: `BLOCKER | HIGH | MEDIUM | LOW | INFO`
- **Domain**: `[e.g., Authorization / Injection / Secrets]`
- **File & Line**: `src/package/auth.py:65`
- **Vulnerability Description**: [Explain vulnerability mechanism, CWE ID if applicable]
- **Exploit Scenario**: [How an adversary could exploit this vulnerability]
- **Required Remediation**: [Actionable fix code or architectural protection]

---

## 4. Decision & Verdict
- **Verdict**: `[APPROVE | PUSHBACK | ESCALATE]`
- **Remediation Target**: [If PUSHBACK, return to `sdlc-implementer` or `sdlc-sa-design`]
- **Residual Risk Sign-off**: [Document any accepted low-level risks with rationale]
