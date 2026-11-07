---
tags: [concept, architecture]
phase: 3
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Limits and Budgets

## What it is (my own words)
_(imported from the chat discussion of 2026-11-07, at Adarsh's request)_

I get your point about the global limits, but I think limits should depend on the kind of task you are running, instead of deciding a token limit for... the entire structure and then pausing in between that. Because like, hear me out right, inside a ReAct structure, you may think "Hmm, I only want to allocate these many output tokens on this particular node structure"
while for another different ReAct node you may want a different one. And where does the logic for the decision lie here? In the Decider node.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), "Further decisions"
- [docs/design/review-01.md](../docs/design/review-01.md), Q25

## Tradeoff / why I chose this


## Related
- [[Deciders and Stop Conditions]]
- [[Canonical Data Model]]
- [[Failure Handling in Agents]]

## Quiz myself
1. Why can't a decider enforce a per-call output token limit?
2. Where does a cumulative budget across loop iterations live?
3. What is the engine-level ceiling for, if not task policy?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- You argued that limits belong to the task and node, not one global number. Accepted: the
  global-limit framing was overstated.
- The split: per-call output tokens are node configuration, set before the call; cumulative
  budgets live in the decider, reading usage from state; a high engine ceiling is only a seatbelt.
- Requires usage in every response, and the engine accumulating it into state.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: limits are a per-task, per-node policy, not one global number. You were right to push back on that.
- Wrong or missing: a per-node output-token limit can't be decided in the decider: a call's output cap must be set *before* the call (max tokens on the request), because nothing can stop it midway. Deciders hold cumulative budgets across iterations, reading usage from state. A high engine-wide ceiling is still worth keeping as a seatbelt against bugs. Next time, write the note as an explanation, not only as an argument.
- Corrected version: limits sit at three levels: per-call caps in node configuration, applied by the provider; cumulative budgets checked by deciders between iterations, using the usage recorded in state; and an engine-wide ceiling that stops runaway runs whatever the user configured.
