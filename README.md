# Nomos

**Self-governing instruction layer for AI coding agents.**

Nomos classifies every agent task by phase × type × complexity, then routes the agent to the right workflows, skills, conventions, and governance gates. It's not a runtime — it's a set of files an agent reads when it enters your project. The agent self-governs by following the protocol.

## Architecture

```
bootstrap.md → registry.yaml → profile → AGENTS.md cascade → artifacts
```

1. Agent reads `.agents/bootstrap.md` — discovers the system
2. Loads `.agents/registry.yaml` — resolves the active profile and artifact index
3. Reads `AGENTS.md` — understands the taxonomy and cascade protocol
4. **Classifies** its task (phase × type × complexity)
5. **Resolves** matching artifacts from the registry
6. **Executes** following the prescribed workflows, skills, and conventions
7. **Emits** `[gov:...]` compliance markers at governance gates

## Task Classification

Every task is classified along three dimensions:

| Dimension | Values |
|---|---|
| **Phase** | `plan`, `design`, `implement`, `test`, `review`, `deploy` |
| **Type** | `feature`, `bugfix`, `refactor`, `architecture`, `research`, `docs`, `ops` |
| **Complexity** | `trivial`, `standard`, `complex`, `critical` |

Example: fixing a typo is `implement × bugfix × trivial`. Designing a new payment system is `plan × feature × complex`.

## Governance Profiles

| Profile | Layers | Use Case |
|---|---|---|
| **minimal** | L1 only | Side projects — conventions only |
| **standard** | L1-L3, L5 | Most projects — conventions + workflows + skills |
| **full** | L1-L5 | Mature projects — full orchestration with governance gates |

## Quick Start

### Adopt Nomos in your project

```bash
# Copy the reusable core into your project
cp -r .agents/base .agents/profiles .agents/schema .agents/registry.yaml your-project/.agents/
cp AGENTS.md .agents/bootstrap.md your-project/

# Set your preferred profile in registry.yaml (default: full)
# Edit .agents/registry.yaml → active_profile: standard

# Add project-specific context
echo "## My Project" > your-project/.agents/project/context/overview.md

# Done. Agents will now self-govern when entering your project.
```

### Run validators

```bash
pip install pyyaml jsonschema
python scripts/validate-registry.py
python scripts/validate-cascade.py
python scripts/validate-headers.py
python scripts/validate-deps.py
python scripts/validate-overrides.py
python scripts/run-compliance-tests.py
```

## Structure

```
your-project/
├── AGENTS.md                       # Protocol + taxonomy
└── .agents/
    ├── bootstrap.md                # Single entry point
    ├── registry.yaml               # Artifact index (SSOT)
    ├── base/                       # Reusable core
    │   ├── conventions/            # Code standards (6 files)
    │   ├── capabilities/           # Workflows, skills, personas (29 files)
    │   ├── config/                 # Tool defaults, templates (4 files)
    │   └── orchestration/          # Gates, approvals, subagents (3 files)
    ├── project/                    # Your project overrides
    ├── profiles/                   # minimal / standard / full
    └── schema/                     # JSON Schema for registry
```

## Governance Gates

| Complexity | Gates |
|---|---|
| trivial | None |
| standard | Verify after completion |
| complex | Plan approved → Design approved → Review approved |
| critical | Plan → Design → Review → Test → Deploy review |

## Compliance

Agents emit structured markers at each gate:

```
[gov:plan:feature:complex:L4:gate-approved]
[gov:implement:bugfix:standard:L4:gate-skipped]
[gov:test:feature:trivial:done]
```

CI pipelines can grep for `[gov:.*]` markers to verify governance compliance.

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Nomos follows its own governance. Adding an artifact = creating the file + adding a registry entry. Run all validators before submitting a PR.
