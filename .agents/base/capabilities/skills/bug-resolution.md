---
role: capability
mode: skill
triggers: { phase: "*", type: bugfix, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Bug Resolution

Reference material for agents working on bugfix-type tasks. Load alongside bugfix planning and implementation workflows.

## Diagnostic Approach

Follow this sequence. Don't skip steps.

1. **Reproduce** — Confirm the bug exists. Capture exact steps. If you can't reproduce it, you can't fix it.
2. **Isolate** — Narrow the scope. Git bisect to find the introducing commit. Minimize the reproduction case to the smallest input that triggers the bug.
3. **Hypothesize** — Form a theory about the root cause. "The bug occurs because X when Y." The theory must explain ALL observed symptoms.
4. **Instrument** — Add logging, assertions, or breakpoints to test the hypothesis. Gather evidence. Don't guess.
5. **Verify** — Confirm the hypothesis with concrete evidence: logs, stack traces, test output. "Probably X" is not verification.
6. **Fix** — Write minimal code to address the root cause. Fix the cause, not the symptom.
7. **Regression-test** — Write a test that reproduces the bug and verifies the fix. Run it: red (bug present) → green (fix works). Commit.

## Common Bug Categories

| Category | Signs | Common Causes |
|---|---|---|
| Off-by-one | Wrong count, loop misses last/first | Index confusion (0-based vs 1-based), `<` vs `<=` |
| Null/undefined | TypeError, NPE, "cannot read property" | Missing null check, uninitialized variable, async race |
| Race condition | Intermittent failure, works sometimes | Unprotected shared state, missing await/lock, event ordering |
| State corruption | Data that shouldn't change, changes | Missing immutability, shared mutable reference, stale closure |
| Incorrect assumption | "This should never happen" but it does | Edge case not considered, API contract misunderstood, data shape changed |
| Boundary condition | Fails at extremes (empty, max, min) | Insufficient validation, not testing limits |

## Diagnostic Tools

- **Logging:** Add structured logs with context (input values, state, timestamps). Log at boundaries.
- **Debugger:** Step through the exact code path. Inspect variable values. Watch conditions.
- **Git bisect:** `git bisect start HEAD <last-known-good-commit>` — binary search through commits to find the introducing change.
- **Isolation tests:** Extract the failing code into a standalone test. Does it still fail? If yes, the bug is in that code. If no, the bug is in the integration.

## The Regression Test Requirement

**Every bug fix MUST include a test that demonstrates the bug.** No exceptions for non-trivial bugs.

The regression test serves three purposes:
1. Proves the bug existed (fails before fix).
2. Verifies the fix works (passes after fix).
3. Prevents the bug from recurring (fails if someone reintroduces the bug).

If you cannot write a regression test, the code is untestable. That's a design problem — escalate.

## When NOT to Fix

- **The fix is riskier than the bug.** A rare cosmetic issue vs a fix that touches core auth logic. Ship a workaround, document the bug, fix in a planned refactor.
- **The bug is in a system you don't control.** File an upstream issue. Add a workaround with a `HACK` comment referencing the upstream issue.
- **Fixing would delay critical work.** Document the bug. File a ticket. Prioritize against other work. Don't let perfect be the enemy of shipped.
