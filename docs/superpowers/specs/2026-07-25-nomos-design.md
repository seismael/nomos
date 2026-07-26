# Agent Governance Framework — Design Spec v2

**Date:** 2026-07-25
**Status:** Design approved (v2 — consolidated)
**Author:** Orchestrator + User
**Scope:** End-to-end governance and enforcement infrastructure for AI coding agents

---

## 1. Purpose

A reusable, layered governance framework that controls and routes AI coding agents. AGENTS.md is the central conductor; `.agents/` is the instrument library. Every agent task is classified by phase × type × complexity, then routed to the correct capability, convention, configuration, or orchestration rule.

**Deliverable:** A reusable core (`.agents/base/`) + a project-specific layer (`.agents/project/`) + a bootstrap entry point. The base layer is portable to any project; the project layer contains domain- and stack-specific overrides.

---

## 2. Architecture

### 2.1 Directory Structure

```
your-project/
├── AGENTS.md                                    # Central conductor
├── .agents/
│   ├── bootstrap.md                             # SINGLE ENTRY POINT — agent reads this first
│   ├── base/                                    # REUSABLE — portable to any project
│   │   ├── capabilities/                        # Merged: workflows + skills + personas
│   │   │   ├── workflows/
│   │   │   │   ├── planning/
│   │   │   │   ├── design/
│   │   │   │   ├── implementation/
│   │   │   │   ├── testing/
│   │   │   │   ├── review/
│   │   │   │   └── deploy/
│   │   │   ├── skills/
│   │   │   └── personas/
│   │   ├── conventions/                         # Language-agnostic code standards
│   │   ├── config/                              # Merged: tools + templates
│   │   │   ├── tools/
│   │   │   └── templates/
│   │   └── orchestration/                       # Merged: subagents + gates + flows
│   │       ├── subagents/
│   │       ├── gates.yaml
│   │       └── approval-flows.md
│   ├── project/                                 # PROJECT-SPECIFIC — not copied
│   │   ├── context/
│   │   ├── conventions/
│   │   ├── config/
│   │   └── orchestration/
│   ├── profiles/                                # Governance depth presets
│   │   ├── minimal.yaml
│   │   ├── standard.yaml
│   │   └── full.yaml
│   ├── registry.yaml                            # Machine-readable artifact index (SSOT)
│   └── schema/
│       └── registry.schema.json                 # Formal schema for registry validation
├── docs/
│   ├── adr/                                     # Architecture Decision Records
│   └── superpowers/
│       └── specs/
│           └── 2026-07-25-nomos-design.md
└── scripts/                                     # Validation/verification tooling
    ├── validate-registry
    ├── validate-cascade
    ├── validate-headers
    ├── validate-deps
    └── run-compliance-tests
```

### 2.2 Core Principles

- **Bootstrap-first.** One file (`bootstrap.md`) tells the agent how to discover and load the entire system. No discovery ambiguity.
- **Generic by default, specific by override.** Base artifacts are language-agnostic. Project artifacts override via an explicit merge strategy.
- **Declarative, not imperative.** The protocol tells agents *what* to load and *when*, not *how*. Agents retain execution autonomy.
- **Single source of truth.** `registry.yaml` is the canonical index. AGENTS.md references it. Agents query it. No duplication.
- **Defense in depth.** Every routing path has a defined fallback. No silent failures.
- **Budget-aware.** Artifacts declare their context cost. Agents load proportionally to available budget.
- **Observable.** Every governance action emits a compliance marker. Humans can audit.

### 2.3 Consolidated Artifact Types (4 instead of 8)

| Type | Contains | Rationale |
|---|---|---|
| **capabilities** | workflows, skills, personas | All are "agent instructions with a mode." A workflow is a skill applied at a phase; a persona is a skill with behavioral constraints. |
| **conventions** | code standards, naming, structure, philosophy | Static rules that don't change per task. |
| **config** | tools, templates | Both are static configuration artifacts. |
| **orchestration** | subagent definitions, gates, approval flows | Everything that controls *how* work is delegated and gated. |

---

## 3. Bootstrap & Discovery

### 3.1 Entry Point: `bootstrap.md`

This is the first and only file an agent must read to onboard to the governance system. It contains:

