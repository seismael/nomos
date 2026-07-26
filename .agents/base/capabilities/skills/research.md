---
role: capability
mode: skill
triggers: { phase: "*", type: research, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Research

Reference material for agents working on research-type tasks. Covers how to find, evaluate, and synthesize information.

## Source Hierarchy (most to least authoritative)

1. **Official documentation** — Library/framework docs, API references, changelogs. The canonical source.
2. **Source code** — When docs are unclear or incomplete, the source is authoritative. Read it.
3. **Real-world examples** — Open-source projects on GitHub using the library in production. Shows patterns, not just APIs.
4. **Technical blog posts** — By recognized experts or library maintainers. Check the date — is it current?
5. **Stack Overflow** — Highly-upvoted, recent answers. Reject anything >2 years old for fast-moving ecosystems.
6. **AI-generated content** — Treat as unverified suggestion. Always cross-reference against higher-tier sources.

## Research Methodology

1. **Define the question precisely.** "How do I X?" is not precise. "How do I configure library Y v3.2 to handle Z with W constraints?" is.
2. **Search systematically.** Start at tier 1. If found and clear, stop. If unclear, work down the hierarchy.
3. **Capture sources.** URL, version number, publication date, relevant excerpt. You'll need these for the output.
4. **Cross-reference.** One source can be wrong or outdated. Two independent sources saying the same thing is stronger.
5. **Note contradictions.** Don't silently pick a side. Flag the contradiction and explain your resolution.
6. **Verify with code.** If possible, write a minimal test to confirm the behavior. A 10-line script beats 3 Stack Overflow answers.

## Output Format

For each finding, provide:
1. **Summary:** One paragraph answering the research question.
2. **Detailed findings:** Per-source breakdown.
3. **Confidence level:**
   - **Confirmed:** Verified against official docs or source code.
   - **Probable:** Consistent across multiple independent, recent sources.
   - **Speculative:** Single source, old information, or AI-generated only.
4. **Source citations:** URLs with retrieval dates. Version numbers where applicable.
5. **Open questions:** What remains unknown or uncertain.

## Quality Checks

- Was the information published recently? Does it apply to the version you're using?
- Is it consistent across multiple independent sources?
- Is the source authoritative for this specific domain?
- Could you write a minimal test to verify the claim?

## When to Research vs Experiment

- **Research** for: API behavior, configuration options, best practices, known limitations, compatibility.
- **Experiment** for: performance questions, integration behavior, edge cases in your specific context.
- **Both** for: "is this approach viable?" — research alternatives, then prototype the best candidate.
