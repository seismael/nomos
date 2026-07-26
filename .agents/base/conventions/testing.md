---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 4
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Testing Conventions

## TDD as Default

- Test-Driven Development is the default workflow: write a failing test first, then implement.
- Exceptions: exploratory prototyping (agree to throw away), configuration changes, trivial boilerplate.
- If you choose not to TDD for a non-trivial change, document why in the commit message or PR description.

## Red-Green-Refactor

1. **Red:** Write a minimal failing test that expresses the desired behavior. Run it; confirm it fails for the expected reason.
2. **Green:** Write the minimal code to make the test pass. Don't optimize, don't add features, don't refactor. Just make it green.
3. **Refactor:** Clean up the code while keeping tests green. Remove duplication, improve names, simplify. The tests have your back.
4. **Repeat:** Each behavior change starts a new Red-Green-Refactor cycle.

## Test Pyramid

```
         ┌──────┐
         │  E2E │  ← Few. Critical user journeys only. Slow.
        ┌┴──────┴┐
        │Integration│ ← Several. Test boundaries between systems.
       ┌┴──────────┴┐
       │   Unit      │ ← Many. Fast, isolated. The foundation.
       └─────────────┘
```

- **Unit tests:** Test a single unit (function, class method) in isolation. Dependencies are mocked/stubbed. Fast (<100ms for the whole suite is the target).
- **Integration tests:** Test how units work together. Real database, real file system, real network (or realistic fakes). Fewer than unit tests, more valuable per test.
- **E2E tests:** Test complete user journeys. Login → create → view → edit → delete. The fewest tests, but the highest confidence. Run in CI, not on every local save.

## Test Behavior, Not Implementation

- Test what the code does, not how it does it. Tests should survive refactoring.
- Bad: test that `calculateTotal()` calls `applyDiscount()` internally.
- Good: test that `calculateTotal([$10, $20], discount="10%")` returns `$27`.
- If a test breaks when you change implementation without changing behavior, the test is too coupled.

## AAA Pattern (Arrange, Act, Assert)

```
# Arrange — set up the test world
user = User(name="Alice", age=30)

# Act — do the thing being tested
result = user.can_purchase_alcohol()

# Assert — verify the outcome
assert result is True
```

- One Act per test. If you need multiple Acts, split into separate tests.
- Arrange should be boring. If setup is complex, extract test fixtures or factories.
- Assert on specific values, not generic truths. `assert result == 42` not `assert result > 0`.

## Test Data

- Use realistic data, not placeholders. `"alice@example.com"` not `"test@test.com"`. `42` not `12345`.
- Don't share mutable test data between tests. Each test creates its own world.
- Use test fixtures/factories for complex object creation. `UserFactory.create(name="Alice")` not 10 lines of property assignment.
- Random test data is acceptable for values where the specific value doesn't matter, but log the seed for reproducibility.

## Coverage Philosophy

- Coverage is a tool, not a goal. 100% coverage doesn't mean well-tested code. It means every line was executed at least once.
- Target 80%+ line coverage, but prioritize testing behavior over hitting metrics.
- Uncovered code is a question, not a failure. Ask: "Is this code reachable? Should it have a test? Should it be deleted?"
- Don't write tests solely to hit coverage targets. Tests that assert nothing of value waste maintenance time.
