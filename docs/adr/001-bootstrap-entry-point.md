# ADR-001: Bootstrap Entry Point

**Date:** 2026-07-25
**Status:** Accepted

## Context

AI coding agents need to discover and load governance artifacts when entering a project. Without a defined entry point, agents either:
1. Read nothing and operate with no governance.
2. Read AGENTS.md but don't know about additional artifacts.
3. Require platform-specific configuration to discover governance.

We need a single, unambiguous file that an agent can read first and from which it discovers everything else. This file must be platform-agnostic and work with any AI coding agent.

## Decision

Use `.agents/bootstrap.md` as the single entry point. This file:
1. Tells the agent to load `registry.yaml` (the canonical artifact index).
2. Tells the agent to load the active profile.
3. References `AGENTS.md` for the cascade protocol.
4. Defines the fallback chain for missing or corrupt artifacts.
5. Defines the compliance marker format.

The file is placed in `.agents/` alongside the artifacts it references, making it self-contained within the governance directory.

## Consequences

### Positive
- **Discoverable:** One file. Read it first. Everything follows.
- **Self-documenting:** The file itself explains how to bootstrap the system.
- **Platform-agnostic:** Works with any agent that can read files. No special tooling needed.
- **Fallback chain:** If `bootstrap.md` is missing, the agent falls back to reading `AGENTS.md` directly. If `registry.yaml` is missing, it loads only `base/conventions/`.
- **Degrades gracefully:** Missing or corrupt files don't block the agent.

### Negative
- Adds one more file that must be maintained.
- Bootstrap.md itself has no frontmatter (not a governed artifact), which means agents must treat it specially.

### Neutral
- The bootstrap protocol is declarative, not imperative. Agents must implement it themselves.
- Some agents may not support multi-step bootstrap discovery. In those cases, the fallback chain ensures minimal governance (baseline conventions) still applies.

## Alternatives Considered

### Alternative 1: AGENTS.md as entry point
AGENTS.md could be the entry point, with all routing logic embedded. Rejected because AGENTS.md would become bloated and would duplicate registry information. The single-source-of-truth principle requires the registry to be separate.

### Alternative 2: Platform-specific configuration
Use IDE/agent-specific config (e.g., `.claude/`, `.opencode/`, workspace settings). Rejected because it's not portable. Each platform would need its own configuration, violating the "generic, reusable" goal.

### Alternative 3: No bootstrap, agent globs for files
Let agents search `.agents/` for files matching their task. Rejected because globbing is slow, fragile, and doesn't provide ordering (layer priority). The registry provides ordering and explicit trigger matching that globbing cannot.
