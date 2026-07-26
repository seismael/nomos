---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 1
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# General Coding Conventions

## Precision and Minimalism

- Every line must justify its existence. If it doesn't add clarity, safety, or functionality, remove it.
- Write the smallest working solution. Resist speculative generality.
- Prefer clarity over cleverness. A naive but readable solution beats an optimized but opaque one.
- Surgical edits: change only what the task requires. No drive-by refactoring in feature commits.

## YAGNI (You Aren't Gonna Need It)

- Don't build abstractions for hypothetical future requirements.
- Don't add interfaces "just in case." A single concrete implementation is fine until a second one exists.
- Don't extract shared code until the duplication is proven harmful (rule of three: copy once, refactor on the third occurrence).
- Exceptions: security boundaries, data integrity layers, and public API contracts can be designed upfront.

## DRY (Don't Repeat Yourself)

- Duplicate knowledge, not code. Two functions that look similar but serve different domain concepts are not duplication.
- Centralize business rules, validation logic, and domain constants. Don't centralize incidental similarities.
- Configuration over code repetition. Environment-specific values belong in config, not in if-else chains.

## Readability

- Code is read 10x more than written. Optimize for the reader.
- Use descriptive names. A long, clear name beats a short, cryptic one.
- Keep functions small (<30 lines target). Each function should do one thing.
- Avoid nested conditionals beyond 2 levels. Use early returns, guard clauses, or extraction.
- Comments explain *why*, not *what*. The code explains what. Comments explain intent, trade-offs, and context that isn't obvious from the code.

## Composition Over Inheritance

- Prefer composition (has-a) over inheritance (is-a).
- Inheritance is acceptable for "is-a" relationships with shared behavior (e.g., domain exceptions extending a base exception). Not for code reuse.
- Use dependency injection to make dependencies explicit and testable.

## Defensive Minimalism

- Validate inputs at system boundaries (API endpoints, CLI entry points, public library functions).
- Don't validate inputs in internal private functions if the boundaries already guarantee validity.
- Use type systems to prevent invalid states. Make impossible states unrepresentable.
- Assertions are for programmer errors (bugs). Exceptions are for recoverable runtime errors.

## Consistency

- Follow existing patterns in the codebase. Consistency within a project outweighs personal preference.
- If the existing pattern is wrong, fix it everywhere in a dedicated refactor — not mixed with a feature.
- Use automated formatters and linters. Don't argue about formatting; configure the tool and move on.
