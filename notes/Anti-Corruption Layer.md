---
tags: [concept, architecture]
phase: 1
status: draft
score: 4
last_reviewed: 2026-11-07
---

# Anti-Corruption Layer

## What it is (my own words)
It's sort of like a layer between two sub systems which keep their in built definitions and specs separate. This is to make sure that both of them don't have definitions and specs get mismatched and corrupt one or the other. And well, this is the space that holds most of the translation + verification and it goes both ways. This is to make sure that the only thing that's passed between these sub systems are spec sheets or structure that they understand.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 1 (decisions)
- Today's translator: `needle-ai/src/needle/llmapi/json_standardize.py` (`JSONStandardizer`)
- [docs/design/review-01.md](../docs/design/review-01.md), Q7

## Tradeoff / why I chose this


## Related
- [[Hexagonal Architecture]]
- [[Canonical Data Model]]
- [[pyproject.toml]]

## Quiz myself
1. Why is an anti-corruption layer mainly about translation, not validation?
2. Why one translator per provider instead of one central class?
3. Why make translators pure functions, and how would you test them?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- First drawn as a wall around the whole core, labelled "validation check with expected spec sheet".
- Decided: the ACL lives in the adapters, one per external system. An adapter is a connection
  part plus a translator part.
- Review 01, Q7: put each translator beside its adapter (a package per provider). A central class
  imports every SDK, which breaks optional extras such as `needle[openai]`. Test translators
  against recorded response fixtures.

## Reviews (Claude)
### 2026-11-07, score 4/5
- Correct: a translating layer between two subsystems with different models; translation plus verification; works in both directions; only shapes the other side understands cross it.
- Wrong or missing: it is asymmetric. It sits on *your* side and protects *your* model from a foreign one (the provider SDK doesn't care about Needle), while "corrupt one or the other" suggests a symmetric guard. The note doesn't say where it lives in Needle (one per provider adapter, as its translator), which is the gap between a 4 and a 5.
- Corrected version: an ACL is a translation boundary your system owns. It converts a foreign model into yours and back, so foreign concepts never leak into your core. In Needle each provider adapter has one: its translator turns provider responses into canonical types and canonical requests into provider calls.
