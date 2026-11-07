---
tags: [concept, system-design]
phase: meta
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Low-Level vs High-Level Design

## What it is (my own words)
I think I know that, I am mostly working on low level design, but I want to start building from there, high level designs are specifically more valid when you start building cloud systems, or web applciations, or any SaaS systems to be honest which are on cloud. It is a valid skills, but i think having a low level understanding first would help me more in the long run.

## Where it lives in needle
- Not in the code. Needle's architecture work is one side of this distinction.

## Tradeoff / why I chose this


## Related
- [[Hexagonal Architecture]]
- [[Vertical Slice]]

## Quiz myself
1. Which kind of design is Needle's architecture work?
2. What do system design interviews at big tech companies usually test?
3. Name four distributed-design topics you haven't studied yet.

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- From the assessment: Needle work is software architecture, or low-level design (modules,
  interfaces, dependencies, data models). Big-tech system design interviews are usually
  high-level distributed design (databases, caching, queues, scaling, consistency, capacity
  estimates).
- Suggested reading: *Designing Data-Intensive Applications* by Martin Kleppmann.
- Assessment snapshot: strong on decomposition, tradeoffs, and defending or revising ideas;
  developing on data flow, failure modes and precision; weak on scope discipline.

## Reviews (Claude)
### 2026-11-07, score 3/5
- Correct: Needle is low-level design, and high-level design matters for distributed, cloud-hosted systems.
- Wrong or missing: neither side is defined. LLD: classes, interfaces, modules, data models, patterns and error handling inside one codebase. HLD: services, data stores, caching, queues, scaling, availability, consistency, capacity estimates. HLD isn't only for SaaS; any system spread across machines needs it, and big-tech interviews test both, with HLD weighted more as seniority rises. Doing LLD first is a reasonable choice, but it's a choice, not a fact.
- Corrected version: LLD designs the internals of one program (modules, interfaces, data models); HLD designs how multiple components and machines fit together (services, storage, scaling, reliability). They complement each other, and interviews test both.
