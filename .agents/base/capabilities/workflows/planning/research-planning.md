---
role: capability
mode: workflow
triggers: { phase: plan, type: research, complexity: "*", valid: true }
layer: phase
priority: 10
status: active
context_cost: medium
depends_on: ["base/capabilities/personas/default.md"]
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Research Planning Workflow

Applied when `phase=plan, type=research`. This workflow guides information-gathering tasks where the agent must find, evaluate, and synthesize external knowledge.

## Process

### Step 1: Define Question

Frame the research precisely:
- What exactly do you need to know? State the question(s) unambiguously.
- What constitutes a sufficient answer? Define scope boundaries.
- What is the context? Version numbers, environment, constraints.
- Is this a known-unknown (you know what you don't know) or an unknown-unknown (exploratory)?

### Step 2: Identify Sources

Prioritize sources by authority (highest to lowest):
1. **Official documentation** — the library/framework's own docs, API references, changelogs.
2. **Library source code** — the authoritative truth when docs are unclear.
3. **Real-world examples** — open-source projects on GitHub using the library in production.
4. **Technical blog posts** — by recognized experts or the library maintainers themselves.
5. **Stack Overflow** — highly-upvoted, recent answers. Reject anything >2 years old for fast-moving ecosystems.
6. **AI-generated content** — treat as unverified suggestion, not fact. Always cross-reference.

### Step 3: Execute Research

Search systematically across sources:
- Start with official docs. If found and clear, stop — this is the best answer.
- If docs are unclear, go to source code for authoritative behavior.
- If source code is unavailable, expand to examples and community sources.
- Capture: URLs, version numbers, publication dates, relevant excerpts.
- Note contradictions between sources. Don't silently pick a side.

### Step 4: Synthesize Findings

Consolidate into a coherent answer:
- Summarize the key findings.
- Note any contradictions and explain resolution.
- Assign confidence levels:
  - **Confirmed:** Verified against official docs or source code.
  - **Probable:** Consistent across multiple independent, recent sources.
  - **Speculative:** Single source, old information, or AI-generated only.

### Step 5: Deliver

Output format:
1. **Summary:** One-paragraph answer to the research question.
2. **Detailed findings:** Per-source breakdown with confidence levels.
3. **Source citations:** URLs with retrieval dates. Version numbers where applicable.
4. **Open questions:** What remains unknown or uncertain.
5. **Recommendations:** If the research was to inform a decision, state the recommendation.
