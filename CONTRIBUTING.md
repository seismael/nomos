# Contributing to Nomos

Thank you for your interest in contributing. Nomos follows its own governance protocol — this means contributions must pass the same validators and compliance checks that governed artifacts enforce on agents.

## How to Contribute

### 1. Fork and Branch

```bash
git clone https://github.com/seismael/nomos.git
cd nomos
git checkout -b feature/my-contribution
```

### 2. Make Your Change

Every change to Nomos falls into one of these categories:

| Change | What to Do |
|---|---|
| **New artifact** (workflow, skill, persona, convention) | Create the file in the correct directory. Add a registry entry. |
| **Modify existing artifact** | Edit the file. Update the registry entry if triggers/layer/priority change. |
| **New validator or tooling** | Add the script. Ensure it runs clean. |
| **Documentation / ADR** | Follow existing formats. |

### Artifact Checklist

Every new or modified artifact must:
- [ ] Have valid YAML frontmatter with `role`, `triggers`, `layer`, `priority`, `status`, `context_cost`
- [ ] Be listed in `.agents/registry.yaml` with matching frontmatter fields
- [ ] Pass `validate-registry` (paths exist, no duplicate triggers)
- [ ] Pass `validate-headers` (valid frontmatter, required fields present)
- [ ] Pass `validate-cascade` (trigger combinations still resolve correctly)
- [ ] Pass `validate-deps` (no circular `depends_on`)
- [ ] Pass `validate-overrides` (project overrides don't violate base contracts)
- [ ] Add or update a compliance test scenario if the change affects routing

### 3. Run Validators

```bash
pip install pyyaml jsonschema

python scripts/validate-registry.py
python scripts/validate-cascade.py
python scripts/validate-headers.py
python scripts/validate-deps.py
python scripts/validate-overrides.py
python scripts/run-compliance-tests.py
```

All six must pass with zero errors.

### 4. Submit a Pull Request

- Describe what you changed and why.
- Note any affected trigger combinations or compliance scenarios.
- Include the output of all validators in the PR description.
- Reference any related ADRs or issues.

## Design Principles

When contributing, follow these principles:

- **Generic by default.** Base artifacts should be language-agnostic and project-agnostic. Stack-specific rules go in project overrides.
- **Single source of truth.** The registry is authoritative. Never duplicate artifact paths or trigger information.
- **Degrade gracefully.** Missing or corrupt artifacts should not block an agent. The fallback chain must always resolve to baseline conventions.
- **Two places only.** Adding an artifact requires exactly two changes: the file + the registry entry. If your change requires more, the design may need rethinking.

## Reporting Issues

- **Bug:** A validator fails on valid input, or an artifact resolves incorrectly. Include the exact trigger combination and expected vs actual behavior.
- **Gap:** A valid trigger combination has no artifact. Include the use case.
- **Enhancement:** A new workflow, skill, or convention that would be useful generically.

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
