---
tags: [concept, practice]
phase: 1
status: draft
score: 4
last_reviewed: 2026-11-07
---

# Vertical Slice

## What it is (my own words)
Testing architecture on a small use case first to get a feel of things, make sure everything works and makes sense before going for a complete implementation. In my case, going for a ReAct loop creation first, before adding all other nodes and structures just to test if my architecture even works in the first place and make changes where required.

## Where it lives in needle
- [docs/design/review-01.md](../docs/design/review-01.md), "Changes before Phase 1", item 1

## Tradeoff / why I chose this


## Related
- [[Architecture Decision Records]]
- [[Low-Level vs High-Level Design]]

## Quiz myself
1. What is in Needle's Phase 1 slice, and what is deliberately left out?
2. Why design the graph runtime after a hand-written ReAct loop has run?
3. What does this approach cost?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Concern in review 01: 25 open questions across seven phases, against very little working code.
- Recommendation: canonical types, one async `generate` per adapter, the error hierarchy,
  `FakeLLM`, and a hand-written ReAct loop with one tiny tool. No build step, spec format or
  registry yet. The loop becomes the baseline the Phase 4 graph-based ReAct must match.
- Scope discipline was the weak spot in the system design assessment.

## Reviews (Claude)
### 2026-11-07, score 4/5
- Correct: build a small working use case first to validate the architecture and adjust it; the ReAct loop as Needle's slice.
- Wrong or missing: the "vertical" part: the slice runs through every layer end to end (public call, core loop, canonical types, adapter, real provider), as opposed to finishing one layer completely (horizontal). It's building, not only testing, and it deliberately leaves things out (build step, spec, registry).
- Corrected version: a vertical slice is a thin feature built through all layers of a system end to end, so the architecture is proven by working code before any layer is finished in full. Needle's Phase 1 slice is a hand-written ReAct loop from the public call down to one real provider.
