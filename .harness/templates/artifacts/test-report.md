# Test Execution Report: [Feature / Change Name]

## Metadata
- **Run ID**: `[run-id]`
- **Date**: `[YYYY-MM-DDTHH:MM:SSZ]`
- **Executor**: `sdlc-test-executor`
- **Test Plan Ref**: `artifacts/test-plan.md`
- **Execution Verdict**: `ALL_PASSED | FAILURES_DETECTED | EXECUTION_BLOCKED`

---

## 1. Execution Environment & Configuration
- **Host OS**: `[e.g., Windows 11 / Linux x86_64]`
- **Python / Runtime**: `[e.g., Python 3.13.1 / Node 20.x]`
- **Working Directory**: `[Absolute path]`
- **Dependencies Version Hash**: `[pyproject.toml / package-lock hash]`

---

## 2. Test Execution Summary
| Metric | Count | Percentage |
|---|---|---|
| **Total Test Cases** | `[Total]` | 100% |
| **Passed (✅)** | `[Passed]` | `[%]` |
| **Failed (❌)** | `[Failed]` | `[%]` |
| **Blocked (⚠️)** | `[Blocked]` | `[%]` |
| **Not Run (⏭️)** | `[Not Run]` | `[%]` |
| **Total Duration** | `[X.XXs]` | - |

---

## 3. Command Execution Log
### 3.1 Build Sanity / Bundle Verification (Non-Test Tier)
- **Command**: `npm run build` or `dotnet build`
- **Exit Code**: `0`
- **Notes**: *Build sanity verifies packaging and compilation only. It does not verify runtime DOM or business behavior.*

### 3.2 Unit Test Suite
- **Command**: `pytest tests/unit/ -v` or `npm run test:unit`
- **Exit Code**: `0 | 1`
- **Execution Time**: `0.45s`
- **Raw Output**:
```text
[Paste terminal test execution output]
```

### 3.3 Integration & API Test Suite
- **Command**: `pytest tests/integration/ -v` or `dotnet test`
- **Exit Code**: `0`
- **Execution Time**: `1.20s`
- **Raw Output**:
```text
[Paste terminal test execution output]
```

### 3.4 E2E Browser Test Suite (Playwright / Cypress)
- **Command**: `npx playwright test`
- **Exit Code**: `0`
- **Execution Time**: `8.50s`
- **Browser Console Errors**: `0 errors`
- **Raw Output**:
```text
[Paste terminal E2E test execution output]
```

---

## 4. Test Results by Case ID
| Test Case ID | Name / Description | Priority | Status | Duration | Failure Log / Notes |
|---|---|---|---|---|---|
| `TEST-001` | Valid User Registration | `P0` | `PASS` | 0.05s | Clean pass |
| `TEST-002` | Invalid Input Returns 400 | `P1` | `PASS` | 0.02s | Clean pass |
| `TEST-003` | Concurrency Lock | `P1` | `PASS` | 0.15s | Clean pass |

---

## 5. Defect Register (Failing Tests)
*Test executor never reinterprets requirements to force passing. Any failure is logged here:*

### Defect DEF-001
- **Failing Test**: `TEST-002: tests/test_module.py::test_boundary`
- **Error Type**: `AssertionError`
- **Expected**: `Status code 400 with payload {"error": "limit_exceeded"}`
- **Actual**: `Status code 500 with InternalServerError traceback`
- **Traceback**:
```text
[Traceback excerpt]
```
