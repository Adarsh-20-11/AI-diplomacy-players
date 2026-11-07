# Needle

Needle is a Python library for building AI agents. The idea: **prebuilt agent patterns
(ReAct, Reflection, ...) that you can "eject" into editable graphs.** `ReAct(llm, tools)` should
work in one line, and when you outgrow it, the same agent opens up as a graph you can change
node by node.

Two things I want Needle to do that I couldn't get easily elsewhere:

- **Switch models per node, mid-conversation, across providers.** One node on a cheap model,
  another on a strong one, sharing the same history. That needs every provider's messages
  normalized into one format Needle owns (see [ADR 0001](docs/adr/0001-canonical-message-model.md)).
- **Layered customization.** The simple case stays simple; each deeper layer is optional.

I know LangChain, LangGraph and CrewAI exist. This is a from-scratch project: I'm building it
to learn how agent frameworks work underneath, and to make design decisions myself instead of
inheriting them.

## Status

Early. Designed more than built.

| Stage | Status |
|---|---|
| Phase 0: tooling (uv, src layout, ruff, strict mypy, pytest, CI) | Done |
| Phase 1 design: architecture, external review, first ADR | Done |
| Phase 1 build: one vertical slice through all layers | In progress |
| ... canonical message model (`core/message.py`) | Done, with tests |
| ... request/response envelopes, LLM port, fake LLM, ReAct loop, first adapter | Next |

The older code in `llmapi/` and `ai/wrapper/` predates the design and will be replaced by the
slice.

## How this repo is organised

| Path | What's there |
|---|---|
| [needle-ai/](needle-ai/) | The library itself (`src/needle/`), tests, and project config |
| [docs/design/](docs/design/) | The architecture: whiteboards, hexagon diagram, ReAct flow, open questions, and an external design review |
| [docs/adr/](docs/adr/) | Architecture Decision Records: one file per decision, with the alternatives I rejected |
| [notes/](notes/) | My learning notes (see below) |

## How I'm working on it

This is a learning project first, so I've set some rules for myself:

- **I hand-type all library code.** AI reviews it and explains what's wrong, but doesn't write
  it for me.
- **Design before code.** The architecture was drawn on a whiteboard, written up, reviewed,
  and recorded in ADRs before the first core module was written.
- **Thin vertical slices.** One working path through every layer before widening any layer.

### The notes

`notes/` is an [Obsidian](https://obsidian.md) vault: one note per concept I've had to learn
for this project (hexagonal architecture, canonical data models, graph validation, ...). Each
note has my own explanation, a review of it, and a history of quiz answers, so it shows how my
understanding changed over time rather than only where it ended up.

### Use of AI

I use Claude as a reviewer and teacher, not as the author of the library: I write the code and
the design decisions, and the AI reviews them, challenges them and explains concepts.
Scaffolding (CI, design write-ups, the notes template) was AI-written. The exact split is in
[AI_USAGE.md](AI_USAGE.md).

## Running it

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```
cd needle-ai
uv sync
uv run ruff check
uv run mypy src
uv run pytest
```

CI runs the same checks on Python 3.12 and 3.13.

## Contributing

Not open for code contributions yet. Since I'm writing the core myself to learn, I can't merge
code PRs for now. Issues, design feedback and arguments about the ADRs are very welcome.
