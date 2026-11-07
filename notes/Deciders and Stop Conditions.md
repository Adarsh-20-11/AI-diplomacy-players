---
tags: [concept, architecture]
phase: 3
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Deciders and Stop Conditions

## What it is (my own words)
Well, I wouldn't say it's a huge architectural decision and would rather say it's a choice of node (similar to reasoning, or action) where the AI (or determenistic code) decides whether another loop should happen or not. Or tbh, that's more of an End-Decider, while a simple Decider is just something getting decided.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), "Loops and node types"
- [docs/design/react-flow.md](../docs/design/react-flow.md), observation 5
- [docs/design/review-01.md](../docs/design/review-01.md), Q18 and Q24

## Tradeoff / why I chose this
Because well, decisions are a core part of why people use AI in the first place, not having a decider node is just plainly going to have us lose a lot of structures that we could potentially build.

## Related
- [[Limits and Budgets]]
- [[Graph Validation]]
- [[Shared-State Graph vs Dataflow]]

## Quiz myself
1. How many LLM calls does one ReAct iteration need, and why?
2. When would you choose `LLMEndDecider` over `DetEndDecider`?
3. What is the strategy pattern, and how do deciders use it?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your design: an End-Decider node, a base Decider class, variants `LLMEndDecider` and
  `DetEndDecider`. Class families wide, not deep.
- Review 01: default stop is "the reply contains no tool calls", plus a maximum iteration count.
  The reasoning node is the model call; the action node runs the tools from that reply; the
  question node checks the reply. One LLM call per iteration. An LLM checking answer quality is
  really the Reflection pattern.
- Jev (TypeSafe AI, a non-generative model for bounded decisions; its claims are unverified)
  suggests a later "choose among these options" capability on the model port.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: a node type, backed by an AI or by deterministic code; the End-Decider vs general Decider distinction (a general decider is routing) is a good one.
- Wrong or missing: it *is* architecturally central: deciders are how control flow works, because they choose the next edge (conditional edges). For ReAct, the default is a deterministic stop (the reply has no tool calls) plus a maximum number of iterations, and one LLM call per iteration. The variants are the strategy pattern: one role, swappable backends. A loop must pass through a bounded decider.
- Corrected version: a decider is a node whose output is a route: it reads state and chooses the next node, and an End-Decider chooses between looping and ending. Implementations are interchangeable strategies, rule-based or model-judged. In ReAct the default rule is "stop when the reply has no tool calls, or when the iteration limit is reached".
