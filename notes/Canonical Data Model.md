---
tags: [concept, architecture]
phase: 1
status: draft
score: 4
last_reviewed: 2026-11-07
---

# Canonical Data Model

## What it is (my own words)
I think this has a lot of similarities with the previous point with respect to a common data model that could be used for interaction between multiple components in our needle library.

**Quiz answer (2026-11-07):**
I would say that the connonical model here is the standardized objects that the AI adapter creates for us for using it in our core engine and other adapters. This enables us to maintain history and context for multiple models making it possible for context to be taken forward even during model changes.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 4
- [docs/design/review-01.md](../docs/design/review-01.md), Q2 and Q3
- ADR 0001 (to write)

## Tradeoff / why I chose this


## Related
- [[Anti-Corruption Layer]]
- [[History vs Context View]]
- [[Stateless LLM Clients]]

## Quiz myself
1. Why store history in Needle's own format instead of a provider's?
2. Name three things that don't survive a cross-provider model switch, and how each is handled.
3. Why block-based messages rather than copying one provider's shape?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your observation after reading the Anthropic, OpenAI and Gemini docs: same information,
  different shapes. Your "spec sheet engine" idea: normalize everything into Needle's own format.
- Requirement: switch models mid-conversation without breaking the context.
- Review 01: a neutral, block-based model (a message is a role plus typed content blocks); the
  system prompt as a separate field; tool-call ids kept, with adapters generating or sanitizing
  them; reasoning blocks opaque, tagged with provider and model, dropped only when the provider
  changes; tokenizers and prompt caching are not portable.
- The promise: full support within one provider; across providers, text, tool calls and tool
  results carry over.
- The response must carry token usage (budgets need it).

## Reviews (Claude)
### 2026-11-07, score 2/5
- Correct: a common data model that components use to communicate.
- Wrong or missing: "similar to the previous point" links it to build time, which is a different concept. Missing: in Needle it is the provider-neutral format for messages and responses; history is stored in it; each adapter translates to and from it at the edge; that is what lets one model continue a conversation another started. Nothing about Needle's specific choices (blocks, separate system prompt, usage).
- Corrected version: a canonical data model is one shared format owned by the system, which every component speaks, with translation only at the boundaries. In Needle it's the provider-neutral message and response types: history lives in them and adapters convert at the edge, so any model can continue any conversation.

### 2026-11-07, quiz, score 4/5
- Question: What is Needle's canonical data model, where does the translation into it happen, and what does it make possible that storing history in OpenAI's format wouldn't?
- Correct: standardized objects produced at the adapter and used by the core; it lets context carry over when the model changes. Answers all three parts.
- Wrong or missing: say that it's Needle-owned and provider-neutral (blocks, messages, request and response), and that the tool adapter translates into it too, not only the AI adapter. The sharpest point is that history is *stored* in it: with OpenAI's format, switching to Gemini would mean translating every stored message from one vendor's shape into another's.
- Follow-up (same day): Adarsh pointed out that "maintain history ... for multiple models" already says history lives in the canonical format. Accepted; the remaining gap is only that the tool adapter translates into it too.
