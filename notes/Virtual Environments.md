---
tags: [concept]
phase: 0
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Virtual Environments

## What it is (my own words)
Uv is like a new venv manager that was made on Rust and hence is blazingly fast, and has probably replaced venv in a lot of spaces.

venv is just a virtual environment so your python version and package versions stay static until you actually want to change them by adding re-dev efforts. Plus, it helps you able to run it on any system without any issues, but yea, it has mostly been replaced by uv. Oh yea, it's also helpful in loading your stuff into docker for testing as well.

*(imported verbatim from the 2026-10-28 session)*

**Quiz answer (2026-11-07):**
venv gives us an isolated environment to maintain a different python version, a set of python libraries, etc for a particular project, without disturbing the main python version in our system. One core advantage for that is that if the python version in our system changes, it doesn't break our packages in the venv. What pins the package versions? I believe that is being done by uv since it's the one which creates a venv and manages it for us. And lastly, the reason why my pytest.exe broke after I moved the project folder was because the path was still given to be the older folder path, which had since changed.

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

### 2026-11-07, quiz, score 3/5
- Question: What does a venv give you, what pins the package versions, and why did pytest.exe break after moving the project folder?
- Correct: isolation of one project's packages from the system and other projects; and pytest.exe broke because its launcher had the old absolute path baked in. Exactly right, and it was the note's biggest gap.
- Wrong or missing: the "core advantage" is backwards. A venv is tied to its base interpreter (your `pyvenv.cfg` says `home = C:\Python315`); if that Python is upgraded or removed, the venv usually breaks and has to be rebuilt. Pinning isn't done by uv as a tool but by the lockfile, `uv.lock`, which uv writes; `uv sync --locked` installs exactly what it lists.
- Follow-up (same day): Adarsh pointed out that `uv.lock` is part of uv and the question didn't ask for the mechanism. Accepted: the pinning part counts as correct. The score stays 3 because of the claim that a venv survives a change to the system Python, which is backwards.
