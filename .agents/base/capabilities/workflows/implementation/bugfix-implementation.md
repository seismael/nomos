---
role: capability
mode: workflow
triggers: { phase: implement, type: bugfix, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Bugfix Implementation Workflow

Applied when `phase=implement, type=bugfix`. This workflow executes the fix plan with a mandatory regression test.

## Process

### Step 1: Load Context

Read the bug report and fix plan:
- What is the bug? What is the expected vs actual behavior?
- What is the root cause?
- What is the fix plan?
- What files will change?

### Step 2: Write Regression Test

Write a test that reproduces the bug:
- The test should fail with the current code (red).
- The test should be specific: it demonstrates the exact bug, not a general area.
- Run it. Confirm it fails. If it passes, either the bug isn't reproducible or the test is wrong.

**No regression test, no fix.** This is a hard rule. If you truly cannot write a test, document why and escalate.

### Step 3: Implement Fix

Write minimal code to fix the bug:
- Change only what's needed. Don't refactor adjacent code (unless the refactor is required for the fix).
- Make the fix pass the regression test (green).
- Keep the change as small as possible. Smaller = easier to review, less risk.

### Step 4: Verify

Confirm the fix is correct:
- Regression test passes.
- Full test suite passes (no regressions).
- If applicable, manually verify the original reproduction steps — bug is gone.
- Run related integration tests if they touch the same area.

### Step 5: Prepare Review

Write a clear PR:
- **Description:** What was the bug? What caused it? How was it fixed?
- **Testing:** The regression test that reproduces and verifies the fix.
- **Risk:** Is this fix safe? Could it have side effects?
- **Governance markers.**

### Step 6: Gate Check

- **Trivial:** No gates. Verify and commit.
- **Standard+:** Verify gate. Emit `[gov:implement:bugfix:<complexity>:L4:gate-ready]`.

### Step 7: Handoff

PR ready for review. Include:
- Bug description and reproduction steps.
- Root cause explanation.
- Fix description.
- Regression test and verification results.
