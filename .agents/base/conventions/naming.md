---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 2
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Naming Conventions

## General Principles

- Names should describe intent, not implementation. `calculateTax()` not `applyFormulaB()`.
- Full words, no arbitrary abbreviations. `configuration` not `cfg`, `repository` not `repo` unless `repo` is the domain term.
- Pronounceable names. If you can't say it in a code review, it's a bad name.
- Searchable names. Single-letter variables only for loop counters (`i`, `j`, `k`) and well-known mathematical notation (`x`, `y`, `r`).

## Functions and Methods

- Verb phrase — describes what the function does: `fetchUser()`, `validateEmail()`, `renderPage()`.
- Boolean-returning functions: prefix with `is`, `has`, `can`, `should`: `isValid()`, `hasPermission()`, `canEdit()`.
- Event handlers: `on` + event: `onClick()`, `onSubmit()`, `onDataLoaded()`.
- Async functions: no special prefix. The return type (Promise/Future/Task) makes it obvious.

## Classes, Types, and Interfaces

- Noun or noun phrase: `UserRepository`, `OrderService`, `EmailValidator`.
- Don't repeat the type in the name: `User` not `UserClass`. `IUser` (Hungarian notation) is noise in modern type systems.
- Exception classes end with `Exception` or `Error`: `ValidationException`, `NotFoundError`.
- Abstract base classes: no special prefix unless the language convention demands it. Name for the abstraction: `PaymentProcessor` not `AbstractPaymentProcessor`.

## Variables and Properties

- Noun or noun phrase: `userCount`, `isActive`, `items`.
- Boolean variables: `is`/`has`/`can`/`should` prefix: `isLoading`, `hasErrors`, `canSubmit`.
- Collections: plural form: `users`, `orderItems`, `availableTaxRates`. Avoid type suffixes (`_list`, `_array`, `_set`).
- Constants (immutable values): `UPPER_SNAKE_CASE` in most languages: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS`.
- Private/protected fields: language convention. No Hungarian notation prefixes (`m_`, `_` only if language standard).

## Files and Directories

- Files: `kebab-case` or the language convention. `user-repository.ts`, `order_service.py`.
- Test files: mirror the source file with `.test` or `_test` suffix: `user-repository.test.ts`, `test_order_service.py`.
- Directories: `kebab-case` (or `snake_case` for Python packages). `src/components/user-profile/`, `app/services/`.
- One primary class/component per file. Filename matches the primary export.
- Entry points use conventional names: `index.ts`, `__init__.py`, `main.go`.

## Domain Language

- Use the business domain's terminology. If the business says "policy" not "rule", use `Policy`.
- Maintain a ubiquitous language across the codebase, docs, and conversations. The same concept should have the same name everywhere.
- When the domain term is ambiguous, resolve with the domain expert and document the decision in an ADR.
