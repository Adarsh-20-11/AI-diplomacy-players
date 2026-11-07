# Needle architecture: design review pack

**Audience:** a reviewer (Opus session) critiquing the architecture before Phase 1 is built.
**Author of the design:** Adarsh. This pack was transcribed from their whiteboards and design
discussion; the decisions are theirs. Anything I (Claude) added or suggested is tagged.

## Working rules for the reviewer

- Adarsh writes all the library code by hand (learning project, portfolio piece). Do not write
  implementation. Critique, explain, ask questions, give pseudo-code or hints.
- Challenge the design. "Looks good" is not useful; specific objections and alternatives are.
- Decisions are recorded as ADRs in `docs/adr/` once settled (none written yet).

## What Needle is

A Python agent library. Pitch: **prebuilt patterns (ReAct, Reflection, ...) that you can eject
into editable graphs.** `ReAct(llm, tools)` works in one line; the underlying graph can still be
edited. Multi-provider (OpenAI, Gemini, Anthropic planned). Later: a visual graph editor.
Key requirements stated so far:

1. Normalize every provider's responses into Needle's own format.
2. Change the model for individual parts of an agent (token efficiency), without breaking the
   context. Conversation history must survive a model switch (Opus <-> Sonnet, and ideally
   across providers).
3. Layered customization: simple case is one line, each deeper layer is optional.

## Status legend used in these docs

| Tag | Meaning |
|---|---|
| **[decided]** | Adarsh stated this as the design |
| **[leaning]** | Adarsh agreed in discussion but hasn't committed |
| **[suggested]** | Raised by Claude in review; not adopted yet |
| **[open]** | Unresolved |

## Contents

| File | What it has |
|---|---|
| [architecture.md](architecture.md) | Hexagon, ports and adapters, build time vs run time, the customization ladder |
| [open-questions.md](open-questions.md) | What the reviewer is asked to challenge |
| [react-flow.md](react-flow.md) | The ReAct execution flow (DAG), pre-check observations. The step-by-step trace is **not written yet** (Adarsh's to write) |
| [review-01.md](review-01.md) | First design review (Opus): view on every open question, changes before Phase 1, ADRs needed, what is missing |
| [whiteboards/](whiteboards/) | The original drawings (v1 hexagon, v2 hexagon, v2 layers, ReAct flow v1 and v2) |

## Where the code is today (Phase 0 finished)

- `needle-ai/src/needle/` with `llmapi/` (OpenAI and Gemini helpers, `JSONStandardizer`,
  `LLMAPIError`), `ai/wrapper/llm.py` (provider switch), `ai/structs/react.py` (a 5-line placeholder that just returns an `LLM`; no ReAct loop yet).
  `BaseLLMClient` declares only `invoke` and `ainvoke`; `invoke_chat` and `ainvoke_chat` exist on
  the two helpers but are not part of the base contract.
- Strict mypy, ruff and pytest pass locally; CI workflow written (`.github/workflows/ci.yml`).
- Known issues in the current code that Phase 1 is meant to resolve: messages are loose
  `dict`s; four near-duplicate methods per provider (`invoke`, `ainvoke`, `invoke_chat`,
  `ainvoke_chat`); the Gemini message conversion is copy-pasted in sync and async;
  `JSONStandardizer` handles responses only (not history going back in); `LLM.__init__` takes
  a `sync` argument that is actually passed as the API key; `SyntaxError` is raised for an
  unknown provider; no tool or message-block types yet.

## Roadmap (from the earlier planning session)

0 Foundations (done) - 1 Provider layer (typed messages, adapters, retries, `FakeLLM`) -
2 Tools - 3 Graph runtime - 4 Prebuilt patterns - 5 Observability and checkpointing -
6 Evals - 7 Visual editor - 8 Launch.
