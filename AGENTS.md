# AGENTS.md — Governance Protocol v1.0.0

## Protocol: Layered Dispatch

Every agent task follows this protocol:

1. **CLASSIFY** — Determine `phase × type × complexity` (see taxonomy below)
2. **LAYER** — Resolve matching artifacts from `.agents/registry.yaml` for each active layer
3. **COMPOSE** — Merge artifacts in layer order: base → phase → type → complexity → project
4. **EXECUTE** — Follow resolved instructions, applying the conventions, workflows, and skills
5. **MARK** — Emit `[gov:...]` compliance markers at each gate checkpoint

Entry point: Read `.agents/bootstrap.md` first. It explains discovery, profiles, and fallbacks.

## Taxonomy

Classify every task along three dimensions:

| Dimension | Values |
|---|---|
| **Phase** | `plan`, `design`, `implement`, `test`, `review`, `deploy` |
| **Type** | `feature`, `bugfix`, `refactor`, `architecture`, `research`, `docs`, `ops` |
| **Complexity** | `trivial`, `standard`, `complex`, `critical` |

**Complexity definitions:**
- **trivial** — Single file, <20 lines, no design decisions (typo fix, one-line config)
- **standard** — Few files, bounded scope, straightforward (single component, well-scoped fix)
- **complex** — Multi-file, architectural impact, meaningful trade-offs (new feature, cross-cutting refactor)
- **critical** — System-wide, data integrity, security, production risk (auth change, schema migration, deploy)

## Cascade

See `.agents/registry.yaml` → `layers` for the active layer stack.

| Layer | Name | Description |
|---|---|---|
| L1 | base | Always applied — baseline conventions and default persona |
| L2 | phase | Applied by phase match (plan, design, implement, etc.) |
| L3 | type | Applied by type match (feature, bugfix, etc.) — skills + specialized personas |
| L4 | complexity | Governance gates — approval flows, subagent rules |
| L5 | project | Project-specific overrides (project context, team conventions) |

Layers apply in order. Later layers extend or override earlier ones per the override contract.

## Override Rules

1. Base artifacts declare `overridable: true | false` in the registry
2. If `overridable: false`, project overrides targeting that artifact are ignored
3. Merge strategy: `replace` (use override only), `extend` (base + append), `prepend` (override + append base)
4. Project overrides share the same path prefix as the base artifact they override

## Governance Gates

Gates are complexity-based. Defined in `.agents/base/orchestration/gates.yaml`.

| Complexity | Gates |
|---|---|
| trivial | None |
| standard | Verify after completion |
| complex | Plan approved → Design approved → Review approved |
| critical | Plan → Design → Review → Test → Deploy review |

Agents must emit a compliance marker at each gate:
```
[gov:<phase>:<type>:<complexity>:L4:gate-approved]
[gov:<phase>:<type>:<complexity>:L4:gate-skipped]
```

## Artifact Types

| Type | Directory | Contents |
|---|---|---|
| conventions | `base/conventions/` | Code standards, naming, structure, testing philosophy |
| capabilities | `base/capabilities/` | Workflows, skills, personas |
| config | `base/config/` | Tool defaults, templates (design docs, ADRs, PRs) |
| orchestration | `base/orchestration/` | Gates, approval flows, subagent definitions |

## Compliance Checklist

Before completing any task, verify:

- [ ] Task classified: phase × type × complexity
- [ ] Bootstrap loaded: registry + profile resolved
- [ ] L1 base conventions applied
- [ ] L2 phase workflow followed (if applicable)
- [ ] L3 type skill referenced (if applicable)
- [ ] L4 gates passed (if standard/complex/critical)
- [ ] L5 project overrides applied (if they exist)
- [ ] Compliance markers emitted at each gate
- [ ] Final marker emitted: `[gov:<phase>:<type>:<complexity>:done]`

## Single Source of Truth

`.agents/registry.yaml` is the canonical artifact index. AGENTS.md does not duplicate artifact paths. If registry and AGENTS.md conflict, registry wins. Adding a new artifact requires:
1. The artifact file itself
2. An entry in `registry.yaml`
