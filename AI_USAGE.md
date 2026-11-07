# Use of AI in this repo

I use Claude (Anthropic) as a reviewer and teacher while building Needle. This file says
exactly who did what, so nobody has to guess.

## Written by me

- **All library code** in `needle-ai/src/` and the tests. The AI reviewed it, pointed out bugs
  and explained concepts, sometimes with a small example on an unrelated toy problem, and I
  wrote the fix. One exception: a single type annotation in `llmapi/openai.py` was shown to me
  as an example, and I applied the same pattern to the rest.
- **The architecture and its decisions:** the whiteboards, the ReAct flow, and the decisions
  recorded in the ADRs.
- **My explanations in `notes/`:** the "What it is" sections and the quiz answers.

## Written by AI

- **Project scaffolding:** the CI workflow, `.gitignore`, the notes template and the progress
  tracker.
- **The write-ups in `docs/design/`**, transcribed from my whiteboards and our design
  discussions. Each item is tagged as decided by me, or suggested by the AI. The design review
  (`review-01.md`) is an AI review of that design.
- **Parts of ADR 0001's wording**, rewritten at my request after we'd agreed on the decision.
- **In `notes/`:** the review, discussion-record and score sections.
- **First drafts of the READMEs and this file**, which I edited.

## Where AI changed the design

Some decisions came out of arguing with the AI rather than from me alone. For example,
block-based messages came from the design review, and an early draft of mine had adapters
talking to each other directly, which the review corrected: adapters only talk to the core.
It went both ways: some of the AI's suggestions were wrong and I argued them out (per-node
limits, Needle-generated tool-call ids). Where a decision came from the AI, the design docs
say so.

## Why I work this way

Needle is a learning project. Writing the code myself is the point. Using AI as a reviewer
gets me fast, specific feedback on the code and the design, the way a senior engineer's code
review would.
