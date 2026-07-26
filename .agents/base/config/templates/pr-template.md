---
role: config
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 30
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Pull Request Template

Use this template for all pull requests. Remove sections that don't apply.

---

## Description

What does this PR do? Why is it needed? Provide enough context for a reviewer who hasn't been following the issue.

## Type of Change

- [ ] Feature (new functionality)
- [ ] Bug fix (incorrect behavior)
- [ ] Refactor (structural change, no behavior change)
- [ ] Documentation
- [ ] Infrastructure / Ops
- [ ] Other: [describe]

## Complexity

- [ ] Trivial — single file, <20 lines, no design decisions
- [ ] Standard — few files, bounded scope
- [ ] Complex — multi-file, architectural impact
- [ ] Critical — data integrity, security, production risk

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All existing tests pass (evidence: test output below or CI link)

## Governance Compliance

- Task classified: [phase] × [type] × [complexity]
- Compliance markers:
  - `[gov:<phase>:<type>:<complexity>:L1:classified]`
  - `[gov:<phase>:<type>:<complexity>:L4:gate-*]` (as applicable)

## Checklist

- [ ] Code follows project conventions
- [ ] No dead code or commented-out blocks
- [ ] Error cases handled
- [ ] Public API documented
- [ ] No unnecessary dependencies added
- [ ] PR is focused (consider splitting if >500 lines)

## Related Issues

Closes #[issue]
Related to #[issue]

## Screenshots / Evidence

[If UI change: before/after screenshots]
[If test results: paste output]
