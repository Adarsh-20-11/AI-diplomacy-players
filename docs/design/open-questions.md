# Open questions for the reviewer

Please challenge these, with reasons and alternatives. Context is in
[architecture.md](architecture.md). Questions marked (A) are Adarsh's own; (C) came up in
review and have not been decided.

## Control flow and the compile step

1. **(A)** A compile step validates structure before running. But in an agent the model picks
   the next node at run time. What can a compiler really check (slots filled, no dangling
   edges, types) versus what stays dynamic? Is a compile step worth its cost here?

## Message format and model switching

2. **(A)** Is a canonical message model of Needle's own design enough to survive a model switch
   mid-conversation (Opus to Haiku, and across providers)? How should these be handled:
   - tool-call ids (does Needle own them, with adapters mapping?)
   - provider-private reasoning blocks and signatures (opaque and provider-tagged, dropped on
     a switch?)
   - system prompt placement
   - role-ordering rules
   - different tokenizers and context windows
   - lost prompt caching on a switch
   How far should the library promise to go: same provider only, or cross-provider?
3. **(C)** Should the canonical format be neutral, or deliberately shaped like one provider's
   (as some libraries do)? Tradeoffs?

## Specs, schemas and layers

4. **(A/C)** The spec sheet: one schema for both the response format and the graph structure,
   or two (spec = program, messages = run-time data)? How should the compiler relate to each?
5. **(C)** Are named, typed **slots** the right mechanism for "any structure with any
   customization"? What would a slot contract look like, and where does it break (for example
   a customization that assumes a node a given skeleton lacks)?
6. **(C)** The customization ladder (calling dependency) and the static/dynamic layers
   (execution dependency): are they one idea or two? Can they be reconciled in one diagram?

## Adapters, translators, context, state

7. **(A)** Translators sit with the adapters (ACL per external system). Should each provider own
   its translator beside its adapter, or stay in one central class? Which is easier to extend
   and to test as pure functions?
8. **(C)** Context: the adapter only connects; a context subsystem lives in the core and shapes
   history (trim, summarize, drop tool results). Should context shaping be pure functions over
   canonical messages? Where does the boundary between "fetching" and "shaping" sit?
9. **(A)** State lives in the core and a store persists it. What is the minimal store interface,
   what is the granularity of a checkpoint, and what must state satisfy to be serializable
   (message types as plain data)?

## API shape and scope

10. **(C)** Sync vs async: async-first with a sync wrapper, or both first-class? Agents that
    call tools in parallel lean async. Impact on the adapter design.
11. **(C)** Collapse generation and chat into one call taking a message list, with the
    prompt-plus-input form as a convenience? Today each provider has four near-duplicate methods.
12. **(C)** Streaming is deferred. What seam should the response type leave so it can be added
    without a redesign?
13. **(C)** Not yet designed: failure handling, step limits, token budgets, and how users test
    their own agents (is `FakeLLM` public API?). What is the minimum to settle before Phase 1
    is built, versus later?

## From the ReAct flow ([react-flow.md](react-flow.md))

16. **(A/C)** v2 of the flow feeds the user's input into the spec sheet. Should the spec stay a
    reusable agent definition (compile once, input goes into initial state at run time), or
    include the input and be rebuilt per request? Effects on export to the editor,
    checkpoint resume, and serialization.
17. **(C)** Message history: part of the state object, or of a separate context subsystem? The
    flow shows the loop reading and writing "Context" while "State management" is a side sink.
18. **(C)** Is the "do we need more steps?" node an LLM call or a deterministic check? Cost and
    stop-condition design (and a step limit).
19. **(C)** The pitch is pre-built then modified (eject), but the flow has no edge for
    customizing a pre-built structure. How is that path expressed?
20. **(C)** Per-node model choice: how does "AI choice" bind to individual nodes (slots), and
    what is the default when the user gives one model?
21. **(C)** Failure paths (tool error, model error, max steps), parallel tool calls, and
    ordering guarantees when appending a tool-call message and its result to history.

22. **(A/C)** Spec sheet format: a recursive nested structure (see the sketch in
    architecture.md section 2). How should cycles and conditional edges be expressed, how are
    typed inputs and outputs declared so chaining can be validated at compile time, and should
    the spec be the serialization of typed (Pydantic-style) models validated against a schema?

23. **(A/C)** Loops via input back-references with an End-Decider node (see "Loops and node
    types" in architecture.md): bindings or an explicit edge list? Class inheritance
    (Decider to End-Decider) or a small interface plus composition and a registry? Should the
    compiler reject unbounded cycles, and where do global limits (steps, tokens) live?

24. **(C)** Should the AI side expose a second, bounded operation ("choose among these options,
    return the choice and a confidence") alongside text generation, for deciders? Is it a
    second method on the AI port or a separate port, and how would ordinary LLMs implement it
    (constrained output) versus a specialist decision model?
25. **(A/C)** Where does each limit live: per-call output tokens as node config, cumulative
    budgets in the decider reading usage from state, and a hard engine ceiling? The canonical
    `Response` must carry token usage for this to work.

## Meta

14. Is any box or arrow in the diagrams in the wrong place for the hexagonal dependency rule
    (core depends on nothing outside)? The question Adarsh has not yet answered: "if `ReAct`
    is a box in the drawing, which arrows touch it?" (the ReAct execution flow in
    `react-flow.md` is meant to answer this).
15. What would you expect an ADR 0001 for Phase 1 to contain, given the above?
