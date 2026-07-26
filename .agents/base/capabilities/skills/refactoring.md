---
role: capability
mode: skill
triggers: { phase: "*", type: refactor, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Refactoring

Reference material for agents working on refactor-type tasks. Load alongside refactor planning and implementation workflows.

## Golden Rule

**Behavior MUST NOT change.** Refactoring is structural improvement without functional change. Tests are the proof.

If you change behavior, it's not a refactor — it's a feature or a bugfix. Call it what it is. Don't hide behavior changes inside "refactoring" commits.

## Safety Net First

Before any refactoring:
1. Run the full test suite. All tests must pass.
2. If test coverage is thin (<60%), write characterization tests for the code being refactored. These capture current behavior so you can detect regressions.
3. Commit the baseline. This is your rollback point.

**Do not refactor without a safety net.** If you can't establish one, the risk of silent behavior change is unacceptably high.

## Small Steps

Each refactoring step should:
- Be small enough to complete in one commit (ideally <50 lines changed).
- Keep tests green — no partially-broken intermediate states.
- Be reversible — if this step was wrong, you can revert just this commit without losing other work.
- Be describable in a single sentence: "Extract `TokenValidator` class from `AuthService`."

## Common Patterns

| Pattern | When to Use | Example |
|---|---|---|
| **Extract Method** | Long function with a coherent sub-task | `processOrder()` → extract `validateOrder()`, `calculateTotal()` |
| **Extract Class** | Class has multiple responsibilities | `UserManager` → `UserRepository` + `UserNotifier` |
| **Inline Method** | Method body is as clear as the name | `getUserName(u)` → inline `u.name` |
| **Rename** | Name doesn't describe intent | `data` → `orderItems`, `process()` → `checkout()` |
| **Replace Conditional with Polymorphism** | Switch/if-else chain on type | `if type == "credit"` → `CreditPayment.process()` |
| **Introduce Parameter Object** | 4+ parameters that travel together | `(name, email, phone)` → `ContactInfo(name, email, phone)` |
| **Replace Magic Number with Constant** | Numeric literal with unclear meaning | `86400` → `SECONDS_PER_DAY` |

## Code Smells That Justify Refactoring

| Smell | What It Looks Like | Why Refactor |
|---|---|---|
| **Duplicated Code** | Same logic in 2+ places | Bugs fixed in one copy survive in the other |
| **Long Method** | >30 lines, multiple indentation levels | Hard to understand, test, and reuse |
| **Large Class** | >300 lines, 10+ methods | Multiple responsibilities crammed into one class |
| **Long Parameter List** | 4+ parameters | Hard to call correctly, easy to confuse order |
| **Divergent Change** | One class changes for unrelated reasons | SRP violation — split by responsibility |
| **Shotgun Surgery** | One change requires edits across many classes | Coupling — consolidate related behavior |
| **Feature Envy** | Method uses another class's data more than its own | Move the method to where the data lives |
| **Primitive Obsession** | Using strings/ints for domain concepts | `status: string` → `OrderStatus` enum/value object |

## When NOT to Refactor

- **During a feature deadline.** The feature ships first. File a refactor ticket for after.
- **Code that's about to be replaced.** Why polish something you're throwing away? Check the roadmap.
- **When tests don't exist and can't be added.** No safety net = no refactoring.
- **Scope creep.** "While I'm here, I'll also refactor the auth module." No. Separate commit, separate PR, or separate ticket.
