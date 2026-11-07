# ADR 0001: Canonical message and response model

- **Status:** Draft
- **Date:** 2026-11-07
- **Author:** Adarsh

## Context

During my read-through on the Anthropic, OpenAI and Gemini docs, I saw that most of the information returned via API calls are similar, just in different shapes. Following that, it's in the best interest of the project to somehow standardize this into particular structures which would be validated via Pydantic.

**What Makes it Hard?**

The vision is to create a system that can work with different models, and different vendors as well. It should be able to share context, nodes, and even structures between them, truly beating vendor lock problems and create a perfect integration.

**What is wrong with the current code?**

The issue is there is no validation (Pydantic is required) and plus, it was created by the author (me) with a 'build as we go' mindset instead of deciding the architecture first. 

## Decision

1. We will have 3 layers of information in our core, which would be used to converse with adapters (AI calls, tool calls, structure exports, etc). The three layers being:
   1.1 Conversation Layer: Anything that the AI/node requires access to (generated text output, context, state, etc)
   1.2 Call Layer: Anything that requires information for making calls (let it be AI or tools), like Arguments and Parameters (this is where a lot of diversification would occur).
   1.3 Telemetry: Observability level information for tracking (input ids, latency, token usage, etc)
   Note: Token usage can also be an input level information for decision based nodes (end-decision specifically), but keeping a copy of it doesn't cause a problem. The core decision of whether it should be kept as a connector or a copy is not made yet, but both will be considered.
2. Blocks: A block is one typed piece of conversation content, whoever produced it. There are four types for now:
   - Text: {text}
   - ToolCall: {id, name, arguments, provider_id}, produced by the model when it wants a tool run
   - ToolResult: {id, tool_call_id, content, is_error}, produced by the tool adapter after running the call
   - Reasoning: {provider, model, data}, the model's opaque reasoning

   Each block carries a `type` tag, so the blocks form a Pydantic discriminated union. Content has a different structure for every vendor, so each adapter's translator normalizes it into an ordered list of blocks. So, a content result coming from a GenerateResult object is mostly giving you information like this:
   content: [ {type: "text", ...}, {type: "tool_call", ...}, {type: "reasoning", ...} ]
   The order is kept because providers interleave text, tool calls and reasoning in one reply, and reasoning has to stay in front of the tool call it led to when it is sent back to the same provider.

   Blocks live in exactly two places: the `messages` of a GenerateRequest and the `content` of a GenerateResponse. The requests and responses themselves are not blocks, and neither is the system prompt; everything on them other than messages and content is a plain field.

   Blocks are independent of the structure (ReAct, Reflection, etc). A new block type is only added when providers support a new kind of content (images, audio), never for a new structure. Data a structure needs to track for itself lives in state, not in blocks.
3. Message: A message is `{id, role, author, content}`, where `content` is an ordered list of blocks (see 2). "Who said it" is split into two fields, because they answer different questions:
   - `role` is the conversation slot every provider understands, and is exactly one of `user`, `assistant` or `tool`. Translators map it one-to-one onto each provider's roles. There is no `system` role; the system prompt is its own field on the request (see 5).
   - `author` is optional and says which part of Needle produced the message (a node or agent name, e.g. `planner`, `critic`). This is the play-script part: it lets a multi-agent run keep track of who said what, without inventing roles that providers don't have. Providers never see it unless the context builder decides to render it into the text; how that is rendered is a later decision.

   For example: the user's query is `role=user` with a Text block; the model asking for a tool is `role=assistant` with a ToolCall block; the tool's answer is `role=tool` with a ToolResult block.
4. Shared Core Types: This is so we can have a perfect integration of objects that are consumed toand fro of the core and adapters. So for example, our ToolCallRequest is generated via core, but consumed via tool adapter, while ToolCallReponse is generated via adapter, and consumed via core, so sharing core types (like ids) is important to keep track of what is a reponse to what.
5. GenerateRequest and GenerateResult: The shapes are more or less decided, but during testing, if things come up, they might change after the Vertical Slice implementation, but here's what it looks like for now:

   Generate Request:
      {generate_request_id, source{flow_id, flow_name, node_id, node_name}, system, messages, tools->optional, parameters:{model, temperature}}
   Generate Response:
      {generate_response_id, generate_request_id, provider_response_id, model, content, finish_reason, input_tokens, output_tokens, latency, metadata}

   The system prompt is its own field, not a block or a message, because providers place it differently and each translator puts it where its provider expects it. `messages` and `content` hold blocks (see 2), so reasoning is part of `content` as a Reasoning block.

   These objects are then exploded and routed to their respective layers.

6. Stop Reason: This Enum value requires special care in our system since we need to rename all of them into a common format. The exact conversion would depend on the provider, but we will have the following possiblities: {NULL (for providers who don't provide end reason), end_result_reached, token_contraint, tool_use, internal_error} 
7. Reasoning Blocks: These are mostly opaque and well, even though they would be present in state management and in the Observability parts as well, it would be mostly to make sure that the AIs reasoning can be tested by developers (since that's a core part of AI development). However, since different sources would give different reasonings, the conversation layer is not going to take forward one models reasoning to the other, and another model shall start another reasoning chain for itself instead.
8. IDs: To be honest, all objects should have an ID, makes tracking easy, retrieval too. Not every argument, but all objects that we have defined (so far, and even in the future, until and unless they are marked as an exception). Needle is going to create it, since we do not want to have a provider level clash of ids. It could be a concat of provider id (in needle) + provider's id, helping us track all responses better.
9. Serialization: Pydantic handles it well already, we don't have to think much about this.


## Alternatives considered

1. It was initially considered that all the information is returned via a single object instead of a 3 layer approach, but was soon scrapped out since their uses are different and it's always good to divide them by usage earlier so entire objects can directly be moved to places that they belong.

2. Tool calls via prompted JSON in the text (the original ReAct style), rejected because it's fragile to parse, its arguments aren't validated, and it can't make parallel calls

3. Content as separate lists per kind ({"texts": [], "tools": []}), rejected because it loses the order of the content, and every new kind of content would need a new key.


## Consequences

The main issue I still think is the reasoning chain, it would be great if we could come up with a solution which would help us carry forward older reasoning into the conversation, but that might break in the future in these cases:
1. If the model you switched to doesn't support reasoning at all.
2. If the reasoning object's structure is different -> (potentially solvable via another normalization)
3. If the reasoning object uses a specific language which only works for that model.

The adapter implementation is large as well, since every provider needs its own translator. Each response goes through two steps: translation into the canonical format inside the adapter, then routing of its parts (content, usage, telemetry) to their layers in the core. The plus point is seamless integration: every adapter speaks the same format to the core, so any model can pick up a conversation another one started. Adapters never talk to each other directly; everything goes through the core.

Streaming, images and voice is out of scope for now, but lets see if I get enough time to implement the same in the future.
