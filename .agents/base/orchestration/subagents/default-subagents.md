---
role: orchestration
triggers: { phase: "*", type: "*", complexity: [standard, complex, critical], valid: true }
layer: complexity
priority: 42
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Default Subagent Delegation Rules

## Principle

Delegate bounded, independent work. Don't delegate work that requires tight integration with the orchestrator's context. A subagent should receive everything it needs to complete the task in one message and return a complete result.

## When to Delegate

- **Clear inputs and outputs.** The sub-task has a well-defined scope, explicit deliverables, and unambiguous completion criteria.
- **Independence.** The work doesn't require sequential handoffs or decisions that depend on the orchestrator's judgment.
- **Right-sized.** The scope fits within a subagent's context window. Not too trivial (overhead > benefit), not too large (exceeds context).
- **Parallelizable.** Multiple sub-tasks can run concurrently without shared state or sequencing dependencies.

## When NOT to Delegate

- **Sequential dependencies.** Sub-task B needs the output of sub-task A. The orchestrator must coordinate.
- **Orchestrator judgment.** The sub-task requires decisions that depend on the orchestrator's broader understanding of the project.
- **Trivial.** The overhead of delegating (preparing context, waiting, reviewing) exceeds the benefit of doing it yourself.
- **Shared state.** The sub-task needs access to state that changes during other concurrent work.

## Subagent Types

### Planner
- **Triggers:** `phase=plan`
- **Scope:** Understand requirements, explore codebase context, produce designs and plans.
- **Deliverable:** Design document and/or implementation plan.
- **Constraint:** Produces documents, not code. Can read any file in the project.

### Implementer
- **Triggers:** `phase=implement`
- **Scope:** Execute a well-defined implementation task with TDD.
- **Deliverable:** Working, tested code committed to the branch.
- **Constraint:** Must have a clear task specification. Cannot make architectural decisions. Cannot change governance files.

### Reviewer
- **Triggers:** `phase=review`
- **Scope:** Review code or design against conventions, requirements, and best practices.
- **Deliverable:** Review feedback with severity classification (must-fix, should-fix, nit, question).
- **Constraint:** Read-only. Does not modify code. Does not approve its own work.

### Researcher
- **Triggers:** `type=research`
- **Scope:** Investigate a technical question. Find authoritative sources. Synthesize findings.
- **Deliverable:** Research findings with sources, confidence levels, and recommendations.
- **Constraint:** Read-only. Produces documents, not code. Does not implement findings.

## Delegation Protocol

1. Orchestrator identifies a delegable sub-task and selects the appropriate subagent type.
2. Orchestrator prepares the context: task description, file paths, constraints, expected output format.
3. Orchestrator dispatches the subagent with the prepared context.
4. Subagent works independently and returns a single result message.
5. Orchestrator reviews the result: does it meet the spec? Is anything missing?
6. Orchestrator integrates the result into the main workflow.

## Parallel Delegation

- Independent sub-tasks should be dispatched concurrently.
- Maximum concurrency depends on the platform but typically 3-5 agents is practical.
- No sub-task should depend on another sub-task's output. If there's a dependency, serialize them.
- Orchestrator should integrate results as they arrive. Don't block on all parallel tasks before making progress.
