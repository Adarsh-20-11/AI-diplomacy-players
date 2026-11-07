---
tags: [concept, architecture]
phase: 1
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Stateless LLM Clients

## What it is (my own words)
Yea, the reason why we needed this is because we want to build our own context and manage it ourselves as well. I know that is a lot to ask, especially when big tech companies like Google actually find it tough to do that in Gemini (I believe Anthropic has the best context management, it's wild), but yea, you get the point. It's so a Gemini model could use the same context a claude model utilizes. This way, we have truly broken the vendor lock that other mediums have issues with. I am sure that even in langgraph + langsmith, forwarding context between 2 models it NOT supported.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 4
- `needle-ai/src/needle/llmapi/base.py` and `needle-ai/src/needle/ai/wrapper/llm.py`
- [docs/design/review-01.md](../docs/design/review-01.md), Q10, Q11, Q20

## Tradeoff / why I chose this


## Related
- [[Canonical Data Model]]
- [[History vs Context View]]
- [[Hexagonal Architecture]]

## Quiz myself
1. Why can't an LLM client hold the conversation history if models are chosen per node?
2. Why one async `generate` method instead of four methods per provider?
3. Why async-first, and when does a sync wrapper built on `asyncio.run` fail?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Requirement: change the model per node for token efficiency without breaking the context,
  like switching between Sonnet and Opus with the same context.
- Review 01: an LLM object takes a request and returns a response, and holds no history. Default
  model at the agent level, per-slot override, resolved at build time.
- Collapse `invoke`, `ainvoke`, `invoke_chat`, `ainvoke_chat` into one async `generate`. Sync
  wrapper only at the public edge; `asyncio.run` fails inside an already running event loop
  (for example Jupyter).

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: the motivation: Needle manages context itself, so any model can continue a conversation another model started, which removes vendor lock-in.
- Wrong or missing: what stateless *means*: the client holds no conversation; it receives a full request (history, system prompt, tools, parameters) and returns a response. That is what allows per-node model choice and safe sharing of one client across nodes. A claim to check before relying on it: "forwarding context between 2 models is NOT supported in LangGraph + LangSmith". As far as I know, LangChain's message classes are provider-neutral and LangGraph state can be handed to a different chat model in another node, so this is likely wrong. A reviewer will check it, so verify it and claim a narrower difference if one exists (for example, handling of provider-private blocks).
- Corrected version: a stateless LLM client keeps no memory between calls. Every call receives the full context it needs and returns a response. The conversation lives in Needle's own format in the agent's state, so the client behind each node can be any provider.
- Follow-up (same day): Adarsh clarified the claim meant "in LangGraph, all nodes in a graph use the same model". That also appears wrong: nodes are plain functions and each can call its own model (examples: [DataCamp tutorial](https://www.datacamp.com/zh/tutorial/langgraph-tutorial), [UVA course notes](https://www.cs.virginia.edu/~rmw7my/Courses/AgenticAISpring2026/Topic2Frameworks/Agent%20Control%20Flow%20Frameworks.html), [surma.dev](https://surma.dev/things/langgraph/); not official docs). The prebuilt ReAct agent takes a single model, which may be the source of the impression. Per-node models therefore aren't a differentiator for Needle by themselves; narrower claims (one-line per-slot overrides on prebuilts, build-time validation of models and budgets) need checking against LangGraph's docs.
