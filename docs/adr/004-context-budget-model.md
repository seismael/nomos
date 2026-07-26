# ADR-004: Context Budget Model

**Date:** 2026-07-25
**Status:** Accepted

## Context

AI coding agents have finite context windows. The governance framework defines ~46 artifacts that an agent might need to load for a given task. Loading all of them would consume thousands of tokens — potentially 10-20% of an agent's available context — before the agent even begins working on the task.

Without a budget management strategy, the governance framework risks:
1. **Context exhaustion:** Agents run out of context for actual implementation work.
2. **Slow dispatch:** Loading 46 files sequentially on every task adds latency.
3. **Adoption resistance:** Teams may disable governance because "it uses too much context."

We need a mechanism that lets agents load governance artifacts proportionally to available context budget.

## Decision

Each artifact declares its approximate token cost via a `context_cost` field in the registry:

| Level | Token Budget | Load Strategy |
|---|---|---|
| `low` | <500 tokens | Always load. Safe to include in any context. |
| `medium` | <2000 tokens | Load when budget permits. Skip only in very tight contexts. |
| `high` | <5000 tokens | Load on demand. Summarize (first 200 tokens + "load full file for details") when budget is tight. |

Agents estimate their available context and load artifacts proportionally:
1. Low-cost artifacts first (always safe).
2. Medium-cost artifacts next (skip only if budget is critically tight).
3. High-cost artifacts last (summarize if budget is exhausted).

## Consequences

### Positive
- **Budget-aware:** Governance doesn't consume more context than is available.
- **Graduated loading:** Essential artifacts load first; detailed reference material loads on demand.
- **Transparent costs:** Artifact costs are declared in the registry, not hidden. Teams can see which artifacts are expensive.
- **Simple model:** 3 levels, not continuous token counts. Easy for agents to reason about.

### Negative
- **Self-reported costs:** Artifact authors estimate token costs. Inaccurate estimates could cause over- or under-loading. Validators flag `context_cost` but don't verify actual token counts.
- **No enforcement:** The framework recommends budget management but doesn't enforce it. Agents could still load everything and exhaust context.
- **Summarization loss:** Summarized artifacts lose detail. The "load full file for details" pattern requires the agent to make a second read — two round trips instead of one.

### Neutral
- Most conventions are `low` cost. Most workflows and skills are `medium`. The default persona is `low`. Only verbose reference material is `high`.

## Alternatives Considered

### Alternative 1: Load everything, no budget management
Simplest approach. Rejected because it consistently consumes 5,000-10,000 tokens of context. For agents with 128K context, this is acceptable. For agents with 32K or less, it's prohibitive. The budget model supports both.

### Alternative 2: Precise token counting
Store exact token counts instead of 3 levels. Rejected because token counts vary by model (different tokenizers produce different counts), and precise counts create false precision. The 3-level model is "good enough" and simpler.

### Alternative 3: Agent decides without hints
Let agents load what they think they need without `context_cost` hints. Rejected because agents can't estimate token costs without reading the files first, creating a chicken-and-egg problem.
