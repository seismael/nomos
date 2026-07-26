---
role: orchestration
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: project
priority: 53
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Project Orchestration

Add project-specific orchestration rules here. These extend or override base orchestration in `.agents/base/orchestration/`.

## What to Add

- **Custom subagent definitions:** Project-specific subagent types and their scopes, triggers, and constraints.
- **Team-specific gates:** Additional approval requirements beyond the base governance gates.
- **Custom approval flows:** Who approves what? What's the escalation path?
- **CI/CD integration:** How governance markers are validated in CI. What checks run.
- **Notification rules:** Who to notify for different event types (deployments, incidents, reviews).

## Example: Adding a Custom Gate

To add a security review gate for critical features:

1. Create a file here (e.g., `security-review.md`).
2. Define the gate checkpoint: when it triggers, who approves, what's required.
3. Reference it in project-specific workflows or in an override of `gates.yaml`.

## Format

- Follow the same frontmatter conventions as base orchestration files.
- Gates should follow the `gates.yaml` schema (id, phase, description, marker, approval, required).
- Approval flows should specify concrete people/roles, not abstract "reviewer."
