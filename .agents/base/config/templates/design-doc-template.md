---
role: config
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 30
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Design Document Template

Copy to `docs/specs/YYYY-MM-DD-<feature>-design.md` and fill in each section. Delete sections that don't apply.

---

# [Feature Name] — Design Spec

**Date:** YYYY-MM-DD
**Status:** Draft | Review | Approved
**Author:** [Name]

## 1. Purpose

One paragraph: what problem does this solve? Who benefits? Why now?

## 2. Requirements

### Functional
- [Requirement 1]
- [Requirement 2]

### Non-Functional
- **Performance:** [expectations — latency, throughput, resource limits]
- **Security:** [threat model, data sensitivity, auth/authz requirements]
- **Scalability:** [expected growth, peak loads]
- **Accessibility:** [requirements if UI feature]
- **Observability:** [metrics, logs, alerts needed]

## 3. Design

### Architecture
High-level description of components and their relationships. Keep it to one paragraph. Include a diagram reference if helpful.

### Components

| Component | Responsibility | Dependencies |
|---|---|---|
| [Name] | [What it does, single responsibility] | [What it needs from other components] |

### Data Flow
How data moves through the system. Input → processing → output. Cover both the happy path and error paths.

### Interfaces
API contracts for new public interfaces:
```
functionName(param1: Type, param2: Type): ReturnType
  - Purpose: [what it does]
  - Errors: [what errors it can produce]
  - Example: [usage example]
```

### Error Handling
What errors can occur? How are they classified (recoverable / non-recoverable / fatal)? Where are they caught? What does the user see?

## 4. Alternatives Considered

| Approach | Pros | Cons | Why Rejected |
|---|---|---|---|
| [Approach 1] | | | |
| [Approach 2] | | | |

## 5. Testing Strategy

- **Unit tests:** What to test at the unit level. Specific scenarios.
- **Integration tests:** What to test across component boundaries.
- **E2E tests:** Critical user journeys to verify.
- **Edge cases:** What boundaries, error conditions, and race conditions to test.

## 6. Migration & Rollout

How to deploy this safely:
- Feature flags? Gradual rollout?
- Backward compatibility with existing APIs?
- Database migrations needed? (Must be backward-compatible.)
- Rollback plan if the feature causes issues.

## 7. Open Questions

- [Question 1]
- [Question 2]
