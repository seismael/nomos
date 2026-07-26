---
role: capability
mode: workflow
triggers: { phase: implement, type: ops, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Operations Implementation Workflow

Applied when `phase=implement, type=ops`. This workflow executes an operational change with safety checks and mandatory rollback capability.

## Process

### Step 1: Load Context

Read the operational plan:
- What is changing?
- What are the pre-flight checks?
- What is the execution sequence?
- What is the rollback procedure?

### Step 2: Pre-Flight Checks

Before touching any production system, verify:
- **Access:** Do you have the required permissions?
- **Backups:** Are there recent backups of affected systems?
- **Rollback:** Is the rollback procedure tested and ready to execute?
- **Monitoring:** Are dashboards and alerts configured for the change window?
- **Communication:** Have affected teams/stakeholders been notified?

If any pre-flight check fails, stop. Do not proceed until it's resolved.

### Step 3: Execute Change

Apply the change step by step:
- Follow the plan exactly. No improvisation.
- After each step, verify the expected outcome before moving to the next.
- Monitor key metrics during execution. Watch for anomalies.
- If anything unexpected occurs: pause. Assess. Don't "push through."

### Step 4: Verify

After the change is applied:
- Run smoke tests. Critical paths must work.
- Check monitoring: error rates, latency, resource usage within expected range.
- Verify the specific success criteria from the plan.
- If verification fails: execute rollback immediately.

### Step 5: Document

Record the change:
- What was done, when, by whom.
- Any deviations from the plan and why.
- Outcome: success, partial, or rollback.
- Lessons learned for future similar changes.

Update runbooks, deployment logs, and any relevant tracking systems.

### Step 6: Gate Check

- **Trivial/Standard:** Verify after completion.
- **Complex:** Deploy-review gate.
- **Critical:** Deploy-review gate. Post-deployment monitoring for defined period.

### Step 7: Handoff

Communicate completion:
- Notify stakeholders.
- Close related tickets with outcome summary.
- Update changelog if applicable.
