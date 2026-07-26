---
role: capability
mode: workflow
triggers: { phase: review, type: architecture, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md", "base/capabilities/personas/reviewer.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Architecture Review Workflow

Applied when `phase=review, type=architecture`. This workflow reviews an architectural decision or design for soundness, consistency, and risk.

## Process

### Step 1: Load Context

Read the relevant documents:
- The ADR being reviewed.
- Related design documents.
- Context from the architect persona's design heuristics.

Understand the decision, the alternatives considered, and the rationale.

### Step 2: Evaluate Decision

Assess the decision itself:
- Is the problem clearly framed? Are constraints correctly identified?
- Was the "do nothing" alternative genuinely considered?
- Are the trade-offs correctly assessed? Nothing over- or under-weighted?
- Were at least 2-3 meaningfully different alternatives explored?
- Is the choice proportional to the problem? A microservices architecture for a todo app is wrong.

### Step 3: Evaluate Design

Assess the design that realizes the decision:
- Does the design satisfy the decision and its constraints?
- Are system boundaries clear and appropriate?
- Are cross-cutting concerns addressed for all subsystems?
- Does it follow SOLID, DDD, and established architectural patterns?
- Is the design testable, deployable, and observable?

### Step 4: Identify Risks

Surface risks the architect may have missed:
- **Technical risks:** Scaling limits, failure modes, complex interactions.
- **Organizational risks:** Knowledge silos (only one person understands this), high maintenance burden.
- **Process risks:** Timeline dependencies, integration complexity.
- **Security risks:** New attack surface, data exposure, compliance implications.

### Step 5: Decide

- **Approve:** Sound architecture. Risks are identified and acceptable. Ready to implement.
- **Request Changes:** Specific issues must be addressed before proceeding. List them clearly.
- **Comment:** Non-blocking observations or suggestions for consideration.

### Step 6: Document

Write review notes:
- Summary of the review.
- Key findings and their severity.
- Any conditions on the approval (e.g., "must add monitoring for X before deploying").
- Archive with the ADR if this is a formal governance gate.

### Step 7: Gate Check

- **Complex/Critical:** Emit `[gov:review:architecture:<complexity>:L4:gate-approved]` when the architecture is approved.

### Step 8: Handoff

If approved: ready for design or implementation.
If changes requested: clear, actionable items for the architect. No ambiguity.
