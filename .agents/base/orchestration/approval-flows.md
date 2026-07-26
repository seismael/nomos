---
role: orchestration
triggers: { phase: "*", type: "*", complexity: [complex, critical], valid: true }
layer: complexity
priority: 41
status: active
context_cost: medium
depends_on: ["base/orchestration/gates.yaml"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Approval Flows

## Human Approval

Required for: `complex` tasks (before implementation), `critical` tasks (before design, before deploy).

### Process

1. Agent reaches a gate requiring human approval.
2. Agent presents:
   - **What was done:** Summary of completed work.
   - **What is proposed:** The next step.
   - **Risks and mitigations:** What can go wrong and how it's handled.
   - **Alternatives:** What other approaches were considered?
3. Agent waits for explicit approval before proceeding.
4. Agent emits `[gov:<phase>:<type>:<complexity>:L4:gate-<checkpoint>-approved]` after receiving approval.

### Agent Approval Prompt

```
[GOVERNANCE GATE — Human Approval Required]

Completed: [summary of work done]
Proposed next step: [what you plan to do]
Risks: [identified risks and mitigations]
Alternatives considered: [what else was evaluated]

Do you approve proceeding? (yes/no/revise)
```

## Peer Review

Required for: `complex` and `critical` tasks after implementation.

### Process

1. Agent creates a pull request with the governance-compliant PR template.
2. At least one peer reviews against the reviewer persona's criteria.
3. All must-fix and should-fix items are resolved.
4. Peer approves the PR.
5. Agent emits `[gov:review:<type>:<complexity>:L4:gate-review-approved]`.

## Architecture Review

Required for: `critical` tasks before implementation, architecture-type tasks at any complexity.

### Process

1. Agent presents the ADR or design document.
2. Architecture review validates:
   - Problem framing: correct and complete?
   - Alternatives: sufficient exploration?
   - Trade-offs: honestly assessed?
   - Design: satisfies the decision? Follows SOLID/DDD?
   - Risks: identified and mitigated?
3. Reviewer approves or requests changes.
4. Agent emits `[gov:review:architecture:<complexity>:L4:gate-review-approved]`.

## Bypassing Gates

Gates should never be silently bypassed. If a gate cannot be satisfied:

1. **Reclassify:** Does the task genuinely meet the gate's criteria? If not, reclassify to a lower complexity.
2. **Escalate:** If the gate is valid but cannot be met, escalate to a human for an explicit exception.
3. **Document:** If an exception is granted, document the reason in the PR or ADR.

The marker for deliberate bypass is `[gov:<phase>:<type>:<complexity>:L4:gate-bypassed:<reason>]`.
