# Agent Governance Framework — Implementation Plan

> **For implementers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete agent governance framework — bootstrap, registry, AGENTS.md, all 4 artifact categories, profiles, orchestration gates, validators, and compliance tests.

**Architecture:** Layered dispatch. `bootstrap.md` → `registry.yaml` → profile → `AGENTS.md` cascade → artifacts. Four consolidated types: capabilities, conventions, config, orchestration.

**Tech Stack:** YAML, Markdown, JSON Schema, Python (validators).

**Source spec:** `docs/superpowers/specs/2026-07-25-nomos-design.md`

---

## File Map

See the spec Section 2.1 for the full directory tree. This plan creates ~60 files across:

- **Foundation (4):** `bootstrap.md`, `registry.yaml`, `AGENTS.md`, `registry.schema.json`
- **Profiles (3):** `profiles/minimal.yaml`, `standard.yaml`, `full.yaml`
- **Conventions (6):** general, naming, structure, testing, documentation, error-handling
- **Personas (4):** default, architect, reviewer, implementer
- **Workflows (18):** 7 planning + 2 design + 4 implementation + 2 testing + 2 review + 1 deploy
- **Skills (7):** feature, bugfix, refactor, architecture, research, docs, ops
- **Config (4):** default-tools, design-doc-template, adr-template, pr-template
- **Orchestration (3):** gates.yaml, approval-flows.md, default-subagents.md
- **Project (4):** context/README.md + conventions/README.md + config/README.md + orchestration/README.md
- **Verification (6):** 4 validators + scenarios.yaml + compliance test runner
- **ADR docs (5):** 5 architecture decision records

---

## Phase 1: Foundation

### Task 1: Directory Structure + Schema + Registry

**Files:**
- Create: `.agents/schema/registry.schema.json`
- Create: `.agents/registry.yaml`

**Steps:**

- [ ] **Step 1: Create all directories**

Run:
```powershell
$dirs = @(
    '.agents/base/capabilities/workflows/planning',
    '.agents/base/capabilities/workflows/design',
    '.agents/base/capabilities/workflows/implementation',
    '.agents/base/capabilities/workflows/testing',
    '.agents/base/capabilities/workflows/review',
    '.agents/base/capabilities/workflows/deploy',
    '.agents/base/capabilities/skills',
    '.agents/base/capabilities/personas',
    '.agents/base/conventions',
    '.agents/base/config/tools',
    '.agents/base/config/templates',
    '.agents/base/orchestration/subagents',
    '.agents/project/context',
    '.agents/project/conventions',
    '.agents/project/config',
    '.agents/project/orchestration',
    '.agents/profiles',
    '.agents/schema',
    'scripts/tests',
    'docs/adr'
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Path $d -Force }
```

- [ ] **Step 2: Create registry.schema.json**

Write the JSON Schema from the spec Section 11.1 — validates `version`, `framework_version`, `active_profile`, `layers[]`, `artifacts[]` with all required fields and enums.

- [ ] **Step 3: Create registry.yaml**

