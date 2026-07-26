---
role: capability
mode: workflow
triggers: { phase: review, type: [feature, bugfix, refactor], complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md", "base/capabilities/personas/reviewer.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Code Review Workflow

Applied when `phase=review` for feature, bugfix, or refactor types. This workflow guides the code review process using the reviewer persona.

## Process

### Step 1: Load Reviewer Persona

Activate the reviewer persona's identity and standards:
- Quality gatekeeper, constructive not adversarial.
- Seven review focus areas: correctness, design, conventions, testing, security, performance, readability.
- Feedback must be specific, constructive, and severity-classified.

### Step 2: Understand the Change

Before reviewing code:
- Read the PR description, linked issues, and any related ADRs.
- Understand what this change is supposed to accomplish.
- Check the governance classification markers — do they match what you see?

### Step 3: Review the Diff

Go through changes file by file. Evaluate against these criteria:
- **Correctness:** Does it do what it claims? Are edge cases handled?
- **Design:** Does it fit the architecture? Right abstractions? Clean interfaces?
- **Conventions:** Naming, structure, error handling, documentation follow project standards?
- **Testing:** Are there tests? Do they test behavior or implementation? Edge cases covered?
- **Security:** Inputs validated? Secrets handled properly? Injection vulnerabilities?
- **Readability:** Can an unfamiliar developer understand this code?

### Step 4: Run Tests

Execute the test suite on the PR branch:
- All tests must pass. This is non-negotiable.
- Check for flaky tests — run the suite twice if there's any doubt.

### Step 5: Provide Feedback

Categorize each finding:
- **Must fix:** Bug, security issue, data loss risk. Blocking.
- **Should fix:** Convention violation, missed edge case, design concern. Non-blocking but expected.
- **Nit:** Style preference, minor naming. Optional.
- **Question:** Genuine curiosity. Not a demand.

Be specific and constructive. Explain why, not just what.

### Step 6: Decide

- **Approve:** All must-fix and should-fix items are resolved.
- **Request Changes:** Must-fix items remain unresolved.
- **Comment:** No blocking issues. Observations only. Approval is implicit.

### Step 7: Gate Check

- **Standard:** Verify. No formal gate.
- **Complex/Critical:** Emit `[gov:review:<type>:<complexity>:L4:gate-approved]` when approved.

Handoff to next phase (deployment or completion).
