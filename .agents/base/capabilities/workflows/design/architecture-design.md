---
role: capability
mode: workflow
triggers: { phase: design, type: architecture, complexity: [standard, complex, critical], valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Architecture Design Workflow

Applied when `phase=design, type=architecture`. Follows the architecture planning phase — this workflow designs the subsystems and boundaries that realize the architectural decision.

## Process

### Step 1: Review ADR

Re-read the architecture decision record:
- Confirm the chosen approach and its rationale.
- Note the consequences: what becomes easier, what becomes harder.
- Identify the key constraints the ADR imposes on the design.

### Step 2: Define System Boundaries

Draw clear lines around subsystems:
- What are the bounded contexts? Where does one domain end and another begin?
- What are the interfaces between contexts? Events, APIs, shared data?
- What crosses boundaries and what stays inside? Define explicit contracts.

### Step 3: Detail Subsystems

For each bounded context, define:
- **Domain model:** Entities, value objects, aggregates. What are the aggregate roots?
- **Services:** Domain services (business logic), application services (orchestration), infrastructure services (external systems).
- **Repositories:** Data access patterns. Per-aggregate or per-entity?
- **Events:** Domain events that cross context boundaries.

### Step 4: Specify Cross-Cutting Concerns

How does each subsystem handle:
- **Logging:** Structured, correlated across contexts.
- **Monitoring:** Metrics, health checks, alerts.
- **Authentication/Authorization:** Who can do what? Where is auth checked?
- **Caching:** What gets cached? Where? Invalidation strategy?
- **Error handling:** Classification, propagation, user-facing messages.

### Step 5: Define Dependencies

Map the dependency graph:
- What does each bounded context depend on?
- Are there circular dependencies? (Must be eliminated — DAG only.)
- What's the direction of dependency? Infrastructure → Application → Domain.
- What are the integration patterns? Synchronous (API calls), asynchronous (events, messages), shared (database, file system)?

### Step 6: Validate

Check the design:
- Does it satisfy the ADR's decision and constraints?
- Is it consistent with SOLID and DDD principles?
- Are there any unaddressed risks from the architecture review?
- Can it be built incrementally? Or does everything need to exist at once?

### Step 7: Produce Artifacts

Generate deliverables:
- Architecture design document: system boundaries, subsystem details, cross-cutting concerns, dependency graph.
- Updated or new ADRs if design decisions surfaced new architectural questions.
- Component diagrams or structured descriptions of the system topology.

### Step 8: Gate Check

Based on complexity:
- **Complex/Critical:** Architecture review gate. A peer architect must review and approve the design. Emit `[gov:design:architecture:<complexity>:L4:gate-approved]`.

Handoff to implementation with complete architecture design artifacts.
