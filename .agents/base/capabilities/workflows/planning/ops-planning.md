---
role: capability
mode: workflow
triggers: { phase: plan, type: ops, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Operations Planning Workflow

Applied when `phase=plan, type=ops`. This workflow guides the planning of operational changes — infrastructure, CI/CD, configuration, dependencies, deployments.

## Process

### Step 1: Understand Change

Define the operational change:
- What is changing? State "before" and "after" explicitly.
- Why is this change needed? Bug, upgrade, new capability, compliance?
- What systems are affected? Service A, database B, pipeline C?
- Who are the stakeholders? Who needs to be notified?

### Step 2: Assess Impact

Evaluate the blast radius:
- What is the blast radius? If this goes wrong, what breaks?
- Is there downtime? How long? Can it be avoided (rolling, blue-green)?
- Is there data migration? Schema changes, data transformation?
- What are the dependencies? Upstream services that need this? Downstream services that consume it?
- How do we verify success? Specific metrics, smoke tests, monitoring checks.

### Step 3: Plan

Write the step-by-step operational plan:
1. **Pre-flight checks:** What must be confirmed before starting?
2. **Execution steps:** Ordered, specific, with expected output for each.
3. **Checkpoints:** At what points do we verify before continuing?
4. **Rollback procedure:** How do we undo this change? Test the rollback in a non-production environment first.

**Rollback is mandatory.** Never plan a change without a documented, tested way to undo it.

### Step 4: Test Plan

How will you verify the change before production?
- Can this be tested in staging? If yes, do it.
- Can this be canary-deployed? Roll out to 1% of traffic first.
- Can this be dry-run? Simulate the change without side effects.
- What specific tests confirm success? Automated and manual.

### Step 5: Gate Check

Complexity-based gates:
- **Trivial:** (e.g. update a non-critical config value) — no gates.
- **Standard:** Verify after completion.
- **Complex:** Plan-required gate.
- **Critical:** Plan-required + deploy-review gates. All must be approved.

### Step 6: Handoff

Transition to implementation. Include:
- Full operational plan (pre-flight, steps, checkpoints, rollback).
- Impact assessment.
- Test plan results.
- Communication plan.
- Gate status.
