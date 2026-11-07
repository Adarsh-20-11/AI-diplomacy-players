---
tags: [concept, architecture]
phase: 3
status: draft
score: 3
last_reviewed: 2026-11-07
---

# Build Time vs Run Time

## What it is (my own words)
Well, this has mostly to do with stuff that is static vs dynamic. Static items like the core of each node in my case have to be something that don't change much, and would hence, be generated during the build time itself, while the dynamic parts which would change with user input or situations would be generated while run time (customizable properties, AI type, etc).

**Quiz answer (2026-11-07):**
a. We can catch errors that are structural in nature before the execution ever happens, saving us tokens. In our case, finalizing the structure is a strong build phase catch that we do, to see if there are any orphans (as a warning) or if every structure has a start and an end, whether the spec sheet is accurate for each node/agent in the structure, if any required arguments are missing, etc. So basically, build time creates a graph out of the spec sheet, and if in that process anything fails, it raises that up as an issue.
So 2 you say huh, I would 1-> Saves time, you catch errors early, 2-> saves money, saves you tokens which might have resulted in failed runs.

b. per node model choice-> build time
    user's question-> build time (but depends on the type of agent as well. A chatbot would be both)
    Number of loop iterations -> While the max loops might be decided at build time, the actual number of loops is decided at run time

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), section 2
- [docs/design/react-flow.md](../docs/design/react-flow.md): left of the spec sheet is build, right is run
- [docs/design/review-01.md](../docs/design/review-01.md), Q1, Q6, Q16

## Tradeoff / why I chose this
Because, well, I thought that to make things easier for everyone, I needed a layer of abstraction (not the main reason but it is one of them) where all the core executions of the LLM happen. These are more structural level stuff like the way our engine compiles the spec sheet and how the AI execution happens, how the calls happen, because that level of architecture doesn't need to be shown to the user.
The second reason is, well, probably a more important one, it's because we needed something as a core spec that all our architectural components could use to interact with each other irrespective of what AI is being used, or what structure it is. THAT is going to be our core compiler that works during build time, while the rest occurs while run time.

## Related
- [[Graph Validation]]
- [[Shared-State Graph vs Dataflow]]
- [[Progressive Disclosure]]

## Quiz myself
1. What can a build step check, and what can only be known at run time in an agent?
2. Define-and-run vs define-by-run: which is Needle, and what does that choice cost?
3. Why should the user's input be a schema in the spec but a value at run time?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your idea, reached independently: a static core and dynamic layers ("things that can change
  depending on connector I/O and user interactions").
- Known names for it: define-and-run vs define-by-run (old TensorFlow vs PyTorch), staged
  computation, LangGraph's `.compile()`.
- You argued every execution needs an input, from a user or an upstream agent. Review 01, Q16:
  declare the input schema in the spec, pass the value at run time.
- Review 01: retire the nested layers diagram; call the "compiler" a build or validate step.

## Reviews (Claude)
### 2026-11-07, score 2/5
- Correct: the split itself, some things fixed before running and others depending on input. The static/dynamic idea is yours and it's a good one.
- Wrong or missing: the note never says what the split buys you: structural errors caught before any tokens are spent, and one build serving many runs. "AI type" is listed as run time, but per-node model choice is resolved and validated at build time; the input *value* is what's run time. The build step validates and freezes structure; it doesn't generate node cores. Both reasons in the tradeoff describe other concepts: hiding internals from users is encapsulation, and "a core spec all components use irrespective of AI or structure" is the canonical data model, which is run-time data, not the build step.
- Corrected version: build time turns a spec into a validated, immutable graph (structure, slots, models and types checked) before anything runs. Run time executes it with an input, and that's where the path, the number of iterations and the token usage get decided. The benefit is that errors surface early and cheaply, and one built agent serves many runs.

### 2026-11-07, quiz, score 3/5
- Question: (a) Two concrete benefits of a separate build step. (b) Build or run time: per-node model choice, the user's question, the number of loop iterations?
- Correct: structural errors caught before execution, saving tokens and time; a good list of what gets checked; "build creates a graph out of the spec sheet". Per-node model at build time, and loops (maximum at build, actual count at run) are exactly right. The note's "AI type at run time" mistake is fixed.
- Wrong or missing: your two benefits are one benefit (catching errors early) counted twice. The second, distinct one is build once, run many times, plus the built graph can be exported. The user's question is always run time: the spec declares the input *type*, and the value arrives with each run. That's how one built chatbot answers many questions.
