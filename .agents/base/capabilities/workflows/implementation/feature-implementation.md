---
role: capability
mode: workflow
triggers: { phase: implement, type: feature, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Feature Implementation Workflow

Applied when `phase=implement, type=feature`. This is the TDD-driven construction phase where plans and designs become working code.

## Process

### Step 1: Load Context

Read the implementation plan, design docs, and relevant ADRs. Understand the full scope:
- What are you building?
- What are the acceptance criteria?
- What existing code will you touch?
- What dependencies do you need?

### Step 2: Verify Preconditions

Before writing any code:
- Run the existing test suite. It must pass. If there are pre-existing failures, fix or escalate — don't build on broken foundations.
- Confirm all dependencies are available.
- Check out the correct branch.

### Step 3: Implement Incrementally

For each unit of work from the plan:
1. **Write a failing test** — Express the desired behavior.
2. **Run the test** — Confirm it fails for the expected reason (red).
3. **Write minimal code** — Just enough to make the test pass. No more.
4. **Run the test** — Confirm it passes (green).
5. **Run full suite** — Confirm no regressions.
6. **Refactor** — Clean up while tests stay green.
7. **Commit** — One logical change per commit.

Repeat until the feature is complete. Each iteration is one commit.

### Step 4: Integration Verify

After all units are built:
- Run integration tests. Do the components work together?
- Manual verification: does the feature work end-to-end?
- Check for integration issues: mismatched interfaces, data format problems, missing error handling.

### Step 5: Code Quality

Before considering the feature done:
- Run linter and formatter. Fix all warnings.
- Self-review the diff: any debug code, commented-out blocks, TODOs without tracking issues?
- Check file sizes: any file over 300 lines should be questioned.
- Verify naming follows conventions.

### Step 6: Prepare Review

Write a pull request:
- **Description:** What was built, why, key design decisions.
- **Testing:** What tests were added? How can the reviewer verify?
- **Governance:** Compliance markers for the classification and any gates.
- **Related issues/ADRs:** Link to everything relevant.

### Step 7: Gate Check

Based on complexity:
- **Trivial/Standard:** Verify after completion. No formal gates.
- **Complex:** Ensure `review-required` gate is available. Emit `[gov:implement:feature:complex:L4:gate-ready]`.
- **Critical:** All prior gates (plan, design) must be approved. Review and test gates pending.

### Step 8: Handoff

Mark the feature as review-ready. Provide:
- PR link.
- Summary of what was implemented and verified.
- Any deviations from the plan and why.
- Classification and gate markers.
