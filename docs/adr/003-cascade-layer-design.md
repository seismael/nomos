# ADR-003: Configurable Cascade Layer Design

**Date:** 2026-07-25
**Status:** Accepted

## Context

The governance cascade determines which artifacts load for which task classifications. The initial design hardcoded 5 layers (L1-L5) in AGENTS.md:

```
L1: Core (always applied)
L2: Phase (applied by phase match)
L3: Type (applied by type match)
L4: Complexity (governance gates)
L5: Project (project-specific overrides)
```

This created a rigidity problem: if a team needed a 6th layer (e.g., L6: Team-specific overrides for a multi-team monorepo), they would need to modify AGENTS.md — a breaking change to the central conductor.

Additionally, the layer definitions were duplicated between AGENTS.md (for human readability) and the registry (for machine readability), violating the single-source-of-truth principle.

## Decision

Make the cascade layer stack configurable in `registry.yaml`:

```yaml
layers:
  - id: L1
    name: base
    mandatory: true
  - id: L2
    name: phase
    mandatory: true
  # ... additional layers
```

AGENTS.md references the layer stack without defining it:

```markdown
## Cascade
See `.agents/registry.yaml` → `layers` for the active layer stack.
```

Adding a new layer (e.g., L6: team) requires:
1. Adding a layer entry to `registry.yaml`.
2. Adding artifact entries with `layer: team` (or the new layer ID).
3. Updating the active profile to include the new layer.
4. No AGENTS.md changes.

## Consequences

### Positive
- **Extensible:** Teams can add layers without modifying the core protocol document.
- **Single source of truth:** Layer definitions live only in the registry. No duplication.
- **Profile-controlled:** The active profile determines which layers load. Adding a layer to the registry doesn't activate it unless the profile includes it.
- **Backward compatible:** The default 5-layer stack works identically to the hardcoded version.

### Negative
- Slightly more indirection: an agent must read `registry.yaml` to understand the cascade, not just `AGENTS.md`.
- Validators must handle variable-length layer stacks, not just the fixed 5-layer model.

### Neutral
- The mandatory/optional distinction (`mandatory: true | false`) gives teams control over which layers are required vs optional. This was implicit in the hardcoded version (L1-L4 mandatory, L5 optional) but is now explicit.

## Alternatives Considered

### Alternative 1: Hardcoded 5 layers in AGENTS.md
The original design. Rejected because it's rigid and requires AGENTS.md changes for simple extensions.

### Alternative 2: No layers, flat artifact list
All artifacts in a flat list with priority ordering. Rejected because layers provide semantic grouping (phase, type, complexity) that makes the cascade comprehensible. A flat list would require agents to understand complex priority interactions without semantic context.

### Alternative 3: Plugin-based layer system
Layers as plugins that can be dynamically loaded. Rejected as over-engineered. The governance system is a set of files, not a runtime. Configurable static layers meet the need without plugin complexity.
