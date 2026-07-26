---
role: config
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: project
priority: 52
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Project Configuration

Add project-specific tool configurations, environment settings, and templates here. These extend or override base config in `.agents/base/config/`.

## What to Add

- **Tool versions:** Required language versions (Node 20+, Python 3.12+, etc.).
- **Environment setup:** `.env` template, required services (database, cache, queue), startup commands.
- **Build configuration:** Build commands, output directories, asset compilation.
- **Deployment configuration:** Environment-specific settings, platform details.
- **Project-specific templates:** Component boilerplate, module scaffolds, test templates.

## Format

- Follow the same frontmatter conventions as base config files.
- Templates should be self-contained documents that can be copied and filled in.
- Tool configs should specify concrete commands, not just principles.
