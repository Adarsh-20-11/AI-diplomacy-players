---
tags: [concept]
phase: 0
status: draft
score: 3
last_reviewed: 2026-11-01
---

# pyproject.toml

## What it is (my own words)
Here I actually did more research. What I understood is, there are 3 main buckets, [build-system], [project] and [tool], and while tool mostly utilizes the tests use cases and their documentations are more tailored into the tool tiself, it is still part of the pyproject.toml file.

The build-system is mostly just information about the actual build backend behind our package. So basically, if my build system here is uv (and well, any person would choose that since it's blazing fast), I need to just put that here along with it's versioning.

Other information with respect to the project, the requirements and dependencies, the python version, authors, license, etc comes under the project bucket.

The tool bucket, like I mentioned earlier, were for testing and other such tools and their documentation would depend on the tool itself.

*(imported verbatim from the 2026-10-28 session)*

## Where it lives in needle
- needle-ai/pyproject.toml


## Tradeoff / why I chose this


## Related
- [[Src Layout]]
- [[Linting vs Type Checking]]

## Quiz myself
1. 
2. 
3. 

## Reviews (Claude)
### 2026-11-01, score 3/5
- Correct: the three tables, and what goes in `[project]` and `[build-system]`.
- Wrong or missing: `uv` is the workflow tool, not the build backend. The backend is a separate piece (`uv_build`, `hatchling`, ...) that turns source into an installable package, and you can use uv with any backend. `[tool]` holds settings for any tool (ruff, mypy, pytest, uv itself), not only tests. You also left out `[project.optional-dependencies]` and why it matters for a multi-provider library.
- Corrected version: `[build-system]` names the backend, `[project]` describes the package, `[tool.*]` configures any tool you use, and optional dependencies let users install only the provider they need.
