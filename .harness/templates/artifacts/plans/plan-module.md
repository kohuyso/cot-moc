# Module Implementation Plan & Work Package: [Module/Service Name]

## 1. Module Metadata
- **Module / Service Name**: `[e.g. Booking | Payment | Identity]`
- **Architecture Style**: `modular_monolith | microservices`
- **Scope Boundary (Path)**: `[e.g. src/Modules/Booking/ or services/booking/]`
- **Target Runtime**: `[.NET 8 / Python 3.12 / Node.js 20]`
- **Requirements Ref**: `artifacts/rtm.md` (`[FR-001, FR-002]`)
- **API Contracts Ref**: `artifacts/solution-design.md` (`[Endpoints / OpenAPIs]`)

---

## 2. Strict File Confinement List
Only the files declared below may be modified by the implementer:
- **Create**:
  - `[path/to/new_file_1.cs]`
  - `[path/to/new_file_2.cs]`
- **Modify**:
  - `[path/to/existing_file.cs]`
- **Test**:
  - `[tests/path/to/test_file.cs]`

---

## 3. Work Breakdown Structure (WBS Tasks)

### Task 1: [Task Name - e.g., Domain Model & DB Schema]
- **Requirement ID**: `[FR-xxx]`
- **Associated Test Case**: `[TC-xxx]`
- **Inputs (Consumes)**: `[Input DTO/Model signatures]`
- **Outputs (Produces)**: `[Output DTO/Entity signatures]`
- **TDD Steps**:
  1. Write failing unit test verifying domain logic.
  2. Implement minimal domain logic.
  3. Verify unit test passes.

### Task 2: [Task Name - e.g., Service Logic & API Endpoint]
- **Requirement ID**: `[FR-xxx]`
- **Associated Test Case**: `[TC-xxx]`
- **Inputs (Consumes)**: `[HTTP Request DTO]`
- **Outputs (Produces)**: `[HTTP Response DTO]`
- **TDD Steps**:
  1. Write failing controller/endpoint test.
  2. Implement service logic and wire repository.
  3. Verify test passes.

---

## 4. Verification & Gate Commands
- **Module Unit Test**: `[e.g. dotnet test src/Modules/Booking.Tests]`
- **Boundary Lint / Typecheck**: `[e.g. dotnet build src/Modules/Booking]`
