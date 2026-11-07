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
| Virtual environments | [[Virtual Environments]] | 2 | 3 | 2026-11-07 | thinks venv survives system Python changes |
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
| Hexagonal architecture | [[Hexagonal Architecture]] | 1 | 3 | 2026-11-07 | misses dependency direction; driving vs driven |
| Anti-corruption layer | [[Anti-Corruption Layer]] | 1 | 4 | 2026-11-07 | frames it as symmetric; no Needle placement |
| Canonical data model | [[Canonical Data Model]] | 2 | 4 | 2026-11-07 | tool adapter translates into it too (said AI adapter only) |
| Build time vs run time | [[Build Time vs Run Time]] | 2 | 3 | 2026-11-07 | user input placed at build time; benefits counted twice |
| Progressive disclosure | [[Progressive Disclosure]] | 1 | 3 | 2026-11-07 | tied to compilation instead of API/UX |
| Shared-state graph vs dataflow | [[Shared-State Graph vs Dataflow]] | 2 | 4 | 2026-11-07 | forwards whole state between agents (should be output only); no why |
| History vs context view | [[History vs Context View]] | 2 | 3 | 2026-11-07 | skipped the consequence half; context as one current version |
| Stateless LLM clients | [[Stateless LLM Clients]] | 1 | 3 | 2026-11-07 | doesn't define stateless; unverified LangGraph claim |
| Deciders and stop conditions | [[Deciders and Stop Conditions]] | 1 | 3 | 2026-11-07 | undersells deciders as control flow |
| Limits and budgets | [[Limits and Budgets]] | 1 | 3 | 2026-11-07 | per-call cap placed in the decider |
| Graph validation | [[Graph Validation]] | 2 | 4 | 2026-11-07 | omits connectivity / reachability |
| Failure handling in agents | [[Failure Handling in Agents]] | 1 | 3 | 2026-11-07 | reporting over recovery |
| Architecture decision records | [[Architecture Decision Records]] | 1 | 3 | 2026-11-07 | missing structure and immutability |
| Vertical slice | [[Vertical Slice]] | 1 | 4 | 2026-11-07 | misses "through all layers" |
| Low-level vs high-level design | [[Low-Level vs High-Level Design]] | 1 | 3 | 2026-11-07 | neither side defined |

## Patterns so far
- You tend to describe a thing by what it contains (the tests, the tools) instead of what it *is* or does. CI, venv and pyproject all showed this.
- You often get the right intuition and mislabel it (venv "portable", `E` as "errors", uv as the backend).
- (2026-11-07, architecture batch) Neighbouring concepts merge: the build step absorbs the
  canonical model, encapsulation and progressive disclosure. When a concept touches the
  "compiler", check whether you're describing that concept or the build step.
- Meta statements stand in for explanations ("not a huge architectural decision", "similar to
  the previous point"). Say what the thing *is* before judging how important it is.
- Strongest when writing the Needle-specific "why" (hexagonal, vertical slice, ACL).