```markdown
# Agent Governance — Bootstrap

## 1. Load the registry
Read `.agents/registry.yaml` — this is the single source of truth for all artifacts.

## 2. Load the active profile
Read `.agents/profiles/<active>.yaml` — this determines which artifact categories are active.
(Active profile is declared in registry.yaml `active_profile` field.)

## 3. Follow the cascade
Read `AGENTS.md` for the layered dispatch protocol.
Classify your task, then resolve artifacts from registry.yaml by layer.

## 4. Fallback rule
If any artifact path resolves to a missing file, skip it and continue.
If registry.yaml is missing, fall back to `.agents/base/conventions/` only (safe minimum).
```

### 3.2 Discovery Sequence

```
bootstrap.md → registry.yaml → profile → AGENTS.md cascade → artifacts
```

Every step has a fallback. If bootstrap.md is missing, the agent falls back to reading AGENTS.md directly (backward compatibility). If registry.yaml is missing, the agent applies only `base/conventions/` as a safe minimum.

---

## 4. AGENTS.md — Protocol & Routing Engine

### 4.1 Protocol Declaration

```markdown
# AGENTS.md — Governance Protocol v1

## Protocol: Layered Dispatch
1. CLASSIFY: phase × type × complexity (see taxonomy)
2. LAYER: resolve artifacts from registry.yaml for each active layer
3. COMPOSE: merge artifacts in layer order (base → phase → type → complexity → project)
4. EXECUTE: follow resolved instructions
5. MARK: emit compliance markers at each gate checkpoint
```

### 4.2 Taxonomy

| Dimension | Values |
|---|---|
| **Phase** | `plan`, `design`, `implement`, `test`, `review`, `deploy` |
| **Type** | `feature`, `bugfix`, `refactor`, `architecture`, `research`, `docs`, `ops` |
| **Complexity** | `trivial`, `standard`, `complex`, `critical` |

Added `ops` to Type — covers infrastructure, CI, deployment changes.

**Invalid combinations:** Some trigger combinations have no defined artifact and will resolve to layer defaults only. The registry marks valid triggers with `valid: true`. Cascade validation warns on unmarked combinations but does not error.

### 4.3 Cascade Rules (Configurable Layers)

The cascade is declared in `registry.yaml`, not hardcoded in AGENTS.md:

```yaml
# registry.yaml (excerpt)
layers:
  - id: L1
    name: base
    description: "Always applied — baseline conventions and defaults"
    mandatory: true
  - id: L2
    name: phase
    description: "Applied by phase match"
    mandatory: true
  - id: L3
    name: type
    description: "Applied by type match"
    mandatory: true
  - id: L4
    name: complexity
    description: "Governance gates"
    mandatory: true
  - id: L5
    name: project
    description: "Project-specific overrides"
    mandatory: false
```

AGENTS.md references this:

```markdown
## Cascade
See `.agents/registry.yaml` → `layers` for the active layer stack.
L1 (base) is always applied. Each subsequent layer is applied when its trigger matches.
```

Adding a team layer (L6) = one entry in registry.yaml `layers`. No AGENTS.md change.

---

## 5. Artifact Format

### 5.1 Uniform YAML Frontmatter

Every `.agents/` file begins with:

```yaml
---
role: capability          # capability | convention | config | orchestration
mode: workflow             # capability: workflow | skill | persona
triggers:
  phase: plan
  type: feature
  complexity: [standard, complex, critical]
layer: phase
priority: 10
status: active             # active | deprecated | retired
depends_on: []
overridable: true          # Can project layer override this?
override_strategy: extend  # replace | extend | prepend
context_cost: low          # low (<500 tokens) | medium (<2000) | high (<5000)
version: 1.0.0
---
```

**Required:** `role`, `triggers`, `layer`, `priority`, `status`, `context_cost`.
**Optional:** `mode`, `depends_on`, `overridable`, `override_strategy`, `version`, `description`.

### 5.2 Context Budget Model

Artifacts declare their token cost via `context_cost`:

| Level | Token budget | Loads |
|---|---|---|
| `low` | <500 | Can always load, even in tight contexts |
| `medium` | <2000 | Load when budget permits |
| `high` | <5000 | Load only when explicitly needed or budget is ample |

Agents estimate available context and load artifacts proportional to budget. If budget is tight, high-cost artifacts are summarized (first 200 tokens + "load full file for details").

### 5.3 Override Contract

Base artifacts declare whether they can be overridden:

