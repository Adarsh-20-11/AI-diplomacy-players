# Design review 01 (November 2026)

Reviewer: Claude Opus 5.5, in the same session that transcribed this pack. Many **[suggested]**
items in the pack came from that session; they are judged here on their merits, and a few are
reversed. Nothing in this file is a decision until Adarsh records it in an ADR.

## What is done well

- **Designing from the consumer.** Reading three providers and concluding "same information,
  different shapes" was the right takeaway. The design asks what an agent needs, not what each
  SDK returns.
- **Canonical history translated at the edge, stateless LLM objects, model chosen per node.**
  This is the foundation that makes the pitch possible. It is correct, and many libraries get it
  wrong by storing history in provider format.
- **Build time versus run time.** Separating "assemble and validate" from "execute" is right, and
  the idea of refusing an unbounded cycle at build time is a real differentiator.
- **Per-node limits.** Adarsh pushed back on a single global budget and was right. Budgets are a
  per-task policy; a global ceiling is only a seatbelt.
- **Deciders as interchangeable strategies, wide not deep.** `LLMEndDecider` and `DetEndDecider`
  behind one role is a sound shape.
- **Process.** Phase 0 was done properly (strict mypy, ruff, CI, hand-written), the design was
  drawn before code, and decisions are written down. That is the habit reviewers look for.

## The main risk: designing too far ahead of working code

There are 25 open questions spanning phases 1 to 7 (compiler, spec format, registry, decision
operation, editor import/export), while the code has two provider helpers and a 5-line ReAct
placeholder. Several questions (history ordering, parallel tool results, what state really
holds, where stopping is decided) are much easier to answer after one loop has run for real.
The recommendation in "Changes before Phase 1" below addresses this.

## Question by question

### 1. Is a compile step worth it?

Yes, kept small. It can check structure, not the path taken:

- start and end exist; every node reachable from start and able to reach end
- every cycle passes through a decider with a bound
- every node type exists in the registry; every slot is filled
- declared input and output types line up where nodes or agents connect
- every chosen model has an installed adapter

What stays dynamic: which branch is taken, how many iterations, tool argument validity, token
usage. Cost is small because this is graph analysis on a few dozen nodes at construction time.
**Change:** call it a *build* or *validate* step, not a compiler. "Compiler" invites code
generation and optimization, which you do not need. Output: a validated, immutable graph.

### 2. Can a canonical model survive a model switch?

Yes for the content that matters, if you promise the right thing.

