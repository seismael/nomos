---
role: capability
mode: workflow
triggers: { phase: implement, type: refactor, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Refactor Implementation Workflow

Applied when `phase=implement, type=refactor`. This workflow executes the refactoring plan while ensuring behavior never changes.

## Process

### Step 1: Load Context

Read the refactor plan:
- What is being refactored and why?
- What is the current structure? What is the target structure?
- What are the incremental steps?

### Step 2: Establish Baseline

Run the full test suite. Record the results. All tests must be green before any refactoring begins. This is your proof that behavior is correct now, and must remain correct after each step.

### Step 3: Execute Incrementally

For each step in the plan:
1. Make the structural change (extract, inline, rename, move).
2. Run the full test suite immediately.
3. If tests stay green: commit. Move to next step.
4. If tests fail: revert to last green commit. Analyze what went wrong. Re-plan that step.

One commit per step. Each commit message describes the specific refactoring action.

### Step 4: Verify No Behavioral Change

After all steps are complete:
- Run the full test suite. Compare results with baseline. Must be identical.
- No test that passed before should fail now.
- Any new test failures are regressions. Fix before proceeding.

### Step 5: Cleanup

Remove any artifacts of the refactoring process:
- Dead code: old files, unused imports, orphaned functions.
- Temporary code: debugging statements, commented-out old code.
- Outdated references: config files, documentation, import paths.

### Step 6: Gate Check

- **Trivial** (rename, extract small method): No gates. Verify.
- **Standard+:** Verify after completion.
- **Complex** (multi-module, significant restructure): Review-required gate.

### Step 7: Handoff

Summarize the refactor:
- What was changed (before → after).
- Why it was changed.
- Evidence that behavior is preserved (test results).
- Any new patterns or conventions established.