Write the complete registry manifest from the spec Section 4.3 — all layers (L1–L5), all ~55 artifact entries with path, role, mode, triggers, layer, priority, status, context_cost, and optional fields.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: add directory structure, schema, and registry manifest"
```

---

### Task 2: Bootstrap + AGENTS.md

**Files:**
- Create: `.agents/bootstrap.md`
- Create: `AGENTS.md`

**Steps:**

- [ ] **Step 1: Create bootstrap.md**

Write the bootstrap entry point as specified in the spec Section 3.1 — single file that tells the agent: load registry → load profile → follow AGENTS.md protocol → fallback rules → compliance markers. Include the fallback chain for missing artifacts.

- [ ] **Step 2: Create AGENTS.md**

Write the central conductor as specified in the spec Section 4 — protocol declaration, taxonomy (phase/type/complexity), cascade reference, override resolution rules, governance gates summary, compliance checklist.

- [ ] **Step 3: Commit**

```bash
git add .agents/bootstrap.md AGENTS.md
git commit -m "feat: add bootstrap entry point and AGENTS.md protocol"
```

---

## Phase 2: Profiles

### Task 3: Governance Profiles

**Files:**
- Create: `.agents/profiles/minimal.yaml`
- Create: `.agents/profiles/standard.yaml`
- Create: `.agents/profiles/full.yaml`

**Steps:**

- [ ] **Step 1: Create minimal profile**

```yaml
name: minimal
description: "Baseline conventions only. No workflows, skills, or gates."
active_layers: [L1]
active_categories: [conventions]
```

- [ ] **Step 2: Create standard profile**

```yaml
name: standard
description: "Conventions + phase workflows + type skills + project context."
active_layers: [L1, L2, L3, L5]
active_categories: [capabilities, conventions, config]
```

- [ ] **Step 3: Create full profile**

```yaml
name: full
description: "All layers, all categories, full orchestration with governance gates."
active_layers: [L1, L2, L3, L4, L5]
active_categories: [capabilities, conventions, config, orchestration]
```

- [ ] **Step 4: Commit**

```bash
git add .agents/profiles/
git commit -m "feat: add governance profiles (minimal, standard, full)"
```

---

## Phase 3: Conventions (L1)

### Task 4: General, Naming, Structure Conventions

**Files:**
- Create: `.agents/base/conventions/general.md`
- Create: `.agents/base/conventions/naming.md`
- Create: `.agents/base/conventions/structure.md`

**Steps:**

- [ ] **Step 1: Write general.md** — Cover: surgical precision, YAGNI, DRY, readability, defensive minimalism, composition over inheritance, consistency. Include YAML frontmatter: `role: convention, layer: L1, priority: 1, context_cost: low, overridable: true, override_strategy: extend`.

- [ ] **Step 2: Write naming.md** — Cover: descriptive names, no abbreviations, verb-phrase functions, noun classes, domain language, file naming conventions. Frontmatter: priority 2.

- [ ] **Step 3: Write structure.md** — Cover: domain-based organization, file size limits (200 target, 300 soft, 500 hard), module boundaries (DAG, no circular imports), test colocation, entry points. Frontmatter: priority 3.

- [ ] **Step 4: Commit**

---

### Task 5: Testing, Documentation, Error-Handling Conventions

**Files:**
- Create: `.agents/base/conventions/testing.md`
- Create: `.agents/base/conventions/documentation.md`
- Create: `.agents/base/conventions/error-handling.md`

**Steps:**

- [ ] **Step 1: Write testing.md** — Cover: TDD as default, red-green-refactor, unit/integration/e2e pyramid, behavior over implementation, AAA pattern, test data isolation, coverage philosophy. Priority 4.

- [ ] **Step 2: Write documentation.md** — Cover: doc why not what, public API docs, ADR format, no obvious-code comments, no commented-out code, HACK/TODO markup. Priority 5.

- [ ] **Step 3: Write error-handling.md** — Cover: recoverable/non-recoverable/fatal classification, catch at boundaries, no swallowing, add context, fail fast, no naked exceptions, logging levels, retry with exponential backoff. Priority 6.

- [ ] **Step 4: Commit**

---

## Phase 4: Personas (L1 default + L3 specialized)

### Task 6: Default + Architect + Reviewer Personas

**Files:**
- Create: `.agents/base/capabilities/personas/default.md`
- Create: `.agents/base/capabilities/personas/architect.md`
- Create: `.agents/base/capabilities/personas/reviewer.md`

**Steps:**

- [ ] **Step 1: Write default.md** — Cover: core behaviors (precision, discipline, honesty, verification), authority boundaries, communication style, compliance obligations. Frontmatter: `mode: persona, layer: L1, priority: 10, overridable: true, override_strategy: replace`.

- [ ] **Step 2: Write architect.md** — Cover: trade-off thinking, questioning assumptions, design for change, SOLID, DDD, separation of concerns, ADR process, anti-patterns to avoid. Depends on default. Priority 15.

- [ ] **Step 3: Write reviewer.md** — Cover: 7 review focus areas (correctness, design, conventions, testing, security, performance, readability), review process, feedback style, approval criteria. Depends on default. Priority 15.

- [ ] **Step 4: Commit**

---

### Task 7: Implementer Persona

**Files:**
- Create: `.agents/base/capabilities/personas/implementer.md`

- [ ] **Step 1: Write implementer.md** — Cover: follow the plan, TDD by default, small commits, incremental progress, implementation process (6 steps), code quality checklist, when to escalate. Depends on default. Priority 15.

- [ ] **Step 2: Commit**

---

## Phase 5: Workflows (L2)

### Task 8: Planning Workflows — Feature, Bugfix, Refactor

**Files:**
- Create: `.agents/base/capabilities/workflows/planning/feature-planning.md`
- Create: `.agents/base/capabilities/workflows/planning/bugfix-planning.md`
- Create: `.agents/base/capabilities/workflows/planning/refactor-planning.md`

**Steps:**

- [ ] **Step 1: Write feature-planning.md** — Define 7-step workflow: understand → explore context → design → produce artifacts (design doc, ADR, plan) → validate → gate check → handoff. Frontmatter: triggers `{phase: plan, type: feature, complexity: [standard, complex, critical], valid: true}`.

- [ ] **Step 2: Write bugfix-planning.md** — Define 6-step workflow: reproduce → diagnose root cause → scope fix → plan → gate check → handoff.

- [ ] **Step 3: Write refactor-planning.md** — Define 7-step workflow: define goal → establish safety net → analyze current → design target → plan incremental steps → gate check → handoff.

- [ ] **Step 4: Commit**

---

### Task 9: Planning Workflows — Architecture, Research, Docs, Ops

**Files:**
- Create: `.agents/base/capabilities/workflows/planning/architecture-planning.md`
- Create: `.agents/base/capabilities/workflows/planning/research-planning.md`
- Create: `.agents/base/capabilities/workflows/planning/docs-planning.md`
- Create: `.agents/base/capabilities/workflows/planning/ops-planning.md`

**Steps:**

- [ ] **Step 1: Write architecture-planning.md** — 8-step workflow: frame decision → gather context → generate alternatives → evaluate trade-offs (6 dimensions) → decide → document ADR → validate → handoff.

- [ ] **Step 2: Write research-planning.md** — 5-step workflow: define question → identify sources → execute research → synthesize findings → deliver with source citations.

- [ ] **Step 3: Write docs-planning.md** — 5-step workflow: identify need → scope change → check conventions → plan content → handoff.

- [ ] **Step 4: Write ops-planning.md** — 6-step workflow: understand change → assess impact → plan (with rollback) → test plan → gate check → handoff.

- [ ] **Step 5: Commit**

---

### Task 10: Design Workflows

**Files:**
- Create: `.agents/base/capabilities/workflows/design/feature-design.md`
- Create: `.agents/base/capabilities/workflows/design/architecture-design.md`

**Steps:**

- [ ] **Step 1: Write feature-design.md** — 8-step workflow: review plan → detail components → design data flow → specify interfaces → review design → produce artifacts → gate check → handoff.

- [ ] **Step 2: Write architecture-design.md** — 8-step workflow: review ADR → define system boundaries → detail subsystems → specify cross-cutting concerns → validate → produce artifacts → gate check → handoff.

- [ ] **Step 3: Commit**

---

### Task 11: Implementation Workflows

**Files:**
- Create: `.agents/base/capabilities/workflows/implementation/feature-implementation.md`
- Create: `.agents/base/capabilities/workflows/implementation/bugfix-implementation.md`
- Create: `.agents/base/capabilities/workflows/implementation/refactor-implementation.md`
- Create: `.agents/base/capabilities/workflows/implementation/ops-implementation.md`

**Steps:**

- [ ] **Step 1: Write feature-implementation.md** — 8-step TDD workflow: load context → verify preconditions → implement incrementally (test → fail → code → pass → refactor → commit) → integration verify → code quality check → prepare review → gate → handoff.

- [ ] **Step 2: Write bugfix-implementation.md** — 7-step workflow: load context → write regression test → implement fix → verify → prepare review → gate → handoff.

- [ ] **Step 3: Write refactor-implementation.md** — 7-step workflow: load context → establish baseline → execute incrementally → verify no behavioral change → cleanup → gate → handoff.

- [ ] **Step 4: Write ops-implementation.md** — 7-step workflow: load context → pre-flight checks → execute change → verify → document → gate → handoff.

- [ ] **Step 5: Commit**

---

### Task 12: Testing, Review, Deploy Workflows

**Files:**
- Create: `.agents/base/capabilities/workflows/testing/feature-testing.md`
- Create: `.agents/base/capabilities/workflows/testing/bugfix-testing.md`
- Create: `.agents/base/capabilities/workflows/review/code-review.md`
- Create: `.agents/base/capabilities/workflows/review/architecture-review.md`
- Create: `.agents/base/capabilities/workflows/deploy/deployment.md`

**Steps:**

- [ ] **Step 1: Write feature-testing.md** — 8-step: review test requirements → run tests → fill coverage gaps → manual verify → performance check → acceptance criteria → gate → handoff.

- [ ] **Step 2: Write bugfix-testing.md** — 5-step: verify fix → run full suite → check related functionality → gate → handoff.

- [ ] **Step 3: Write code-review.md** — 7-step: load reviewer persona → review diff (6 criteria) → run tests → provide feedback → decide (approve/changes/comment) → gate → handoff.

- [ ] **Step 4: Write architecture-review.md** — 8-step: load context → evaluate decision → evaluate design → identify risks → decide → document → gate → handoff.

- [ ] **Step 5: Write deployment.md** — 7-step: pre-deployment checklist → deploy → verify → monitor → rollback (if needed) → post-deployment → handoff.

- [ ] **Step 6: Commit**

---

## Phase 6: Skills (L3)

### Task 13: All Type Skills

**Files:** Create all 7 skill files under `.agents/base/capabilities/skills/`

- [ ] **Step 1: Write feature-development.md** — key principles, common patterns, anti-patterns, deliverables.

- [ ] **Step 2: Write bug-resolution.md** — diagnostic approach (reproduce → isolate → hypothesize → instrument → verify → fix), common bug categories, regression test requirement.

- [ ] **Step 3: Write refactoring.md** — behavior must not change, safety net first, small steps, common patterns (extract, inline, rename, replace conditional), when NOT to refactor.

- [ ] **Step 4: Write architecture.md** — design heuristics (SOLID, DDD, CQRS, event-driven, hexagonal), 8 analysis dimensions, ADR deliverables.

- [ ] **Step 5: Write research.md** — source hierarchy (official docs → source code → examples → blogs → issues → SO → AI), output format with confidence levels.

- [ ] **Step 6: Write documentation.md** — doc types (README, API, ADR, guides), explain why not what, keep current, remove before adding.

- [ ] **Step 7: Write ops.md** — IaC principle, common tasks, safety checklist (documented, rollback, tested, notified, monitored).

- [ ] **Step 8: Commit**

---

## Phase 7: Config (L1)

### Task 14: Tool Config + Templates

**Files:**
- Create: `.agents/base/config/tools/default-tools.md`
- Create: `.agents/base/config/templates/design-doc-template.md`
- Create: `.agents/base/config/templates/adr-template.md`
- Create: `.agents/base/config/templates/pr-template.md`

**Steps:**

- [ ] **Step 1: Write default-tools.md** — Cover: git conventions (commit messages, branching), linting/formatting (automated, pre-commit, CI blocking), testing frameworks (single command, CI), package management (lockfiles committed), code review (PR required, approval required).

- [ ] **Step 2: Write design-doc-template.md** — Sections: Purpose, Requirements (functional + non-functional), Design (architecture, components, data flow, interfaces, error handling), Alternatives Considered, Testing Strategy, Migration & Rollout, Open Questions.

- [ ] **Step 3: Write adr-template.md** — Sections: Context, Decision, Consequences (positive/negative/neutral), Alternatives Considered, References. Include status and supersedes/superseded-by headers.

- [ ] **Step 4: Write pr-template.md** — Sections: Description, Type of Change, Complexity, Testing, Governance Compliance (classification + markers), Checklist, Related Issues, Screenshots.

- [ ] **Step 5: Commit**

---

## Phase 8: Orchestration (L4)

### Task 15: Gates + Approval Flows + Subagents

**Files:**
- Create: `.agents/base/orchestration/gates.yaml`
- Create: `.agents/base/orchestration/approval-flows.md`
- Create: `.agents/base/orchestration/subagents/default-subagents.md`

**Steps:**

- [ ] **Step 1: Write gates.yaml** — Define 4 complexity tiers with checkpoints: trivial (no gates), standard (verify after), complex (plan approved + review approved), critical (plan → design → review → test → deploy review). Each checkpoint has id, phase, description, marker, approval type, required flag.

- [ ] **Step 2: Write approval-flows.md** — Define human approval process (agent prompt format, what to present), peer review process, architecture review process, bypass rules (never bypass, reclassify or escalate).

- [ ] **Step 3: Write default-subagents.md** — Define when to delegate / not delegate. Define 4 subagent types: Planner, Implementer, Reviewer, Researcher — each with triggers, scope, deliverable, constraints. Define delegation protocol and parallel delegation rules.

- [ ] **Step 4: Commit**

---

## Phase 9: Project Layer (L5)

### Task 16: Project Layer READMEs

**Files:**
- Create: `.agents/project/context/README.md`
- Create: `.agents/project/conventions/README.md`
- Create: `.agents/project/config/README.md`
- Create: `.agents/project/orchestration/README.md`

**Steps:**

- [ ] **Step 1: Write all 4 READMEs** — Each README explains: what this directory is for, what to add, format conventions, how overrides work. Keep each short (<500 words) with YAML frontmatter.

- [ ] **Step 2: Commit**

---

## Phase 10: Verification Scripts

### Task 17: Registry + Cascade Validators

**Files:**
- Create: `scripts/validate-registry.py`
- Create: `scripts/validate-cascade.py`

**Steps:**

- [ ] **Step 1: Write validate-registry.py**

Python script that:
- Loads `registry.yaml` via PyYAML
- Checks required top-level fields (version, active_profile, layers, artifacts)
- Validates each artifact: required fields present, enums valid, path exists on disk, no duplicate paths, no duplicate trigger+layer+priority combos
- Checks depends_on references exist
- Checks project overrides don't target non-overridable base artifacts
- Reports errors (exit 1) and warnings (exit 0)
- Use `pip install pyyaml` if not available

- [ ] **Step 2: Write validate-cascade.py**

Python script that:
- Loads `registry.yaml`
- Iterates all 168 combinations (6 phases × 7 types × 4 complexities)
- For each, checks which layers have matching artifacts
- For combinations marked `valid: true` by at least one artifact, verifies all mandatory layers resolve
- Reports gaps as errors, unmarked combinations as informational

- [ ] **Step 3: Test the validators**

Run:
```bash
python scripts/validate-registry.py
python scripts/validate-cascade.py
```

Expected: validate-registry passes (all paths exist, all fields valid). validate-cascade reports valid combinations with resolved layers, warnings for unmarked combos.

- [ ] **Step 4: Commit**

---

### Task 18: Headers + Deps Validators + Compliance Tests

**Files:**
- Create: `scripts/validate-headers.py`
- Create: `scripts/validate-deps.py`
- Create: `scripts/tests/scenarios.yaml`
- Create: `scripts/run-compliance-tests.py`

**Steps:**

- [ ] **Step 1: Write validate-headers.py**

Python script that:
- Iterates all `.md` files under `.agents/`
- Extracts YAML frontmatter (content between first `---` and second `---`)
- Validates required fields: role, triggers, layer, priority, status, context_cost
- Validates field values against enums
- Reports any file with missing/invalid frontmatter

- [ ] **Step 2: Write validate-deps.py**

Python script that:
- Loads `registry.yaml`
- Builds dependency graph from `depends_on` fields
- Detects cycles using DFS (WHITE/GRAY/BLACK coloring)
- Checks all dependency targets exist in registry
- Reports circular dependencies and missing deps

- [ ] **Step 3: Write scenarios.yaml**

```yaml
scenarios:
  - name: "Plan a complex feature"
    triggers: { phase: plan, type: feature, complexity: complex }
    expected_min_artifacts: 3
    expected_layers: [L1, L2, L3, L4]
    expected_gates: [plan-required, review-required]

  - name: "Fix a trivial bug"
    triggers: { phase: implement, type: bugfix, complexity: trivial }
    expected_min_artifacts: 2
    expected_layers: [L1, L2, L3]
    expected_gates: []

  - name: "Architecture review"
    triggers: { phase: review, type: architecture, complexity: complex }
    expected_min_artifacts: 3
    expected_layers: [L1, L2, L3]
    expected_gates: []

  - name: "Critical feature deploy"
    triggers: { phase: deploy, type: feature, complexity: critical }
    expected_min_artifacts: 2
    expected_layers: [L1, L2]
    expected_gates: [plan-required, design-required, review-required, test-required, deploy-review]

  - name: "Trivial docs update"
    triggers: { phase: implement, type: docs, complexity: trivial }
    expected_min_artifacts: 1
    expected_layers: [L1]
    expected_gates: []
