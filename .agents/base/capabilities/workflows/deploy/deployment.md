---
role: capability
mode: workflow
triggers: { phase: deploy, type: [feature, bugfix, refactor, ops], complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Deployment Workflow

Applied when `phase=deploy`. This workflow guides the safe release of changes to production with monitoring and rollback capability.

## Process

### Step 1: Pre-Deployment Checklist

Before deploying, verify:
- All governance gates for the complexity level are approved.
- Test suite passes on the deployment candidate.
- Rollback plan is documented and tested (preferably in staging).
- Monitoring dashboards are configured and visible.
- Communication plan: who is notified before, during, and after?
- Deployment window is appropriate (not during peak traffic unless urgent).

### Step 2: Deploy

Execute the deployment process:
- Follow the deployment runbook or pipeline. Don't improvise.
- Monitor key metrics during deployment (error rate, latency, saturation).
- Deploy incrementally if possible: canary (1%), then 10%, then 100%.
- If any metric deviates from expected, pause and assess.

### Step 3: Verify

After deployment is complete:
- Run smoke tests against production. Critical paths must work.
- Verify new functionality is operational (if this is a feature deploy).
- Confirm error rates are within normal range.
- Check monitoring dashboards — no anomalies.

### Step 4: Monitor

Active monitoring for a defined period:
- **Standard deploy:** 15 minutes of active monitoring.
- **Critical deploy:** 1 hour minimum, extended if risk assessment warrants.
- Watch: error rates, latency, resource utilization, user reports.
- Don't walk away. Stay available until the monitoring period ends.

### Step 5: Rollback (if needed)

If verification or monitoring reveals a problem:
- Execute rollback immediately. Don't try to "fix forward" under pressure.
- Roll back first, then analyze the root cause in a calm state.
- Verify rollback restored normal operation.
- Communicate: rollback executed, service restored, investigation underway.

### Step 6: Post-Deployment

After successful deployment:
- Update deployment logs: what was deployed, when, by whom, outcome.
- Close related tickets and issues.
- Notify stakeholders of completion.
- If this was a critical deploy, schedule a brief post-deployment review.

### Step 7: Handoff

- If all verification and monitoring passed: deployment complete. Emit `[gov:deploy:<type>:<complexity>:done]`.
- For critical deployments: ensure deploy-review gate is satisfied post-monitoring.