- `overridable: true` — project layer can replace/extend
- `overridable: false` — core invariant, project layer cannot touch
- `override_strategy: replace` — project file replaces base entirely
- `override_strategy: extend` — project file appends to base
- `override_strategy: prepend` — project file prepends to base

Agents resolve by: base artifact → check project for same path → apply merge strategy.

---

## 6. Governance Profiles

Profiles control *which artifact categories load* — independent of task complexity gates.

```yaml
# profiles/minimal.yaml
name: minimal
description: "Baseline conventions only. No workflows or gates."
active_layers: [L1]
active_categories: [conventions]
```

```yaml
# profiles/standard.yaml
name: standard
description: "Conventions + phase workflows + type skills. No orchestration gates."
active_layers: [L1, L2, L3, L5]
active_categories: [capabilities, conventions, config]
```

```yaml
# profiles/full.yaml
name: full
description: "All layers, all categories, full orchestration."
active_layers: [L1, L2, L3, L4, L5]
active_categories: [capabilities, conventions, config, orchestration]
```

The active profile is declared in `registry.yaml`:

```yaml
active_profile: full
```

Agents resolve: registry → active profile → which layers and categories to load → which artifacts match triggers.

---

## 7. Observability & Compliance Markers

### 7.1 Marker Format

Every governance checkpoint emits a structured marker:

```
[gov:<phase>:<type>:<complexity>:<layer>:<action>]
```

Examples:
- `[gov:plan:feature:complex:L4:gate-approved]` — human approved the planning gate
- `[gov:implement:bugfix:standard:L2:workflow-loaded]` — loaded the implementation workflow
- `[gov:test:feature:trivial:L4:gate-skipped]` — skipped gates (trivial)

### 7.2 Audit Trail

Agents append markers to their output. A CI step can grep for `[gov:.*]` markers to verify:
- The agent classified its task (marker present at step 1)
- Gates were respected (L4 markers present for complex/critical)
- No marker indicates a gate was skipped → compliance failure

---

## 8. Fallback & Error Handling

| Scenario | Behavior |
|---|---|
| `bootstrap.md` missing | Agent reads AGENTS.md directly. Registry paths resolve by convention. |
| `registry.yaml` missing | Agent loads `base/conventions/` only. Safe minimum. |
| Trigger has no matching artifact | Skip that layer. Log `[gov:*:*:*:Lx:artifact-missing]`. |
| Multiple same-priority matches | Load all in alphabetical path order. Log a warning. |
| `depends_on` missing | Skip the dependency. Log `[gov:*:*:*:Lx:dep-missing]`. |
| Artifact file missing | Skip the artifact. Log `[gov:*:*:*:Lx:artifact-missing]`. |
| Corrupt frontmatter | Skip the artifact. Log `[gov:*:*:*:Lx:parse-error]`. |

**Principle:** The governance system degrades gracefully, never blocks an agent from working. A partially-loaded governance stack is better than a blocked agent.

---

## 9. Artifact Lifecycle

| Status | Meaning | Agent behavior | Validator |
|---|---|---|---|
| `active` | Current, load normally | Load | No warning |
| `deprecated` | Still valid, will be removed | Load + emit `[gov:*:*:*:Lx:deprecated]` | Warning on registry-validate |
| `retired` | No longer valid | Skip + emit `[gov:*:*:*:Lx:retired]` | Error on registry-validate if any trigger still resolves to this |

Deprecated artifacts must set `superseded_by` pointing to the replacement.

---

## 10. Agent Execution Flow (Complete)

1. Agent receives a task.
2. Agent reads `.agents/bootstrap.md` (or falls back to AGENTS.md).
3. Agent loads `.agents/registry.yaml` → discovers active profile + layer stack.
4. Agent loads profile → determines active categories.
5. Agent reads AGENTS.md → understands the protocol.
6. Agent self-classifies: phase × type × complexity.
7. Agent queries registry.yaml with classifications → gets matching artifacts.
8. Agent resolves overrides: for each base artifact, check project layer, apply merge strategy.
9. Agent estimates context budget → loads artifacts proportionally (low first, high last, summarize if needed).
10. Agent executes, emitting compliance markers at L4 gates.
11. Agent verifies completion against complexity rules.
12. Agent emits final compliance marker: `[gov:<phase>:<type>:<complexity>:done]`.

---

## 11. Verification & Quality Assurance

### 11.1 Structural Validators

