---
tags: [concept]
phase: 0
status: draft
score: 3
last_reviewed: 2026-11-01
---

# Linting vs Type Checking

## What it is (my own words)
ruff is a linter and a formatter and it usually catches errors pertaining to import problems and small bugs.
mypy is a type checker
pytest is where you write your own tests, wrt to code quality or contracts (api or function contracts as perse)

*(imported verbatim from the 2026-10-28 session)*

## Where it lives in needle
- `[tool.ruff]`, `[tool.mypy]` and `[tool.pytest.ini_options]` in needle-ai/pyproject.toml


## Tradeoff / why I chose this


## Related
- [[Pyflakes]]
- [[pyproject.toml]]

## Quiz myself
1. 
2. 
3. 

## Reviews (Claude)
### 2026-11-01, score 3/5
- Correct: the one-line role of each tool.
- Wrong or missing: the note lists the tools but doesn't contrast linting and type checking, which is the title. A linter reads syntax and patterns without knowing types (unused imports, undefined names, style). A type checker follows the types of values through the code and checks that they fit. You have now met real errors from both, so it is easy to add examples. pytest checks behaviour by running code, which neither of the other two does.
- Corrected version: ruff and mypy are static (nothing runs), but ruff looks at code shape and mypy at types. pytest is dynamic (it runs the code). Each catches what the others can't.
