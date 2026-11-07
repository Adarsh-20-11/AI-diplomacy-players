---
tags: [concept, architecture, system-design]
phase: 1
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Failure Handling in Agents

## What it is (my own words)
There can again be 2 types of errors, build errors and run-time errors. In case someone does not have a fixed End, or a fixed Start, that would come under a build error. I believe that in the naming itself, it means the run-time errors. Well, in case the agent throws an error, it's important to handle it with a trace, and also using our observability framework through it's adapter.

## Where it lives in needle
- [docs/design/react-flow.md](../docs/design/react-flow.md), observations 6 to 8
- [docs/design/review-01.md](../docs/design/review-01.md), Q13 and Q21
- Today: `LLMAPIError` in `needle-ai/src/needle/llmapi/exceptions.py`; ADR 0003 (to write)

## Tradeoff / why I chose this
Well, simply because Agents are always going to have some % chance of throwing errors, so we need to handle it gracefully, by not just throwing "Agent ran into an error" but rather a full stack trace and the state of the agent which lead to that error as well, otherwise whatever we are building is pointless.

## Related
- [[Limits and Budgets]]
- [[Deciders and Stop Conditions]]
- [[Anti-Corruption Layer]]

## Quiz myself
1. Why return a tool error to the model instead of raising it?
2. What makes an error retryable?
3. With parallel tool calls, how do you keep calls and results in the right order?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- The first ReAct flow had no failure paths; they were raised in review.
- Review 01: tool errors go back to the model as tool results marked as errors. Model errors:
  retry the retryable ones with backoff, raise the rest. An error hierarchy with a `retryable`
  flag. Parallel tool calls run concurrently, results recorded in call order after the assistant
  message. Nodes return updates and the engine is the single writer to state (reducers).
- In the current code: `raise LLMAPIError(...) from e` (B904) is right; `except Exception` is too broad.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: build errors vs run-time errors; errors should carry the trace and the state that led to them, reported through observability.
- Wrong or missing: in agents, "graceful" mostly means *recovering*, not only reporting. Tool errors go back to the model as error results so it can try something else; transient provider errors (rate limits, timeouts) are retried with backoff; only unrecoverable errors stop the run. That needs errors classified (retryable or not), and a checkpoint lets a failed run resume.
- Corrected version: agent failure handling classifies errors and picks a response per class: feed tool errors back to the model, retry transient provider errors with backoff, fail fast on configuration errors (a bad key, an invalid request), and on a real failure surface the error with its trace and the state, keeping a checkpoint to resume from.
