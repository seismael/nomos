---
role: capability
mode: workflow
triggers: { phase: design, type: feature, complexity: [standard, complex, critical], valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Feature Design Workflow

Applied when `phase=design, type=feature` and complexity is standard or higher. Trivial features skip design and go directly to implementation.

## Process

### Step 1: Review Plan

Re-read the planning phase output:
- Confirm the scope and constraints haven't changed.
- Review the design approach chosen during planning.
- Identify any new information or decisions since planning.

### Step 2: Detail Components

Define every component, module, or class involved in this feature:
- **Responsibilities:** What does each component do? Single responsibility per component.
- **Dependencies:** What does each component depend on? Dependencies should be explicit and injectable.
- **Public interfaces:** What API does each component expose? Define method signatures, not implementations.
- **Internal state:** What data does each component own? What's mutable vs immutable?

### Step 3: Design Data Flow

Map how data moves through the system:
- **Input flow:** How does data enter the system? Validation, transformation, routing.
- **Processing flow:** How is data transformed? Which components handle which transformations?
- **Output flow:** How does data leave the system? Response format, side effects (events, logs, database writes).
- Use diagrams or structured descriptions. Cover the happy path AND error paths.

### Step 4: Specify Interfaces

Define exact contracts for all public interfaces:
- Function signatures: name, parameters (types, required/optional, defaults), return type.
- Error types: what errors can each method throw/return?
- Data structures: schemas, validation rules, invariants.
- Contract not implementation: consumers should know WHAT, not HOW.

### Step 5: Design Error Handling

Plan for failure:
- What errors can occur in each component?
- How are they classified? Recoverable (handle and continue), non-recoverable (propagate with context), fatal (fail fast).
- Where are errors caught? At boundaries (API handlers, event consumers) or internally?
- What's the user experience of each error? Don't expose internal error details.

### Step 6: Review Design

Apply design quality checks:
- Does the design follow SOLID principles?
- Are responsibilities clearly separated? No god objects, no anemic models.
- Does it fit with the existing architecture? Consistent patterns, no surprises.
- Is it testable? Can each component be tested in isolation?
- Is it simple? Can it be simpler? Challenge every abstraction.

### Step 7: Produce Artifacts

Create or update deliverables:
- Design document (using the design-doc template): architecture overview, component details, data flow, interfaces, error handling, alternatives considered.
- Updated ADRs if design decisions were made or changed.
- Implementation handoff notes: anything the implementer needs to know beyond the design doc.

### Step 8: Gate Check

Based on complexity:
- **Complex:** Ensure `design-required` gate is approved. Emit `[gov:design:feature:complex:L4:gate-approved]`.
- **Critical:** Ensure `design-required` gate is approved. Emit `[gov:design:feature:critical:L4:gate-approved]`.

Handoff to implementation phase with complete design artifacts.
