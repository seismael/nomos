---
role: capability
mode: workflow
triggers: { phase: plan, type: feature, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Feature Planning Workflow

Applied when `phase=plan, type=feature`. This workflow guides the agent from an unshaped feature request to a validated implementation plan ready for design or implementation.

## Process

### Step 1: Understand

Parse the feature request. Identify:
- **Explicit requirements:** What the user literally asked for.
- **Implicit needs:** What the user needs but didn't state. What problem does this solve?
- **Constraints:** Technical, business, timeline, dependencies.
- **Success criteria:** How will we know this is done and correct?

If anything is ambiguous, ask clarifying questions before proceeding. A misunderstood requirement at this stage cascades into wasted work.

### Step 2: Explore Context

Examine the codebase to understand the change landscape:
- What modules, files, and systems will be affected?
- What existing patterns should the feature follow?
- Are there ADRs or design docs relevant to this area?
- What are the technical risks and dependencies?

Don't design yet. Just learn. Output: a summary of the relevant codebase landscape.

### Step 3: Design

Propose the architecture for this feature:
- **Components:** What new modules, classes, or services are needed? What existing ones change?
- **Data flow:** How does data move through the system? Input → processing → output.
- **Interfaces:** Public API signatures for new components.
- **Error handling:** What can go wrong and where is it caught?
- **Alternatives:** 2-3 different approaches with trade-offs. Recommend one with rationale.

For complex features, produce this as a design document using the design-doc template.

### Step 4: Produce Artifacts

Generate the deliverables:
- **Design doc** (for standard+ complexity): written using the design-doc template.
- **ADR** (for architectural decisions): written using the ADR template.
- **Implementation plan**: broken into bite-sized tasks with file paths, test-first TDD steps, and verification commands.

### Step 5: Validate

Review the plan before handoff:
- Does the design follow project conventions?
- Are there placeholder/TODO/ambiguous requirements?
- Is the scope consistent? No gold-plating, no missing pieces.
- Can an implementer execute this without asking for clarification?

### Step 6: Gate Check

Based on complexity:
- **Standard:** Run validation. No formal gate.
- **Complex/Critical:** Ensure `plan-required` gate is approved. Emit `[gov:plan:feature:<complexity>:L4:gate-approved]`.

### Step 7: Handoff

Transition to the design or implementation phase. Emit the classification marker. Include:
- Design doc and ADR (if produced).
- Implementation plan.
- Context summary for the next phase.
