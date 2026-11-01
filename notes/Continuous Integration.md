---
tags: [concept]
phase: 0
status: draft
score: 2
last_reviewed: 2026-11-01
---

# Continuous Integration

## What it is (my own words)
CI stands for continuous integration, so let's say you built 6 features today and now you want to add another feature tomorrow. You won't want to disturb the already existing 6 features, so you have multiple levels of testing. You start off with the unit tests (whether the code for the new feature does what is required and in the way that is expected wrt latency and method), and once that passes, you do the integration test (to see if the contracts of those functions match with the already set contracts, basically if it integrates well with the already existing 6 features), and then over that an overall test that tests the entire library together.

*(imported verbatim from the 2026-10-28 session)*

## Where it lives in needle
- not written yet (planned: a GitHub Actions workflow running pytest, ruff and mypy)


## Tradeoff / why I chose this


## Related
- [[Linting vs Type Checking]]

## Quiz myself
1. 
2. 
3. 

## Reviews (Claude)
### 2026-11-01, score 2/5
- Correct: your description of the testing levels (unit, integration, whole library) is accurate, and the instinct that new work shouldn't break old work is the right motivation.
- Wrong or missing: you described testing, not CI. CI is the automation: the checks run on a clean machine on every push or pull request, so a break can't be merged unnoticed. The levels of testing are what CI runs, not what it is. Also, unit tests check behaviour, not latency.
- Corrected version: CI is an automatic pipeline (tests, lint, types) that runs on every change on a fresh machine, so "works on my machine" can't hide a break.
