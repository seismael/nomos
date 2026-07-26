---
role: capability
mode: skill
triggers: { phase: "*", type: architecture, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Architecture

Reference material for agents working on architecture-type tasks. Load alongside the architect persona and architecture workflows.

## Design Heuristics

Evaluate architectural decisions across these dimensions. Weight them based on what matters most for the specific context.

| Dimension | What It Means | When It Matters Most |
|---|---|---|
| **Simplicity** | Fewest moving parts. Easiest to understand. | Early-stage projects, small teams, tight deadlines |
| **Flexibility** | Easy to change direction. Low coupling. | Evolving requirements, startup environments |
| **Performance** | Throughput, latency, resource efficiency. | High-traffic systems, real-time processing |
| **Maintainability** | Easy to debug, modify, and onboard. | Long-lived systems, large teams, high turnover |
| **Scalability** | Handles growth in users, data, traffic. | Growing products, unpredictable demand |
| **Security** | Threat model, attack surface, data protection. | Regulated industries, user data, financial systems |
| **Testability** | Can each component be verified in isolation? | High-reliability systems, continuous deployment |
| **Observability** | Can you monitor, debug, and understand production? | Distributed systems, microservices, production incidents |

## Architecture Styles

Choose the style that fits the problem. Don't let the style define the problem.

| Style | When to Use | When to Avoid |
|---|---|---|
| **Layered** | Simple CRUD apps, clear separation of concerns | Complex domains where layers become leaky abstractions |
| **Hexagonal (Ports & Adapters)** | Domain-heavy apps, need to swap infrastructure | Simple apps where the extra abstraction is overhead |
| **CQRS** | Read/write patterns differ significantly, high query complexity | Simple CRUD where read and write models are the same |
| **Event-Driven** | Loose coupling between subsystems, async workflows | Simple request-response apps, strong consistency requirements |
| **Microservices** | Independent team ownership, independent scaling needs | Small team, simple domain — use a modular monolith |
| **Modular Monolith** | Single deployable with clear internal boundaries | Need independent deploy or truly independent scaling |

## SOLID at System Level

- **S:** Each bounded context has a single business capability. Don't mix Order and Payment logic in one context.
- **O:** Extend system behavior by adding new contexts or adapters. Don't modify existing context internals to add features.
- **L:** Adapter implementations must satisfy the port contract. A `PaymentGateway` adapter that doesn't handle refunds violates the contract.
- **I:** Context interfaces should be narrow. A `UserContext` shouldn't export admin functions to all consumers.
- **D:** High-level policy (domain) doesn't depend on low-level details (database, HTTP). Dependencies flow inward.

## DDD Strategic Patterns

| Pattern | Description | Example |
|---|---|---|
| **Bounded Context** | A boundary within which a model applies. Inside, terms are consistent. | `Order` in Sales context ≠ `Order` in Fulfillment context |
| **Core Domain** | The business's competitive advantage. Invest the most design effort here. | For Uber: matching riders to drivers |
| **Supporting Subdomain** | Necessary but not differentiating. Use off-the-shelf or simpler designs. | For Uber: billing, notifications |
| **Generic Subdomain** | Commodity. Buy, don't build. | For Uber: authentication, file storage |
| **Anticorruption Layer** | Translate between contexts so foreign concepts don't leak in. | Adapter that translates external API models to your domain models |
| **Context Mapping** | How contexts relate: partnership, shared kernel, customer-supplier, conformist | Documented in ADRs |

## ADR Discipline

Every significant architectural decision MUST produce an ADR. An ADR:
- Captures the decision and its rationale at the moment it was made.
- Is immutable once accepted. If superseded, write a new ADR that references the old one.
- Answers: what did we decide, why, what were the alternatives, what are the consequences?

Use the ADR template. Commit to `docs/adr/`.

## Decision Anti-Patterns

- **Resume-Driven Development:** Choosing technology because it looks good on a resume, not because it solves the problem.
- **Cargo Cult Architecture:** Copying Netflix/Google/Uber patterns because they do it. They have different problems.
- **Analysis Paralysis:** Debating architecture forever instead of building and learning. Decide, build, adapt.
- **Big Design Up Front:** Designing the entire system before writing a line of code. Design enough for the next increment.
- **Ivory Tower Architecture:** Architects who don't write code designing systems. Architecture emerges from building.

## Practical Rule

Start simple. Add complexity only when the simple approach demonstrably fails.

A modular monolith that actually ships is better than a perfect microservices architecture that never finishes.
