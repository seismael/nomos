# ADR-005: Governance Profiles

**Date:** 2026-07-25
**Status:** Accepted

## Context

Not every project needs full governance. A small side project may only need baseline conventions. A mature production system needs full orchestration with governance gates. The initial design conflated task complexity (how much ceremony per task) with governance depth (how many artifact categories are active).

We needed a mechanism to:
1. Let projects choose their governance depth independent of task complexity.
2. Support incremental adoption: start minimal, add complexity as the project matures.
3. Not force teams to configure every layer and category individually.

## Decision

Introduce governance profiles: predefined bundles that control which layers and artifact categories are active.

```yaml
# profiles/minimal.yaml
name: minimal
active_layers: [L1]
active_categories: [conventions]
```

Three profiles are defined:

| Profile | Layers | Categories | Use Case |
|---|---|---|---|
| **minimal** | L1 only | conventions | Side projects, proof-of-concepts, quick scripts |
| **standard** | L1, L2, L3, L5 | conventions, capabilities, config | Most production projects — conventions, workflows, skills, project context |
| **full** | L1-L5 | all | Mature projects with high reliability requirements and formal governance |

The active profile is declared in `registry.yaml`:

```yaml
active_profile: full
```

## Consequences

### Positive
- **Simple adoption:** Choose a profile. Done. No per-layer configuration needed.
- **Incremental path:** Start with `minimal`. When the project matures, switch to `standard`. When it needs formal gates, switch to `full`.
- **Separation of concerns:** Task complexity (how much ceremony) is separate from profile (which categories load). A complex task under `standard` profile still gets workflows and skills, just no orchestration gates.
- **Custom profiles:** Teams can create additional profiles by copying and modifying the existing ones.

### Negative
- **Limited to 3 out-of-the-box:** Teams with unusual needs must create custom profiles. The 3-profile model covers most use cases but not all.
- **Profile is checked at bootstrap time:** Changing the profile mid-session has undefined behavior. The agent loads the profile once at bootstrap.

### Neutral
- The profile system is independent of the complexity gates system. A task can be `critical` complexity under `minimal` profile — it gets the same minimal artifacts but still requires critical-level gates (if gates are active, which they aren't under `minimal`).

## Alternatives Considered

### Alternative 1: Use complexity as the sole depth control
Use `trivial` tasks for minimal governance, `critical` for full governance. Rejected because it conflates task risk with governance depth. A `trivial` task in a `full` profile project should still get baseline conventions, and a `critical` task in a `minimal` profile project should still get the minimal artifacts.

### Alternative 2: Per-category toggles
Let teams toggle each artifact category individually (conventions: on, workflows: off, skills: on, etc.). Rejected because it's too fine-grained. Most teams don't need this level of control, and the configuration surface is too large.

### Alternative 3: No profiles, always full governance
Simplest approach. Rejected because it creates adoption friction. A team writing a 50-line script shouldn't need to configure orchestration gates.

### Alternative 4: Auto-detect profile from project characteristics
Infer profile from repo size, team size, or existing config. Rejected as magical and unpredictable. Explicit profiles are deliberate and understandable.
