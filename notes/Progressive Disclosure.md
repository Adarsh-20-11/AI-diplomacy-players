---
tags: [concept, architecture]
phase: 4
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Progressive Disclosure

## What it is (my own words)
Yes, this is something I thought of myself, and this is more like the way our engine would compile stuff right?

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 3 (customization ladder)
- [docs/design/review-01.md](../docs/design/review-01.md), Q5 and Q19

## Tradeoff / why I chose this
1. This way, compilation occurs in a way that doesn't entirely depend on the core stuff, giving users a wiggle room to do customization in the first place.
2. It gives a clear distinction between what are stuff that you 100% require, and what are stuff you can customize.
3. The user doesn't get the entire thing in one go and can make the decision about how deep they truly want to go.

## Related
- [[Build Time vs Run Time]]
- [[Graph Validation]]
- [[Deciders and Stop Conditions]]

## Quiz myself
1. What are the levels of Needle's customization ladder, with a ReAct example at each?
2. What is a slot, and which kind of customization is not a slot fill?
3. Why should editing a prebuilt agent produce a new spec instead of changing it in place?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your ladder: exoskeleton (structure), then essential choices (models, prompts, tools), then
  deep customization. You described it as calling dependency, and the layers as execution
  dependency.
- Diagram lesson: your rings put the foundation outermost, the reverse of the usual convention.
  Caption every diagram with what nesting or arrows mean.
- Slots: named, typed places (reason, act, decide) that customizations bind to. Changing the
  topology is a graph edit, validated by the build step.
- Your analogy: editing nodes like effect chains in Audacity.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: reasons 2 and 3 are exactly the point: separate what's required from what's optional, and let users choose how deep to go.
- Wrong or missing: it isn't about how the engine compiles. It's an API and UX design principle about how much complexity a user sees; it can line up with build stages, but the concept is user-facing. Missing: sensible defaults are what make the simplest level work, and each level should be reachable without rewriting the previous one (no cliff). The principle is well established in UI design; applying it as a ladder to an agent API is your contribution.
- Corrected version: progressive disclosure means a simple surface first, with complexity revealed only when the user asks for it. In Needle: one line with good defaults, then per-node choices, then graph edits, then fully custom nodes, each level building on the previous one without forcing a rewrite.
