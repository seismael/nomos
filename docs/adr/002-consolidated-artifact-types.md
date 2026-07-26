# ADR-002: Consolidated Artifact Types

**Date:** 2026-07-25
**Status:** Accepted

## Context

The initial design proposed 8 artifact types: workflows, skills, personas, tools, templates, subagents, orchestration gates, and conventions. Each type had its own directory and conceptual model.

This created several problems:
1. **Cognitive overhead:** Agents and developers had to learn 8 different concepts to navigate the governance system.
2. **Overlap:** Workflows, skills, and personas are all "agent instructions" — a workflow orchestrates skills, a persona is a specialized skill. The boundaries were blurry.
3. **Directory bloat:** 8 directories at the top level of `.agents/base/` made discovery harder.
4. **Tooling complexity:** Validators, the registry schema, and frontmatter validation had to handle 8 different types with their own rules.

## Decision

Consolidate to 4 artifact types:

| Type | Contains | Rationale |
|---|---|---|
| **capabilities** | workflows, skills, personas | All are "agent instructions with a mode." A workflow is a capability applied at a phase. A persona is a capability with behavioral constraints. A skill is a capability for a task type. |
| **conventions** | code standards, naming, structure, philosophy | Static rules that don't change per task. Always applied. |
| **config** | tools, templates | Both are static configuration artifacts loaded at baseline. |
| **orchestration** | gates, approval flows, subagents | Everything that controls *how* work is delegated and gated. |

Capabilities use an additional `mode` field (`workflow | skill | persona`) to distinguish sub-types without creating separate top-level directories.

## Consequences

### Positive
- **Simpler mental model:** 4 types instead of 8. Each type has a clear, non-overlapping purpose.
- **Fewer directories:** `capabilities/workflows/`, `capabilities/skills/`, `capabilities/personas/` share a parent. `config/tools/` and `config/templates/` share a parent.
- **Easier extensibility:** Adding a new capability variant (e.g., "checklist") requires only adding a new `mode` value and a subdirectory — no new top-level type.
- **Smaller registry schema:** Validators handle 4 roles instead of 8, with `mode` as a secondary discriminator.

### Negative
- **Mode field ambiguity:** Not all tooling will understand the `mode` distinction. Validators must accept capabilities with or without a `mode` field.
- **Migration cost:** Projects that adopted the 8-type system must remap their directories. (This project is the first implementation, so no migration cost exists.)

### Neutral
- The conceptual grouping (workflows by phase, skills by type, personas by role) is preserved within the `capabilities/` directory structure.

## Alternatives Considered

### Alternative 1: Keep 8 types
Rejected for the reasons stated in Context — too many concepts, blurry boundaries, directory bloat.

### Alternative 2: 3 types (capabilities, rules, tools)
Merge conventions into rules, config into tools. Rejected because conventions (code standards) and config (tool configuration) serve different purposes and have different lifecycle expectations. Conventions are principles; config is actionable settings.

### Alternative 3: 2 types (instructions, configuration)
Extreme flattening. Rejected because it loses too much semantic distinction. "Instructions" would contain workflows, skills, personas, conventions, and orchestration — a catch-all that defeats the purpose of categorization.
