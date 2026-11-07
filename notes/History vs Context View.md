---
tags: [concept, architecture]
phase: 1
status: draft
score: 3
last_reviewed: 2026-11-07
---

# History vs Context View

## What it is (my own words)
Well, history will 100% go and merge into a context, and well, the entire context sub system may have conext divided into projects, or use cases, or whatever, and how it is handled with respect to cacheing, or changing sizes and everything will be handled by the context subsystem while the core would only care about getting the context for the current task.
History on the other hand would actually matter lesser than context, and these are basically contexts that have grown stale, or are old and the context subsystem have compacted it. This way, we don't have to spend a lot of tokens or processing power into actually pulling entire contexts along with history and only focus on the latest ones.

**Quiz answer (2026-11-07):**
Full history is the entire history of calls and content that has been created by agents, while context is the current compacted version of the history which the Agent/AI currently uses to make inference, decisions and generation.

## Where it lives in needle
- [docs/design/review-01.md](../docs/design/review-01.md), Q8 and Q17
- [docs/design/react-flow.md](../docs/design/react-flow.md), observation 4

## Tradeoff / why I chose this


## Related
- [[Canonical Data Model]]
- [[Stateless LLM Clients]]
- [[Shared-State Graph vs Dataflow]]

## Quiz myself
1. Why must context shaping never edit the stored history?
2. Which part of "context" is a port, and which is core logic?
3. Where does the message history live during a ReAct run?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- The ReAct flow had the loop reading and writing "Context", with "State management" as a side sink.
- Decided: the context adapter only connects; the context subsystem decides what to do with what
  it fetches.
- Review 01: history in state is the source of truth. Each model call gets a trimmed or
  summarized view of it. Fetching is a port; shaping is core logic, and may take an injected LLM
  to summarize.
- Open: are "context greps" tools the model chooses to call, or context the framework injects?

## Reviews (Claude)
### 2026-11-07, score 2/5
- Correct: the core should only ask for the context for the current task, and the context subsystem owns sizing, compaction and caching.
- Wrong or missing: the note defines history as stale context that has been compacted, which means the *stored* data gets compacted. That inverts the concept, and it works against your own goals: compaction loses information, so you couldn't later give a bigger-window model the full conversation, resume exactly from a checkpoint, replay runs for evals, or show the state that led to a failure (which your failure note asks for). The concept is that full history is the source of truth and is never edited; context is a view computed from it for each call. If you disagree, that's a legitimate design debate: write your argument in the Tradeoff section and we'll take it up.
- Corrected version: history is the complete, append-only record of a run, kept in state. Context is what one particular model call sees: a view built from history (trimmed, summarized, plus fetched material) to fit that model's window and task. Shaping context never destroys history.

### 2026-11-07, quiz, score 3/5
- Question: Define history and context in one sentence each, then give one concrete thing you'd lose if the stored history were compacted.
- Correct: the definitions are now the right way round: history is the full record, context is the compacted view the model uses. That fixes the main error in the note.
- Wrong or missing: the second half of the question was skipped. Compacting the stored history would lose, for example: giving a bigger-window model the full conversation, resuming exactly from a checkpoint, replaying runs for evals, or seeing the state that led to a failure. Also, context isn't one "current" version: it's computed for each call, and can differ per model and per node.
