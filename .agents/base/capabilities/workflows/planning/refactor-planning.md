---
role: capability
mode: workflow
triggers: { phase: plan, type: refactor, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Refactor Planning Workflow

Applied when `phase=plan, type=refactor`. This workflow guides the planning of structural code changes that must not alter behavior.

## Process

### Step 1: Define Goal

State the measurable outcome:
- **What problem is this solving?** Readability? Testability? Performance? Reducing duplication? Enabling a future feature?
- **How will we know it worked?** "Tests pass" is necessary but not sufficient. Be specific.
- **What is out of scope?** Explicitly state what will NOT change.

### Step 2: Establish Safety Net

Before touching any code, ensure you can detect behavioral changes:
- Run the full test suite. Confirm all tests pass.
- If test coverage is thin, write characterization tests for the code being refactored. These capture current behavior so you can detect regressions.
- Commit the baseline. This is your safety net snapshot.

This step is non-negotiable. If you can't establish a safety net, the refactor is too risky.

### Step 3: Analyze Current

Map the code to be refactored:
- What are the current responsibilities? Are they entangled?
- What are the coupling points? Who depends on what?
- Where are the boundaries? What should stay together vs be separated?

Output: a clear description of the current state and its problems.

### Step 4: Design Target

Define the target structure:
- What moves where? What gets extracted into its own module/class/function?
- What gets inlined (abstraction that isn't pulling its weight)?
- What gets renamed for clarity?
- What patterns will be applied (extract method, strategy pattern, dependency injection)?

The target should be clearly better than the current state across the dimensions that matter for this refactor.

### Step 5: Plan Incremental Steps

Break the refactor into small, reversible steps. Each step should:
- Be small enough to complete in one commit.
- Leave tests green (no partially-broken intermediate states).
- Be reversible — if this step was wrong, you can revert just this commit.

Bad: "Refactor the entire auth module." Good: "Extract TokenValidator class from AuthService. 3 files, ~40 lines."

### Step 6: Gate Check

For complex refactors (spanning multiple modules, significant structural change), ensure review-required gate. For standard refactors, verify after completion. For trivial (rename a variable), no gates needed.

### Step 7: Handoff

Transition to implementation. Include:
- Safety net verification instructions.
- Step-by-step refactoring plan.
- Target structure description.
- What to verify after each step (tests stay green).
