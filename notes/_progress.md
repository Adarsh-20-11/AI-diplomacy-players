# Progress tracker

Maintained by Claude after each review or quiz. Quizzes pick concepts with low or
falling scores first, then ones not reviewed for a long time.

## Scale (1-5)
| Score | Meaning |
|---|---|
| 1 | Wrong idea, or can't explain it |
| 2 | Vague, partly right, key point missing |
| 3 | Right idea, imprecise terms |
| 4 | Correct and precise, small gaps |
| 5 | Correct, precise, and can apply it to needle code |

`status: solid` needs a 4+ on two reviews, or a quiz answered without looking.

## Concepts
| Concept | Note | Attempts | Latest | Last reviewed | Recurring mistake |
|---|---|---|---|---|---|
| Src layout | [[Src Layout]] | 1 | 4 | 2026-11-01 | reason for relative imports is imprecise |
| pyproject.toml | [[pyproject.toml]] | 1 | 3 | 2026-11-01 | uv (tool) vs build backend; `[tool]` is for any tool |
| Virtual environments | [[Virtual Environments]] | 1 | 2 | 2026-11-01 | thinks uv replaces venv; venv = isolation, not pinning or portability |
| Linting vs type checking | [[Linting vs Type Checking]] | 1 | 3 | 2026-11-01 | lists the tools without contrasting them |
| Continuous integration | [[Continuous Integration]] | 1 | 2 | 2026-11-01 | describes testing levels instead of the automation |
| Pyflakes | [[Pyflakes]] | 1 | 3 | 2026-11-01 | reads `E` as "errors" (it is style); loose on how static analysis works |
| pytest discovery and plain `assert` | | 0 | | | |
| Venvs aren't portable | | 0 | | | |
| B904, `raise ... from e` | | 0 | | | |
| Absolute vs relative imports | | 0 | | | |
| mypy strict, `no-untyped-def` | | 0 | | | |
| Implicit Optional and narrowing | | 0 | | | |
| Generics and `type-arg` | | 0 | | | |
| Liskov and `override` | | 0 | | | |
| `TypedDict` and `arg-type` | | 0 | | | |
| Converters at the provider edge | | 0 | | | |

## Patterns so far
- You tend to describe a thing by what it contains (the tests, the tools) instead of what it *is* or does. CI, venv and pyproject all showed this.
- You often get the right intuition and mislabel it (venv "portable", `E` as "errors", uv as the backend).
