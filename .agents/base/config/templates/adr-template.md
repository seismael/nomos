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

# ADR Template

Copy to `docs/adr/NNNN-<title-with-dashes>.md` where NNNN is the next sequential number.

---

# ADR-NNNN: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Supersedes:** ADR-NNNN (if applicable)
**Superseded by:** ADR-NNNN (if applicable)

## Context

What is the problem? What constraints exist (technical, business, organizational)? What forces are at play? Include enough background that someone unfamiliar with the project can understand why this decision matters now.

## Decision

What did we decide? Be specific. Include technical details. "We chose PostgreSQL" is not enough. "We chose PostgreSQL as the primary data store, using its JSONB columns for semi-structured order data and its full-text search for the product catalog. All writes go through the OrderService repository; no other service accesses the database directly."

## Consequences

### Positive
What improves because of this decision? What becomes easier?

### Negative
What trade-offs are we accepting? What becomes harder? What risks are introduced?

### Neutral
What changes but isn't clearly better or worse?

## Alternatives Considered

### Alternative 1: [Name]
- **Description:** What would this look like?
- **Pros:** Why was it considered?
- **Cons:** Why was it rejected?

### Alternative 2: [Name]
- **Description:** What would this look like?
- **Pros:** Why was it considered?
- **Cons:** Why was it rejected?

## References

- [Link to related docs, discussions, issues, PRs]
