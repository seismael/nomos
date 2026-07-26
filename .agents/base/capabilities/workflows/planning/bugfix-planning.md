---
role: capability
mode: workflow
triggers: { phase: plan, type: bugfix, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Bugfix Planning Workflow

Applied when `phase=plan, type=bugfix`. This workflow guides the agent from a bug report to a fix plan, emphasizing evidence-based diagnosis over guesswork.

## Process

### Step 1: Reproduce

Confirm the bug exists before attempting to fix it:
- Capture exact steps to reproduce.
- Note the actual behavior vs expected behavior.
- Record the environment (OS, browser, version, data state).
- If you cannot reproduce, flag it. Don't fix a bug you can't observe.

### Step 2: Diagnose Root Cause

Trace the code path from symptom to cause:
- Follow the data flow from input to the point of failure.
- Use logging, debugger, or git bisect to narrow down.
- Identify the exact line, condition, or state that causes the bug.
- Form a hypothesis: "The bug occurs because X happens when Y."

Do not guess. Every diagnostic conclusion must be backed by evidence (logs, stack traces, test output).

### Step 3: Scope Fix

Determine the extent of the change:
- What files need to change?
- How many lines of code?
- Does the fix affect other behavior? Check callers, dependents, and similar code.
- Is this a one-line fix or does it require refactoring?

Flag if the fix scope is larger than expected — a "simple bug" that requires architectural changes is not a simple bug.

### Step 4: Plan

Write the fix plan:
1. **Regression test:** What test will we write to reproduce the bug? (Must include this.)
2. **Code change:** What exactly changes? Show the affected code.
3. **Verification:** How do we confirm the fix works? What tests does it pass?

Keep the plan minimal. Fix the bug; don't refactor the module (unless the refactor is necessary for the fix).

### Step 5: Gate Check

Emit the appropriate compliance marker. Trivial bugs skip gates; standard+ bugs require verification after completion.

### Step 6: Handoff

Transition to implementation. Include:
- Reproduction steps (so implementer can verify).
- Root cause analysis.
- Fix plan with regression test requirement.
- `[gov:plan:bugfix:<complexity>:L2:workflow-loaded]`