| Validator | Purpose |
|---|---|
| `validate-registry` | Schema validation against `registry.schema.json`. Every path exists. No orphan files. No duplicate triggers at same priority. Deprecated/retired artifacts flagged. |
| `validate-cascade` | Simulates all trigger combinations. Ensures every *valid* combination resolves to ≥ L1. Warns on unmarked combinations. Errors if mandatory layers have no fallback. |
| `validate-headers` | Every `.agents/` file has required frontmatter fields. Context costs are valid. Statuses are valid. |
| `validate-deps` | No circular `depends_on`. All dependencies exist and are `active`. |
| `validate-overrides` | Project overrides only target `overridable: true` base artifacts. Merge strategies are valid. |

### 11.2 Behavioral Tests

Test scenarios in `scripts/tests/scenarios.yaml`:

```yaml
- name: "Plan a complex feature"
  triggers: { phase: plan, type: feature, complexity: complex }
  expected_artifacts:
    - base/capabilities/workflows/planning/feature-planning.md
    - base/capabilities/skills/feature-development.md
    - base/orchestration/gates.yaml
  expected_gates: [plan-required, review-required]

- name: "Fix a trivial bug"
  triggers: { phase: implement, type: bugfix, complexity: trivial }
  expected_artifacts:
    - base/conventions/
    - base/capabilities/workflows/implementation/
    - base/capabilities/skills/bug-resolution.md
  expected_gates: []
```

`run-compliance-tests` validates these scenarios against the registry. CI runs this on every change.

### 11.3 Self-Consistency Rules
- No two `active` artifacts match the same trigger combination with equal priority.
- Every persona tree resolves to exactly one default at L1.
- `depends_on` chains are acyclic.
- Mandatory layers (L1-L4) must have at least one artifact for every valid trigger combination.
- Project overrides must not target `overridable: false` base artifacts.

---

## 12. Extensibility

### Adding a new dimension value (e.g., new phase `monitor`)
1. Create artifact files under the appropriate directory.
2. Add entries to `registry.yaml`.
3. Add the layer entry to `registry.yaml` `layers` if it's a new layer.
4. Add a line to the cascade reference in AGENTS.md (only if it maps to a cascade layer).
5. Add test scenarios for the new trigger combinations.
6. Run validators.

### Adding a new layer (e.g., `L6: team`)
1. Add layer definition to `registry.yaml` `layers`.
2. Add artifact files and registry entries.
3. Update the active profile if this layer should be active by default.
4. Run validators.

---

## 13. Adoption Model

### 13.1 Incremental Adoption

| Step | Action | What changes |
|---|---|---|
| 1 | Copy `base/conventions/` into project | Code standards are now governed |
| 2 | Set profile to `minimal` | Conventions load automatically |
| 3 | Add project-specific conventions | Overrides extend base |
| 4 | Set profile to `standard` | Workflows + skills activate |
| 5 | Add project context to `project/context/` | Agent gains domain knowledge |
| 6 | Set profile to `full` | Orchestration gates activate |
| 7 | Wire CI compliance check | Automated verification |

### 13.2 Migration Between Versions

The governance framework itself is versioned in `registry.yaml`:

```yaml
framework_version: 2.0.0
```

When a project upgrades:
1. Diff `base/` between versions.
2. Check `deprecated` and `retired` statuses in old artifacts.
3. Update project overrides if base artifacts changed merge strategies.
4. Run validators to confirm compatibility.

---

## 14. Out of Scope

- Runtime agent execution engine. This framework is instructions, not an agent runtime.
- IDE/editor-specific integrations. The framework is platform-agnostic.
- Project-specific content for domains other than this workspace.
- Automated CI pipeline construction. The framework defines *what* to check; teams build *how*.
- Formal verification of agent behavior. Compliance markers are self-reported; trust but verify.

---

## 15. Success Criteria

1. An agent reading `bootstrap.md` can discover and load the entire governance system without external guidance.
2. An agent can self-classify any task and resolve the correct artifact set from the registry.
3. All validators pass against the initial artifact set.
4. All behavioral test scenarios resolve correctly.
5. The `base/` directory is self-contained — copy to another project, set profile, and governance activates.
6. Adding a new artifact requires changes in exactly 2 places: the file itself + `registry.yaml`.
7. The system degrades gracefully — no missing file or corrupt artifact blocks an agent.
8. Every governance action produces a compliance marker.
