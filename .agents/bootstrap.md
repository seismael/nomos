# Agent Governance — Bootstrap

> **READ THIS FIRST.** This is the single entry point to the agent governance framework.
> Every other file is discovered through this one. Read it once at session start.

## 1. Load the Registry

Read `.agents/registry.yaml`. This is the **single source of truth** for every governance artifact. It declares:
- The active governance profile (`active_profile`)
- The cascade layer stack (`layers`)
- Every artifact: its path, role, triggers, layer, priority, status, and context cost

Never maintain a separate artifact index. The registry is authoritative.

## 2. Load the Active Profile

Read `.agents/profiles/<active_profile>.yaml` (profile name from `registry.yaml` `active_profile`). Profiles control **which layers and categories are active**:
- `minimal` — L1 only, conventions only. Baseline code standards.
- `standard` — L1 + L2 + L3 + L5. Conventions, workflows, skills, and project context.
- `full` — All layers. Full orchestration with governance gates.

## 3. Follow the Cascade Protocol

Read `AGENTS.md` for the layered dispatch protocol.

The execution flow:
1. **CLASSIFY** your task — phase × type × complexity (see AGENTS.md taxonomy)
2. **LAYER** — resolve matching artifacts from `registry.yaml` for each active layer
3. **COMPOSE** — merge artifacts in layer order: base → phase → type → complexity → project
4. **EXECUTE** — follow resolved instructions
5. **MARK** — emit `[gov:<phase>:<type>:<complexity>:<layer>:<action>]` compliance markers

## 4. Context Budget Management

Artifacts declare their token cost via `context_cost` in the registry:
- `low` (<500 tokens) — always load
- `medium` (<2000 tokens) — load when budget permits
- `high` (<5000 tokens) — load on demand, summarize if tight

Estimate available context. Load low-cost artifacts first. For high-cost artifacts with tight budget, read the first ~200 tokens + note "load full file for details."

## 5. Override Resolution

If a project artifact (L5) shares the same path prefix as a base artifact:
1. Check the base artifact's `overridable` field
2. If `overridable: false` — skip the project override, use base only
3. If `overridable: true` — apply `override_strategy`:
   - `replace` — use project artifact exclusively
   - `extend` — base content then project content appended
   - `prepend` — project content then base content appended

## 6. Fallback Chain

| Scenario | Behavior |
|---|---|
| `bootstrap.md` missing | Read AGENTS.md directly. Resolve registry paths by convention. |
| `registry.yaml` missing | Load `base/conventions/` only. Emit `[gov:*:*:*:L0:registry-missing]`. |
| `profiles/<active>.yaml` missing | Default to `standard` profile. |
| Trigger has no matching artifact | Skip that layer. Emit `[gov:*:*:*:Lx:artifact-missing]`. |
| Multiple same-priority matches | Load all, alphabetical path order. Emit `[gov:*:*:*:Lx:priority-collision]`. |
| `depends_on` target missing | Skip the dependency. Emit `[gov:*:*:*:Lx:dep-missing]`. |
| Artifact file missing on disk | Skip. Emit `[gov:*:*:*:Lx:artifact-missing]`. |
| Corrupt frontmatter | Skip. Emit `[gov:*:*:*:Lx:parse-error]`. |

**Principle:** Degrade gracefully. A partially-loaded governance stack is better than a blocked agent.

## 7. Compliance Markers

Emit markers at key governance checkpoints:
```
[gov:<phase>:<type>:<complexity>:<layer>:<action>]
```

Examples:
- `[gov:plan:feature:complex:L4:gate-approved]`
- `[gov:implement:bugfix:standard:L2:workflow-loaded]`
- `[gov:test:feature:trivial:L4:gate-skipped]`

At task completion, emit: `[gov:<phase>:<type>:<complexity>:done]`
