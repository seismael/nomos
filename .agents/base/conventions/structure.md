---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 3
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Structure Conventions

## Domain-Based Organization

- Organize code by domain concept, not by technical layer.
- Good: `src/orders/`, `src/users/`, `src/payments/` — each contains its own models, services, and tests.
- Bad: `src/models/`, `src/services/`, `src/controllers/` — cross-cutting by layer makes domain boundaries invisible.
- Within a domain directory, co-locate related files: `orders/models.py`, `orders/services.py`, `orders/tests/`.
- Shared cross-domain code goes in a `common/` or `shared/` directory. Use sparingly — elevate to a proper domain if it grows.

## File Size Limits

| Limit | Rule |
|---|---|
| **200 lines** | Target. Most files should be around this size. |
| **300 lines** | Soft limit. Re-evaluate if a file exceeds this. Is it doing too much? |
| **500 lines** | Hard limit. Break it up. Files this large indicate a design problem. |

- These are guidelines, not absolute rules. Generated code, large data mappings, and well-structured config files can exceed limits.
- When breaking up a large file, split by responsibility, not arbitrarily. Each resulting file should have a clear purpose.

## Module Boundaries

- **DAG (Directed Acyclic Graph):** Module dependencies must form an acyclic graph. No circular imports.
- High-level modules (domain logic) should not depend on low-level modules (infrastructure). Both depend on abstractions.
- Each module should expose a minimal public API. Internal implementation details stay internal.
- Dependencies should flow inward: infrastructure → application → domain. The domain has no external dependencies.

## Test Co-location

- Tests live alongside the code they test, not in a separate `tests/` top-level directory (unless the language ecosystem standard demands it).
- Python: `test_<module>.py` in the same directory, or `tests/test_<module>.py` adjacent.
- TypeScript/JavaScript: `<module>.test.ts` in the same directory.
- Integration and e2e tests can live in a top-level `tests/` directory since they often span multiple domains.
- Test utilities and fixtures should be in `tests/conftest.py`, `tests/setup.ts`, or equivalent.

## Entry Points

- Each project should have a small number of well-defined entry points.
- CLI applications: a single `main()` or `cli.py` that bootstraps the application.
- Web applications: a single `app.py` / `server.ts` that assembles the application graph.
- Libraries: a clear public API in `__init__.py` / `index.ts` that exports only what consumers need.
- Internal scripts live in `scripts/`. Not part of the application's public interface.

## Dependency Direction

```
domain/entities/         ← no dependencies
domain/services/         ← depends on entities
application/use-cases/   ← depends on domain
infrastructure/          ← depends on application abstractions
presentation/            ← depends on application
```

- Each layer depends only on layers to its left.
- Interfaces/abstract classes define contracts at layer boundaries.
- Concrete implementations are injected at startup. No layer instantiates a class from a layer to its right.
