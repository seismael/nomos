---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: project
priority: 51
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Project Conventions

Add stack-specific and project-specific conventions here. These extend or override the base conventions in `.agents/base/conventions/`.

## What to Add

- **Language-specific rules:** TypeScript strict mode rules, Python type hinting standards, Go error handling patterns, etc.
- **Framework conventions:** React component patterns, Django app structure, Spring Boot conventions, etc.
- **Project patterns:** Recurring patterns specific to this codebase that developers should follow.
- **Tool configuration:** Linter rules, formatter settings, test runner configuration.

## Override Strategy

By default, base conventions have `override_strategy: extend` — project files append to base content.

To fully replace a base convention:
1. Create a file in this directory with the same name as the base convention.
2. Set `override_strategy: replace` in its frontmatter.
3. The agent will use only your file, not the base version.

To prevent a specific base convention from being overridden, set `overridable: false` in the base file.
