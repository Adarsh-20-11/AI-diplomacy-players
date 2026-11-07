---
tags: [concept, architecture]
phase: 1
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Hexagonal Architecture

## What it is (my own words)
So this is basically an architecture where you have a core logic in the center as a hexagon, which is connected to multiple external sources or targets (or both) like APIs, databases, etc. These are connected via adapters which meet the hexagon (core) at ports. So basically, they can be treated as sub systems, have anti-corruption layers between them so stuff doesn't get mixed up.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 1
- The AI port today: `needle-ai/src/needle/llmapi/base.py` (`BaseLLMClient`)

## Tradeoff / why I chose this
AI Observability, state management (persistence wise), tool calling, user interaction, my n8n-like application, context, etc all are technically external tools that are going to use the core codebase and library as a central spot. This way, I can manage all that stuff externally, have different testing architecture and all, and still keep my core as is.
Also, this helps me develop the sub systems in a different way (as required by different AI adapters) so that core handles everything in a graceful way, and inter communication inside the core becomes way easier.

## Related
- [[Anti-Corruption Layer]]
- [[Canonical Data Model]]
- [[Stateless LLM Clients]]

## Quiz myself
1. What is the difference between a driving and a driven port? Give one of each from Needle.
2. Which way must dependency arrows point, and what in `llm.py` breaks that rule today?
3. What is a composition root, and how would it fix that?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- First take: "mostly the outer layer of the application". Corrected in discussion: the core idea
  is the direction of dependencies; ports are interfaces the core defines, adapters implement them.
- Decided: no input/output split of the hexagon; each port is labelled with its own direction.
- The driving port (user code, the public API) was missing from the first two drawings.
- Ports on the board: AI, tools, observability, state store, context, structure (import/export).
- Review 01, Q14: `llm.py` imports the OpenAI and Gemini helpers directly, so the core depends on
  concrete adapters. A dependency-rule violation in the current code.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: core in the centre, adapters meeting it at ports, an ACL per adapter; a good Needle-specific why (external concerns built and tested separately, the core stays stable).
- Wrong or missing: the defining rule, which we discussed: dependencies point inward. The core defines the ports (interfaces) and knows nothing about the adapters. Also driving vs driven: user code and the editor drive the core, while AI providers, tools and the database are driven by it. Your tradeoff says all of these "use the core", but for providers and the database it is the core that calls out through a port. The hexagon shape itself means nothing.
- Corrected version: hexagonal architecture keeps the logic in a core that depends on nothing external. The core defines ports (interfaces), and adapters implement them for specific technologies. Driving adapters (the user API, the editor) call into the core; driven adapters (AI providers, tools, stores) are called by it. Any outside piece can then be swapped or faked without touching the core.
