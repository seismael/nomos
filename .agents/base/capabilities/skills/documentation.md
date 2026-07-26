---
role: capability
mode: skill
triggers: { phase: "*", type: docs, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Documentation

Reference material for agents working on docs-type tasks. Covers what to document, how, and when not to.

## Core Principle

**Explain why, not what.** Code shows *what* the system does. Documentation explains *why* it does it that way, *how* to use it, and *what context* the reader needs.

A comment that reads "increment the counter" next to `counter++` is noise. A comment that reads "counter tracks active connections; must be thread-safe because the connection pool is shared across goroutines" is valuable.

## Doc Types & Formats

| Type | Audience | Content | Format |
|---|---|---|---|
| **README** | New developers, visitors | What, setup, run, test, contribute, license | Project root `README.md` |
| **API Docs** | Developers using your code | Function signatures, parameters, returns, errors, examples | TSDoc/JSDoc/Docstrings in code |
| **ADR** | Team, future maintainers | Context, decision, consequences, alternatives | `docs/adr/NNNN-title.md` |
| **Guides** | Developers doing specific tasks | Step-by-step, code examples, expected outcomes | `docs/guides/` |
| **Runbooks** | Operations, on-call | Diagnostic steps, common issues, escalation path | `docs/ops/` or operations wiki |

## What to Document

- **Public APIs:** Every exported function, class, and module. Include purpose, parameters, return value, exceptions, and a usage example.
- **Architecture decisions:** Every significant design choice gets an ADR. Non-obvious trade-offs, rejected alternatives, and future implications.
- **Domain concepts:** Business-specific terminology and rules. A glossary if the domain is complex.
- **Setup:** A README that gets a new developer from zero to running tests in <5 minutes.

## What NOT to Document

- **Obvious code:** The code itself is the best documentation for what it does. Don't repeat the code in comments.
- **Implementation details likely to change:** Document the contract (public API), not the internals. Internals change; contracts shouldn't.
- **Commented-out code:** Delete it. Version control remembers. Commented-out code confuses readers and rots.

## Keep It Current

- Docs that lie are worse than no docs. Outdated documentation actively misleads readers.
- Update docs in the same PR that changes the behavior they describe.
- Delete obsolete docs. Version control preserves history. Dead docs are noise.
- If you find outdated docs but can't fix them now, file a ticket. Don't let them rot.

## Audience Awareness

- **Developer docs** assume technical knowledge but not codebase familiarity. Explain the architecture, not what a function is.
- **User docs** assume zero technical knowledge. No jargon. Every term defined. Screenshots for UI.
- **Ops docs** assume infrastructure knowledge. Focus on what's specific to this system: ports, dependencies, failure modes, recovery procedures.

## Remove Before Adding

Before writing new documentation, check if existing docs can be updated instead. Duplicate information diverges. One canonical source > two partial sources.

## Good Documentation Answers

- What problem does this solve?
- How do I use it? (with example)
- What are the edge cases?
- What does it depend on?
- What errors can occur and how are they handled?
