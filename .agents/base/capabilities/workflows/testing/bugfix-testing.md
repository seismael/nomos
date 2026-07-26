---
role: capability
mode: workflow
triggers: { phase: test, type: bugfix, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Bugfix Testing Workflow

Applied when `phase=test, type=bugfix`. This workflow verifies the fix works and hasn't introduced regressions.

## Process

### Step 1: Verify Fix

Confirm the bug is resolved:
- Run the regression test that reproduces the bug. It must pass.
- Manually reproduce the original bug scenario. The bug must be gone.
- Check: does the fix address the root cause, or just the symptom?

### Step 2: Run Full Suite

Run the complete test suite:
- All tests must pass. The fix should not have broken anything else.
- Pay extra attention to tests related to the changed code area.
- If any test fails, investigate. The fix may have unintended side effects.

### Step 3: Check Related Functionality

Manually verify behavior adjacent to the fix:
- Features that share code with the fixed area — do they still work?
- Any similar bugs in nearby code? (If one instance of the pattern was buggy, check others.)
- Edge cases around the fix — did the fix handle them or create new ones?

### Step 4: Gate Check

- **Trivial:** No gate. Verify.
- **Standard+:** Verify gate.
- **Critical** (security fix, data corruption fix): Review-required gate.

### Step 5: Handoff

Confirm the bug is resolved:
- Evidence: regression test passes, reproduction steps no longer reproduce.
- Any follow-up actions (e.g., check similar code for the same bug pattern).
- Ready for deployment.
