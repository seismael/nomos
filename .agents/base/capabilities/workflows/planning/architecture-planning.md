---
role: capability
mode: workflow
triggers: { phase: plan, type: architecture, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Architecture Planning Workflow

Applied when `phase=plan, type=architecture`. This workflow guides the agent through making and documenting a significant architectural decision.

## Process

### Step 1: Frame Decision

Define the problem precisely:
- What is the decision about? Be specific, not "we need to pick a database."
- What are the constraints? Technical (language, platform, existing systems), business (budget, timeline, team skills, compliance), and organizational (team structure, Conway's Law).
- What is the scope? What parts of the system are affected? What's out of scope?
- What happens if we don't decide? "Do nothing" is always an alternative. State its consequences.

### Step 2: Gather Context

Understand the landscape:
- Read existing ADRs in `docs/adr/` — don't contradict past decisions without acknowledging it.
- Examine the current architecture — what's fixed, what's flexible, what's already committed.
- Identify stakeholders — who is affected by this decision? Who needs to approve it?

### Step 3: Generate Alternatives

Propose 2-4 distinct approaches:
- Each alternative should be a genuinely different path, not a minor variation.
- "Do nothing" must be considered — it forces you to articulate why change is necessary.
- For each alternative: briefly describe the approach, its key characteristics, and when it would be appropriate.

### Step 4: Evaluate Trade-offs

Score each alternative across these dimensions:
- **Simplicity:** How many moving parts? How easy to understand?
- **Flexibility:** How easy to change later? How well does it accommodate known future requirements?
- **Performance:** Throughput, latency, resource usage.
- **Maintainability:** Ease of debugging, modifying, onboarding.
- **Scalability:** Handles growth in users, data, traffic.
- **Security:** Attack surface, data protection, compliance.

Use a decision matrix. Weight the dimensions based on what matters most for this specific decision. Not all dimensions are equally important.

### Step 5: Decide

Choose the best option:
- State the decision clearly. One sentence.
- Provide the rationale. Why this over the alternatives?
- Note what was rejected and why. Future readers should understand the path not taken.
- Identify any assumptions. "This assumes we won't exceed 1M users in the next 2 years."

### Step 6: Document ADR

Write an Architecture Decision Record using the ADR template:
- **Title:** Short, descriptive. "ADR-003: Use PostgreSQL for Primary Data Store"
- **Context:** Why this decision is needed. What are the forces at play?
- **Decision:** What we decided. Clear, unambiguous.
- **Consequences:** What becomes easier? What becomes harder? What are the risks?
- **Alternatives:** What else was considered and why rejected.
- **Status:** Proposed, Accepted, Deprecated, or Superseded.

Commit the ADR to `docs/adr/`. ADRs are immutable once accepted. If superseded, create a new ADR.

### Step 7: Validate

Have the decision reviewed:
- Peer review: does the reasoning hold up? Are there unstated assumptions?
- Check against existing ADRs: any conflicts?
- Verify the decision is actionable: can the team implement this?

### Step 8: Handoff

Transition to design or implementation. Include:
- The ADR (committed to `docs/adr/`).
- Decision matrix and rationale.
- Action items for implementation.
