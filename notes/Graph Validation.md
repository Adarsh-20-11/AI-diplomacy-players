---
tags: [concept, architecture]
phase: 3
status: draft
score: 4
last_reviewed: 2026-11-07
---

# Graph Validation

## What it is (my own words)
I wouldn't really say that this is a complete architectural decision, but rather one part of the build level checks or build errors.

**Quiz answer (2026-11-07):**
Checks which occur:
     i. Whether it has a start node
     ii. It has an ending node
     iii. In case of loops, a token/loop limit (decider)
     iv. all node and model types valid
     v. All slots are filled and are compatible.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), "Further decisions"
- [docs/design/review-01.md](../docs/design/review-01.md), Q1
- ADR 0005 (before Phase 3)

## Tradeoff / why I chose this


## Related
- [[Build Time vs Run Time]]
- [[Deciders and Stop Conditions]]
- [[Shared-State Graph vs Dataflow]]

## Quiz myself
1. List the structural checks, and say which are errors and which are warnings.
2. Why must every cycle pass through a bounded decider?
3. Which agent behaviour can a build step never check?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your rules: a start node and an end node are required, always connected; warnings for orphans.
- Added in review: a node that cannot reach the end is an error; every cycle passes through a
  bounded decider; node types exist in the registry; slots are filled; input and output types
  line up; every chosen model has an installed adapter.
- The output is a validated, immutable graph. Not a code-generating compiler.

## Reviews (Claude)
### 2026-11-07, score 2/5
- Correct: it belongs to the build-time checks.
- Wrong or missing: the note doesn't say what gets validated. Your own rules from the design discussion were good and belong here: start and end required, everything connected, warnings for orphans. Also: nodes that can't reach the end, cycles without a bounded decider, unknown node types, unfilled slots, mismatched input and output types, models without an installed adapter, and which of these are errors vs warnings.
- Corrected version: graph validation is the set of structural checks the build step runs on a spec before execution: everything reachable from the start, every node able to reach the end, every cycle bounded by a decider, all node types and models resolvable, slots filled and types compatible. Errors block the build; warnings (such as orphans) don't.

### 2026-11-07, quiz, score 4/5
- Question: List four checks the build step runs on a graph, and which one guarantees an agent can't loop forever.
- Correct: start, end, bounded loops through a decider, valid node and model types, slots filled and compatible. Check iii is the one that prevents endless loops.
- Wrong or missing: connectivity. Having a start and an end doesn't mean they're connected: every node must be reachable from the start and able to reach the end (orphans are a warning, dead ends an error). Also name which check answers the "loop forever" part explicitly next time.
