---
role: capability
mode: skill
triggers: { phase: "*", type: feature, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Feature Development

Reference material for agents working on feature-type tasks. Load alongside feature planning and implementation workflows.

## Key Principles

- **Start with a failing test.** Every feature starts with a test that defines the desired behavior. No exceptions for non-trivial features.
- **Incremental delivery.** Build the feature in vertical slices that each deliver user-visible value. Don't build all layers before any layer works.
- **Working software over comprehensive docs.** The code and tests are the primary artifacts. Design docs support implementation; they don't replace it.
- **Backward compatibility.** Unless the feature explicitly replaces old behavior, existing APIs and behaviors must continue working.

## Common Patterns

- **Feature flags:** Wrap new behavior in a flag so it can be deployed dark, tested in production, and rolled back instantly. Remove the flag after the feature is stable (within 1-2 sprints).
- **API versioning:** If the feature changes a public API, version it (`/v2/orders`). Keep the old version working during a deprecation period.
- **Database migrations:** Schema changes must be backward-compatible. Add columns (nullable with default) before removing old ones. Multi-step: add → migrate data → remove old column.
- **Event-driven features:** New behavior triggered by events is loosely coupled. Emit events after state changes; don't couple the emitter to consumers.

## Anti-Patterns

- **Big bang PRs:** A single PR with 47 files and 3000 lines. No reviewer can effectively review this. Break features into reviewable chunks.
- **Gold-plating:** Adding polish, extra features, or optimizations not in the spec because "it would be nice." It wouldn't. Ship the spec, iterate.
- **Premature optimization:** Optimizing before measuring. Write clear, correct code first. Profile. Then optimize only the hot paths.
- **Building without requirements:** Starting implementation before understanding what "done" means. If acceptance criteria aren't clear, stop and clarify.

## Deliverables

| Complexity | Deliverables |
|---|---|
| Trivial | Working code + tests |
| Standard | Working code + tests + brief design notes in PR |
| Complex | Design doc + ADR (if architectural) + implementation plan + working code + tests |
| Critical | All complex deliverables + architecture review + deployment plan |

## Quality Checklist

Before marking a feature done:
- [ ] All acceptance criteria met (with evidence, not assumption).
- [ ] Test suite passes. New tests cover the feature's behavior and edge cases.
- [ ] No regressions in existing tests.
- [ ] Linter and formatter pass without warnings.
- [ ] No debug code, commented-out blocks, or TODO-without-tracking-issue.
- [ ] PR description explains what, why, and how tested.
- [ ] Governance markers emitted at all required gates.
- [ ] Feature flag cleanup plan (if applicable) filed as a follow-up.
