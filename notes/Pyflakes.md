---
tags: [concept]
phase: 0
status: draft
score: 3
last_reviewed: 2026-11-01
---

# Pyflakes

## What it is (my own words)
This is basically an analyzer which analyzes without ever running any line of code. What it gives as an output is more similar and close to stuff which are logical, but not things that get caught in type testing nd mypy test (hence complementing it perfectly). It is instantiated under ruff tools and the test character 'F' stands for it. It's not a standard error checker as perse, that's the 'E' character, this deals more towareds a bit of the potential logical issues like missing imports, or variable never used, import never used, etc.

## Where it lives in needle
- `[tool.ruff.lint] select` in needle-ai/pyproject.toml
- Real hit: F401 in tests/test_import.py (`from needle import ai` is never used)

## Tradeoff / why I chose this
Cheap and fast, catches bugs before tests run. Won't catch wrong types, so it complements mypy.

## Related
- [[Linting vs Type Checking]]
- [[pyproject.toml]]

## Quiz myself
1. Why can Pyflakes find an undefined name without running the program?
2. What's the difference between an `E` finding and an `F` finding?
3. Why do I still need mypy if Pyflakes is clean?

## Reviews (Claude)
### 2026-11-01, score 3/5
- Correct: static analysis without running code; it complements mypy instead of overlapping with it; the examples (unused import, unused variable) are real F rules; `F` is the code ruff uses for it.
- Wrong or missing: `E` is not "the standard error checker". It is the pycodestyle rules, i.e. formatting and style (line length, whitespace). Most real bugs show up under `F`, which is the reverse of what "standard error" suggests. "Missing imports" is more precisely an undefined name (F821): the name is used but never defined or imported. "Logical issues" is loose, since Pyflakes finds probable bugs and not wrong business logic. "Instantiated under ruff" isn't the right verb: ruff reimplements Pyflakes's checks and labels them `F`. You didn't say *how* it works without running code, which is quiz question 1.
- Corrected version: Pyflakes parses the source into a syntax tree and walks it to find probable bugs (unused or undefined names, unused imports), without executing anything. Ruff reimplements these checks as `F` rules. `E` rules are style, and types are mypy's job.
