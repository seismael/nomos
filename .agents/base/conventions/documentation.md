---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 5
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Documentation Conventions

## What to Document

- **Why, not what.** Code explains what. Comments and docs explain why: intent, context, constraints, trade-offs. A comment reading "increment the counter" next to `counter++` is noise.
- **Public APIs.** Every public function, class, and module should have a docstring describing its purpose, parameters, return value, and any side effects or exceptions.
- **Architecture decisions.** Any non-obvious design choice gets an ADR (Architecture Decision Record) in `docs/adr/`. See the ADR template.
- **Domain concepts.** Non-obvious business rules and terminology should be documented. A new team member should be able to understand the domain from the docs.
- **Setup and onboarding.** `README.md` should get a developer from zero to running tests in under 5 minutes.

## What NOT to Document

- **Obvious code.** `// Set name to "Alice"` adds nothing to `name = "Alice"`.
- **Implementation details that change frequently.** Docs that rot are worse than no docs. If it changes with every feature, keep it in the code.
- **Commented-out code.** Delete it. Version control remembers. Commented-out code confuses readers ("is this intentionally disabled? should I uncomment it?").

## Docstring Standards

- **Python:** Google-style docstrings. One-line summary, optional Args/Returns/Raises sections.
- **TypeScript/JavaScript:** TSDoc/JSDoc for all exported functions, classes, and types. `@param`, `@returns`, `@throws`.
- **Java:** Javadoc for all public and protected members.
- **Go:** Godoc comments. Start with the name of the thing being described.

## HACK / TODO / FIXME Markup

Use standardized tags for inline notes. Always include a reason and, if possible, a reference:

```
// HACK: Workaround for library bug in v2.3. Remove after upgrade to v2.4. See issue #123.
// TODO(author): Add caching layer to reduce DB calls. Tracked in JIRA-456.
// FIXME: This fails for negative values. Need to discuss requirements with PM.
```

- `HACK` — temporary workaround with an exit plan.
- `TODO` — planned future work with an owner.
- `FIXME` — known broken behavior that needs attention.
- Don't leave these lingering. Either fix it or don't mark it.

## ADR Format

Architecture Decision Records follow a consistent format. See the ADR template in `.agents/base/config/templates/adr-template.md`.

Each ADR captures:
- **Context:** What is the problem? What constraints exist?
- **Decision:** What did we choose and why?
- **Consequences:** What becomes easier? What becomes harder?
- **Alternatives:** What else did we consider? Why wasn't it chosen?

ADRs are immutable once accepted. If a decision is superseded, create a new ADR and reference the old one. Don't edit old ADRs.

## README

Every project has a README.md at the root. Minimum contents:
- What the project does (one sentence)
- How to set up (prerequisites, install, run)
- How to run tests
- How to contribute
- License

The README is the first thing visitors see. Keep it current, keep it clear.