- **Tool-call ids.** Keep the id string in the canonical tool call. Adapters generate one when a
  provider does not supply it and sanitize format if another provider rejects foreign ids (check
  each provider's id rules). The invariant the core enforces: every tool result references a
  tool call earlier in the same history. A full id-mapping table is only needed if sanitizing is
  not enough.
- **Reasoning blocks.** Store them opaque, tagged with provider and model. Replay them to the same
  provider, drop them on a switch. Careful: some providers require these blocks to be sent back
  *within* a tool-use loop (I believe Anthropic does when extended thinking is on; verify in the
  docs). So "drop" applies only when the provider changes, never mid-loop on the same one.
- **System prompt.** A separate field on the request, not a message role. Two of three providers
  take it separately, and a separate field removes "system message in the middle" ambiguity.
- **Role ordering.** The canonical model allows anything semantically valid; translators enforce
  each provider's rules (merging consecutive same-role messages and so on).
- **Tokenizers and context windows.** Not portable. Keep per-model metadata (window, max output)
  and use estimates for context shaping; exact counts are an optional adapter capability.
- **Prompt caching.** Accept the loss on a switch and document it.

**The promise:** switching within one provider is supported. Across providers, text, tool calls,
tool results (and images later) carry over; provider-private extras are dropped, and an
observability event says so. That is honest and achievable.

### 3. Neutral or provider-shaped?

Neutral, block-based: a message is a role plus a list of typed content blocks (text, tool call,
tool result, reasoning, later image). This is the most general form, so the others map onto it
easily. It resembles Anthropic's shape because that shape is general, not because you are copying
a vendor. Copying OpenAI's Chat Completions shape would tie you to an API that OpenAI itself is
moving away from (the Responses API); provider shapes change, your model should not have to.

### 4. One schema or two?

Two schemas, one family. Spec (agent definition, versioned, exported) and messages (run-time data
in state) change at different rates and live in different places. Both are typed models in the
same system (for example Pydantic). The spec may *reference* message types, for example as the
declared input type, but never contains messages.

### 5. Are slots the right mechanism?

Yes, for one kind of customization. A slot is a node name, a role interface (reasoner, actor,
decider), a default implementation and its config. Filling a slot is ladder level 1. Adding a
reflection step changes the topology, which is a graph edit (levels 2 and 3), not a slot fill.
So there are two mechanisms, and the build step validates both. A customization that names a slot
the skeleton lacks is a build error naming the slot. Not needed before Phase 4; Phase 1 only needs
the LLM injected into nodes.

### 6. Ladder and layers: one idea or two?

Two, and they should not be merged. **Change (reversing the pack's framing):** retire the nested
"static core and dynamic layers" diagram. It was useful thinking, but the ReAct flow already
shows build versus run, and the nested rectangles add a third vocabulary (structure, AI-call,
context layers) that does not map to code. Keep three diagrams, each answering one question:

| Diagram | Question |
|---|---|
| Hexagon | where does code live, and who may depend on whom |
| Flow | what happens at build time and at run time |
| Ladder | how deep does a user have to go |

### 7. Where do translators live?

Beside each adapter, one package per provider (`providers/openai/client.py` and `translate.py`).
The deciding reason is **optional dependencies**: a central class with a method per provider
imports every SDK, so a user who installed only one provider gets an `ImportError`. Per-provider
packages line up with extras (`needle[openai]`). Translators are pure functions (request out,
response in), tested against recorded JSON fixtures of real responses.

### 8. Context: fetching versus shaping

Fetching is a port (I/O). Shaping lives in the core. The important refinement: **shaping produces
the view sent to the model; it never edits the stored history.** Full history stays in state as
the source of truth; each call gets a trimmed or summarized projection. Then a switch to a model
with a bigger window can use more history, and checkpoints keep everything. Summarizing needs an
LLM, so a shaping function takes one injected; it is not pure, but it is still core logic.

### 9. State store

Minimal interface: save a snapshot for a run and step, load a run's latest (or a given) step,
list a run's steps. Checkpoint after each node finishes; that is the natural resume point, never
mid-call. State must be plain data: no clients, sockets or functions (refer to them by name), and
a schema version. Phase 1 needs only one thing from this: a test that message types round-trip
through JSON.

### 10. Sync or async?

Async-first, with a sync wrapper only at the public edge (`run` and `arun`). Parallel tool calls,
concurrent nodes and streaming are all async-native, and retrofitting async later is painful
because it spreads through every call site. Adapters implement async only. Note: a sync wrapper
built on `asyncio.run` fails inside an already running event loop (for example Jupyter), so
document `arun` for that case. Async is a real learning cost; it is worth paying now.

### 11. Collapse generation and chat?

Yes, clearly. One method per adapter: generate from a request (messages, system, tools, params)
to a response. The prompt-plus-input form becomes a helper outside the adapters, or disappears.
Combined with item 10, four methods per provider become one. This is the biggest simplification
available.

### 12. Streaming seam

Design the response as what a stream would add up to: content blocks, stop reason, usage. Do not
put anything in it that only a non-streaming call can know. Later, a separate streaming method
yields events, and a helper folds events into a response. Nothing to build now.

### 13. Minimum to settle before Phase 1

- **Error hierarchy** with a `retryable` flag (rate limit, timeout, server error retryable; auth
  and invalid request not). Retries in Phase 1 depend on it.
- **`FakeLLM` as public API** (for example `needle.testing`): scripted responses in order, records
  the requests it received. Users testing their agents need it as much as you do.
- **Usage in the response.** Budgets come later; the data must exist now.

Step limits and budgets themselves: Phase 3 and 4.

### 16. User input in the spec?

Input *schema* in the spec, input *value* at run time. Adarsh's point that every run has an input
(from a user or an upstream agent) is right, and it argues for declaring the input type in the
spec. Putting the value there makes the spec per-request and breaks compile-once, export, and
chaining (agent B's definition would depend on agent A having already run).

### 17. History: state or context?

State, as the source of truth. Context is the per-call view (item 8). This resolves the flow's
"Context" box versus "State management" sink: the loop reads and writes state, and context
shaping produces what each model call sees.

### 18. Is the stop check an LLM call?

Deterministic by default: stop when the model's reply contains no tool calls (that is how
tool-calling models signal completion), plus a maximum iteration count. This changes the mental
model of the flow: **one LLM call per iteration**. The reasoning node is the model call; its reply
holds both the thought and the chosen action. The action node executes the tool calls from that
reply (no LLM). The question node checks the reply (no LLM). An LLM-judged decider is opt-in, and
checking answer quality with a second model is really the Reflection pattern, a separate prebuilt.

### 19. The eject path

The prebuilt exposes its graph; editing returns a new spec, which is rebuilt and revalidated.
Treat built graphs as immutable and edits as "copy with changes", so editing one agent never
mutates a shared prebuilt. Phase 4.

### 20. Per-node model choice

Agent-level default plus per-slot override, resolved and validated at build time (model known,
adapter installed). Stateless LLM objects make sharing one across nodes safe. Agrees with the pack.

### 21. Failures, parallel calls, ordering

- **Tool errors go back to the model** as a tool result marked as an error, not raised. The model
  can often recover. Raise only for infrastructure failures.
- **Model errors:** retry the retryable ones with backoff; raise the rest.
- **Parallel calls:** a reply may contain several tool calls. Run them concurrently and record the
  results in the order of the calls, all after the assistant message and before the next one
  (some providers require all results in a single following message; translators handle that).
- **Ordering guarantee:** nodes return updates; one place (the engine) applies them to state.
  A single writer is what guarantees order. Look up "reducers" in the LangGraph docs.

### 22 and 23. Spec format, loops, node classes

**Revised view.** Adarsh's back-reference bindings do express a loop; the earlier objection that
a tree cannot was wrong. But the real choice is not syntax, it is the paradigm:

- **Shared-state graph** (LangGraph style): nodes read the whole state and return updates. What is
  left to specify is control flow, which edges express. Natural for agents, because history must
  be shared and model switching depends on it.
- **Dataflow** (n8n style): each node's output is piped to the next node's input. Natural for
  pipelines and chaining. Bindings express it.

Adarsh's design uses both instincts: shared history (state) inside the loop, n8n-style chaining
between agents. They combine cleanly: **inside an agent, a shared-state graph with explicit
edges** (conditional edges come from deciders); **between agents, dataflow** with typed inputs and
outputs, which the build step checks. That also gives item 16 its home. This deserves its own ADR
before Phase 3.

Node classes: a small node interface plus a registry, with wide and shallow class families, is
fine. The spec names node types through the registry, so custom classes can be exported. The
build step rejects unbounded cycles; a high engine-level ceiling stays as a seatbelt.

### 24. A bounded "choose" operation

Good idea, not now. If added, make it a capability on the model port rather than a separate port:
"choose among these options, return the choice and a confidence". Any LLM adapter can implement
it through structured output; a specialist decision model (Jev was mentioned, with unverified
claims) would be an adapter that supports only this capability. Revisit when deciders exist
(Phase 3 and 4).

### 25. Where limits live

Agree with the split in the pack: per-call output caps in node config (set before the call),
cumulative budgets in deciders reading usage from state, and a high engine ceiling as a seatbelt.
It requires the engine to accumulate each call's usage into state.

### 14. Hexagonal dependency rule

The diagrams are mostly consistent. Two real findings:

- **The current code violates the rule.** `needle/ai/wrapper/llm.py` imports
  `needle.llmapi.openai` and `needle.llmapi.gemini` directly, so the core depends on concrete
  adapters. It should depend on the port only, with the provider chosen at the edge (a registry or
  factory, sometimes called the composition root).
- **The flow mixes steps and ports.** "State management" and "Observability" appear as steps
  after "Execution"; they are ports used by every step. Fine for a sketch; worth fixing in the
  final diagram.

Which arrows touch ReAct: the AI port (the reasoning call, and an LLM decider if used), the tool
port (the action node), state (every node reads it and returns updates), and observability
(events from every node). ReAct does not touch the state store directly; the engine checkpoints.

### 15. ADR 0001 contents

See "ADRs needed first" below.

## Changes before Phase 1

1. **Build a thin vertical slice first.** Phase 1 delivers: the canonical message and response
   types; one async `generate` per adapter; translators beside adapters; the error hierarchy;
   `FakeLLM`; and a **hand-written ReAct loop** as a plain function of about 50 lines, using one
   tiny tool and running on `FakeLLM` and one real provider. No build step, spec format or
   registry yet. This is a change to the roadmap (ReAct was Phase 4). The reason: the graph runtime
   in Phase 3 should be designed from a loop that has run, and the hand-written loop becomes the
   regression baseline the Phase 4 graph-based ReAct must match. The cost is some code that gets
   replaced, which is acceptable for a learning project.
2. **Fix the dependency violation** in `llm.py` (core importing concrete adapters).
3. **Collapse the four methods per provider into one async method** (items 10 and 11).
4. **Retire the nested layers diagram**; keep hexagon, flow and ladder.
5. **Rename "compiler" to a build or validate step.**
6. **Write the trace.** With items 17, 18 and 21 above, it should now be quick, and it is the
   check that the design holds.

## ADRs needed first

Before Phase 1:

- **0001 Canonical message and response model.** Context (providers converge; switching models is
  a requirement). Decision: block-based messages; roles; system prompt as a separate field; tool
  call (id, name, arguments) and tool result (call id, content, error flag); reasoning blocks
  opaque and provider-tagged; response (content blocks, stop reason enum, usage, model, raw
  original); serializable typed models. Explicitly out of scope: streaming, images. Consequences:
  what is lost across providers. Alternatives considered: OpenAI-shaped, plain dicts or
  TypedDicts, dataclasses versus Pydantic.
- **0002 Provider port.** One async `generate`, sync wrapper policy, translators per provider,
  package layout and optional dependency extras.
- **0003 Error model.** Hierarchy, the `retryable` flag, tool errors returned to the model.

Before Phase 3:

- **0004 Shared-state graph inside agents, dataflow between agents** (items 22 and 23), history in
  state and context as a per-call view (items 8 and 17).
- **0005 The build step:** what it validates, and the bounded-cycle rule.

Before Phase 4: slots and the customization ladder.

## What is missing

- **A test strategy for adapters.** `FakeLLM` covers the core. Adapters also need recorded
  response fixtures for translators, one shared contract test suite that every adapter must pass,
  and a few live tests that are skipped by default (they need keys and cost money; never run them
  on pull requests).
- **Tools versus context sources overlap.** "Context greps" could be a tool the model chooses to
  call, or context the framework injects before a call. Both are valid; decide which is which.
- **Tool safety.** Tools touch the external world: sandboxing, timeouts, and possibly human
  approval for dangerous ones. Phase 2, but it affects the tool port's shape.
- **Human-in-the-loop interrupts** (pause, approve a tool call, resume). It pairs naturally with
  checkpointing and is a common requirement.
- **Model metadata.** Context window, supported features (tools, images), and prices for cost
  tracking. Context shaping, the build step and budgets all need it.
- **Public API and versioning.** Which names are public, and what a breaking change is (semver).
  Matters once anyone else imports Needle.
- **The package name.** `needle` is almost certainly taken on PyPI; check before it is baked into
  imports everywhere.
