---
tags: [concept]
phase: 0
status: draft
score: 2
last_reviewed: 2026-11-01
---

# Virtual Environments

## What it is (my own words)
Uv is like a new venv manager that was made on Rust and hence is blazingly fast, and has probably replaced venv in a lot of spaces.

venv is just a virtual environment so your python version and package versions stay static until you actually want to change them by adding re-dev efforts. Plus, it helps you able to run it on any system without any issues, but yea, it has mostly been replaced by uv. Oh yea, it's also helpful in loading your stuff into docker for testing as well.

*(imported verbatim from the 2026-10-28 session)*

## Where it lives in needle
- needle-ai/.venv (generated, not committed)


## Tradeoff / why I chose this


## Related
- [[pyproject.toml]]

## Quiz myself
1. 
2. 
3. 

## Reviews (Claude)
### 2026-11-01, score 2/5
- Correct: uv is fast and is written in Rust, and isolating a project's packages is the point of a venv.
- Wrong or missing: uv does not replace the venv. It creates and manages one for you. A venv gives isolation (this project's packages don't mix with others), not version pinning, and not portability. Pinning comes from the lockfile, `uv.lock`. "Run it on any system" is the opposite of the truth, as you found out in Phase 0: a venv can't be moved, because its launcher scripts hold absolute paths.
- Corrected version: a venv is an isolated folder of packages tied to one interpreter and one location. uv builds and syncs it from `pyproject.toml` and `uv.lock`, and you rebuild it, never move it.
