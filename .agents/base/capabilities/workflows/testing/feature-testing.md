---
role: capability
mode: workflow
triggers: { phase: test, type: feature, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Feature Testing Workflow

Applied when `phase=test, type=feature`. This workflow validates that a feature works correctly, covers edge cases, and meets acceptance criteria.

## Process

### Step 1: Review Test Requirements

Understand what needs testing:
- What types of tests are expected? Unit, integration, end-to-end?
- What is the target coverage?
- What are the acceptance criteria from the feature spec?
- What areas are highest risk and need extra attention?

### Step 2: Run Existing Tests

Run the full test suite:
- All tests must pass. If there are pre-existing failures, note them.
- Record the baseline — test count, pass/fail, coverage.

### Step 3: Run New Tests

Execute the feature's test suite:
- All new tests should pass (they should have passed during TDD implementation).
- If any new test fails, this is a regression. Investigate.

### Step 4: Fill Coverage Gaps

Review uncovered code paths:
- What code was added but not tested?
- Are there edge cases the existing tests miss? (Null inputs, boundary values, error states, concurrent access)
- Add tests for critical gaps. Don't test trivial getters/setters, but do test behavior.

### Step 5: Manual Verification

For features that benefit from human judgment:
- **UI features:** Visually verify the interface. Check responsive behavior, accessibility, error states.
- **API features:** Test with real requests (curl, Postman, integration test client).
- **Data features:** Verify with realistic datasets. Check data integrity after operations.

### Step 6: Performance Check

Check for regressions:
- Compare key metrics before/after: response time, memory usage, startup time.
- If there's a significant regression, flag it. Don't silently ship slower code.
- For performance-sensitive features, run load tests or benchmarks.

### Step 7: Acceptance Criteria

Verify every acceptance criterion from the feature spec:
- Go through the list one by one.
- Each criterion: pass or fail with evidence. "Seems to work" is not evidence.
- If any criterion fails, the feature is not done.

### Step 8: Gate Check

- **Trivial/Standard:** Verify.
- **Complex:** Test gate ready.
- **Critical:** Test-required gate must be approved.

Handoff with test results summary.
