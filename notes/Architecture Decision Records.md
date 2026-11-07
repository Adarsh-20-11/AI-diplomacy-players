---
tags: [concept, practice]
phase: 1
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Architecture Decision Records

## What it is (my own words)
This just gives general decision audits for architecture. Stuff about why a particular architecture was chosen, why it was good, what are the trade-offs, etc.

## Where it lives in needle
- `docs/adr/` (none written yet)
- [docs/design/review-01.md](../docs/design/review-01.md), "ADRs needed first"

## Tradeoff / why I chose this


## Related
- [[Vertical Slice]]
- [[Canonical Data Model]]

## Quiz myself
1. What sections does an ADR have, and why does "alternatives considered" matter?
2. Which three ADRs come before Phase 1?
3. Should an ADR be written before or after the code it describes?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Planned: 0001 canonical message and response model, 0002 provider port, 0003 error model.
  Before Phase 3: 0004 shared-state graph vs dataflow, 0005 the build step.
- Rule: ADRs written in your own words, reviewed before committing.
- Suggested reading earlier: Michael Nygard's original ADR article and adr.github.io.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: records why an architecture decision was made, with its tradeoffs.
- Wrong or missing: the structure (context, decision, status, alternatives considered, consequences); one decision per record; written when the decision is made; never edited once accepted, but superseded by a new ADR, which is what makes it an audit trail. It records consequences including the bad ones, not "why it was good".
- Corrected version: an ADR is a short, numbered, immutable record of one architecture decision: the context, the decision, the alternatives rejected, and the consequences, good and bad. A changed decision gets a new ADR that supersedes the old one.
