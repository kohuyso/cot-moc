# Security & Compliance Review Checklist

**Target Artifact**: `artifacts/security-review.md`
**Reviewer Role**: `sdlc-security-review`
**Marker Semantics**: Mark `[x]` only when security verification is satisfied.

---

## 1. Authentication & Authorization
- [ ] `CHK-SEC-001`: Are authentication credentials, session tokens, and API keys validated on every request?
- [ ] `CHK-SEC-002`: Are role-based or attribute-based authorization checks enforced at server boundaries?
- [ ] `CHK-SEC-003`: Does the system follow the principle of least privilege for database and service roles?

## 2. Input Validation & Injection Prevention
- [ ] `CHK-SEC-004`: Are all untrusted inputs strictly validated for length, characters, and schemas?
- [ ] `CHK-SEC-005`: Are SQL queries parameterized without raw string concatenation?
- [ ] `CHK-SEC-006`: Are OS commands avoided or executed with safe argument arrays rather than shell execution?

## 3. Cryptography & Secrets Hygiene
- [ ] `CHK-SEC-007`: Are sensitive fields (passwords, payment data, PII) encrypted in transit (TLS) and at rest?
- [ ] `CHK-SEC-008`: Are zero secrets, API tokens, or private keys committed to the repository?
- [ ] `CHK-SEC-009`: Are sensitive values masked in log files and error responses?

## 4. Supply Chain & Vulnerability Scanning
- [ ] `CHK-SEC-010`: Are newly added dependencies scanned for known CVE vulnerabilities?
- [ ] `CHK-SEC-011`: Are security review findings categorized by severity with zero unmitigated Blocker/High issues?
