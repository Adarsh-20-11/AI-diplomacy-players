---
tags: [concept, architecture]
phase: 3
status: draft
score: 4
last_reviewed: 2026-11-07
---

# Shared-State Graph vs Dataflow

## What it is (my own words)
Okay, the reason why I needed to add this is because I needed a way to enforce structure. A structure of the entire flow needs to be decided before you go into compilation, and well, you had an option to go with a graph, or go with a tree. Why I went with a tree instead of a graph was because:
1. I needed more than just the node information inside a structure. Global contraints of all the nodes in particular.
2. The other option was to start with a tree and inside the node definitions, turn it into a graph, but the problem with that would be that some nodes might require a hierarchical based definition, like for example, a reasoning node using a planner node within it, so it doesn't act as a dependency, but rather a tool call (action).

**Quiz answer (2026-11-07):**
That's through state memory. So basically, inside a ReAct agent, all nodes maintain a single state graph, and the same state is basically updated by every node and the edges decide where the agents go next.. However, when it become inter-agent communication (I sometimes get confused between inter and intra so I am making it clear, between 2 different agents), the communication happens via a dataflow level (as in the states and history is forwarded to the new agent so it can make use of it) and well, although in some cases it may require some decisions on what must run next, but that depends on the output of the previous node and comes in part with the chaining.

## Where it lives in needle
- [docs/design/architecture.md](../docs/design/architecture.md), "Loops and node types"
- [docs/design/review-01.md](../docs/design/review-01.md), Q22 and Q23
- ADR 0004 (before Phase 3)

## Tradeoff / why I chose this


## Related
- [[Build Time vs Run Time]]
- [[History vs Context View]]
- [[Graph Validation]]

## Quiz myself
1. In a shared-state graph, what do edges express that bindings would express in a dataflow design?
2. Why does a ReAct loop fit a shared-state graph?
3. Where does dataflow fit in Needle?

## Discussion record (Claude)
<!-- What was discussed and decided, with sources. Not an explanation: write that above. -->
- Your proposal: loops through input back-references (node1 takes node3's output, seeded with
  "redo" for the first pass). It works; the earlier claim that a tree cannot express a loop was wrong.
- Review 01: the real choice is the paradigm, not the syntax. Inside an agent, a shared-state
  graph with explicit edges, where deciders produce the conditional edges. Between agents,
  dataflow with typed inputs and outputs (n8n-style chaining).
- Your recursive spec: a node can contain a whole structure, giving agents as nodes.

## Reviews (Claude)
### 2026-11-07, score 1/5
- Correct: nothing on this note's concept, but the text has good points about the *spec format*: structure decided before building, global constraints across nodes, and hierarchy (a reasoning node using a planner inside it, as a call rather than a dependency), which is composition, i.e. subgraphs.
- Wrong or missing: the note answers "tree or graph for the spec format", which is a different question. Shared-state vs dataflow is about how data moves at run time: either every node reads one shared state and returns updates, with edges choosing who runs next, or each node's output is passed directly as the next node's input. Review 01 suggested shared state inside an agent and dataflow between agents. On the tree argument: global constraints can be top-level fields in any format, and a graph can nest (a node that contains a graph), so tree vs graph isn't a forced choice. Consider moving this text into a new "Spec Sheet Format" note, where it's on topic.
- Corrected version: in a shared-state graph, nodes communicate only through one state object: each reads it and returns updates, and edges decide what runs next. In dataflow, nodes communicate by passing outputs directly into the next node's inputs. Shared state suits loops over a common history (agents); dataflow suits pipelines and chaining agents together.

### 2026-11-07, quiz, score 4/5
- Question: In a ReAct loop, how does information get from the reasoning node to the action node? Both ways it could work, and which Needle uses inside vs between agents, and why.
- Correct: inside an agent, one shared state that every node updates, with edges choosing what runs next; between agents, dataflow, chained by the previous output. A big step up from the note.
- Wrong or missing: between agents, what flows is the previous agent's *output* (its typed result), not its whole state and history. Each agent's run keeps its own state; that isolation is what stops histories nesting inside each other. The "why" wasn't given: shared state inside because every node works on one history (and model switching depends on it); dataflow between because agents stay decoupled and the build step can check one agent's output type against the next one's input type. (Intra = within, inter = between.)
