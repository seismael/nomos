---
role: capability
mode: workflow
triggers: { phase: plan, type: docs, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Documentation Planning Workflow

Applied when `phase=plan, type=docs`. This workflow guides documentation changes — creating, updating, or removing project documentation.

## Process

### Step 1: Identify Need

Define the documentation gap:
- What documentation is missing, outdated, or unclear?
- Who is the audience? Developer (API docs, architecture), User (guides, README), Operations (runbooks, deployment docs)?
- What problem is the reader trying to solve? Frame from their perspective.
- Is this a new document, an update to existing, or a removal of obsolete content?

### Step 2: Scope Change

Determine the extent:
- What files will be created, modified, or deleted?
- Are there related docs that also need updating for consistency?
- Is this a standalone change or part of a larger feature/doc effort?

### Step 3: Check Conventions

Review relevant documentation conventions:
- Follow docstring standards for the project's language.
- Use the ADR template for architectural decisions.
- Follow README conventions for project-level docs.
- Check the documentation conventions in `base/conventions/documentation.md`.

### Step 4: Plan Content

Outline the document structure:
- What sections should the document have?
- What code examples are needed? Will they stay current?
- What cross-references to other docs? Keep links bidirectional.
- What's the maintenance plan? Who updates this if the code changes?

### Step 5: Handoff

Transition to implementation. Include:
- Document outline.
- File paths to create/modify/delete.
- Audience and purpose statement.
- Conventions reference.