```

- [ ] **Step 4: Write run-compliance-tests.py**

Python script that:
- Loads `scenarios.yaml` and `registry.yaml`
- For each scenario, resolves artifacts by matching triggers
- Verifies minimum artifact count, expected layers, expected gates
- Reports pass/fail per scenario

- [ ] **Step 5: Run all validators**

```bash
python scripts/validate-registry.py
python scripts/validate-cascade.py
python scripts/validate-headers.py
python scripts/validate-deps.py
python scripts/run-compliance-tests.py
```

Expected: all pass or report only informational warnings.

- [ ] **Step 6: Commit**

---

## Phase 11: Architecture Decision Records

### Task 19: ADR Documentation

**Files:**
- Create: `docs/adr/001-bootstrap-entry-point.md`
- Create: `docs/adr/002-consolidated-artifact-types.md`
- Create: `docs/adr/003-cascade-layer-design.md`
- Create: `docs/adr/004-context-budget-model.md`
- Create: `docs/adr/005-governance-profiles.md`

**Steps:**

- [ ] **Step 1: Write ADR-001** — Context: agents need unambiguous entry point. Decision: bootstrap.md as single file with fallback chain. Consequences: discoverable, debuggable, backward compatible.

- [ ] **Step 2: Write ADR-002** — Context: 8 artifact types create cognitive overhead. Decision: consolidate to 4 (capabilities, conventions, config, orchestration) with mode field. Consequences: simpler mental model, fewer directories, mode field adds flexibility.

- [ ] **Step 3: Write ADR-003** — Context: hardcoded 5-layer cascade limits extensibility. Decision: configurable layer stack in registry.yaml. Consequences: teams can add layers, AGENTS.md stays stable, validators adapt.

- [ ] **Step 4: Write ADR-004** — Context: loading all artifacts burns context budget. Decision: context_cost field (low/medium/high) + lazy loading + summarization fallback. Consequences: agents stay within budget, low-cost artifacts always load, high-cost on demand.

- [ ] **Step 5: Write ADR-005** — Context: not every project needs full governance. Decision: 3 profiles (minimal/standard/full) controlling active layers and categories. Consequences: incremental adoption, complexity gates separate from profile depth.

- [ ] **Step 6: Commit**

---

## Phase 12: Final Integration & Verification

### Task 20: End-to-End Validation

**Steps:**

- [ ] **Step 1: Run all validators**

```bash
python scripts/validate-registry.py
python scripts/validate-cascade.py
python scripts/validate-headers.py
python scripts/validate-deps.py
python scripts/run-compliance-tests.py
```

Fix any failures before proceeding.

- [ ] **Step 2: Manual consistency check**

- Verify every `.md` file in `.agents/` is listed in `registry.yaml` (and vice versa).
- Verify every trigger combination with `valid: true` has at least one artifact.
- Verify no project artifact overrides a base artifact with `overridable: false`.
- Verify all `depends_on` chains resolve.

- [ ] **Step 3: Bootstrap chain verification**

Walk through the agent execution flow manually:
1. Read `bootstrap.md` → loads registry → loads profile → reads AGENTS.md
2. Classify a sample task: `{phase: plan, type: feature, complexity: complex}`
3. Resolve artifacts from registry for L1-L4
4. Verify each resolved path exists

- [ ] **Step 4: Commit final state**

```bash
git add -A
git commit -m "feat: complete agent governance framework v1.0.0"
```

---

## Success Criteria Checklist

- [ ] `bootstrap.md` is the single entry point — agent can discover the entire system from it
- [ ] `registry.yaml` is the SSOT — all artifacts listed, no orphans
- [ ] AGENTS.md contains: protocol, taxonomy, cascade reference, compliance checklist
- [ ] All 4 artifact types have content: capabilities (29 files), conventions (6), config (4), orchestration (3)
- [ ] 3 profiles exist: minimal, standard, full
- [ ] All YAML frontmatter is valid and complete
- [ ] `validate-registry.py` passes (0 errors)
- [ ] `validate-cascade.py` passes (all valid combos resolve)
- [ ] `validate-headers.py` passes (all files have valid frontmatter)
- [ ] `validate-deps.py` passes (no cycles, all deps exist)
- [ ] `run-compliance-tests.py` passes (all 5 scenarios resolve correctly)
- [ ] 5 ADRs document key design decisions
- [ ] `base/` directory is self-contained — can be copied to another project
- [ ] Adding a new artifact requires changes in exactly 2 places: file + registry
