---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: project
priority: 50
status: active
context_cost: low
overridable: true
override_strategy: replace
version: "1.0.0"
---

# Project Context

Add project-specific domain knowledge here. Files in this directory are loaded at L5 (after all base artifacts) and can override or extend base conventions per the override contract.

## What to Add

- **Domain glossary:** Business-specific terms and their meanings. Maintain ubiquitous language.
- **Architecture overview:** High-level description of this project's system design. What are the bounded contexts?
- **Key decisions:** Project-specific ADRs that differ from or extend base conventions.
- **Integration points:** External systems this project depends on or serves.
- **Team conventions:** Team-specific workflows, communication norms, or ownership boundaries.

## Format

- One concept per file. Don't create monolithic "project context" documents.
- Use YAML frontmatter following the standard schema.
- Files override base artifacts with the same relative path (project/context/ overrides base/context/ where applicable).
- Set `overridable: false` on base artifacts you do NOT want project files to override.
