def render_json(
    response_id: str,
    output_text: str,
    model: str,
    metadata: dict,
    temperature: float,
    input_tokens: int,
    output_tokens: int,
    reasoning: str = None,
    finish_reason: str = None,
) -> dict:
    return {
        "response_id": response_id,
        "model": model,
        "output_text": output_text,
        "finish_reason": finish_reason,
        "metadata": metadata,
        "temperature": temperature,
        "reasoning": reasoning,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens, 
        "total_tokens": input_tokens + output_tokens,
    }

class JSONStandardizer:
    @staticmethod
    def openai_response(response: dict, model: str) -> dict:
        usage = response.get("usage", {})
        incomplete = response.get("incomplete_details") or {}
        
        outputs = response.get("output", [])
        first_output = outputs[0] if outputs else {}

        return render_json(
            response_id=response.get("id", ""),
            output_text=response.get("output_text", ""),
            model=model,
            metadata=response.get("metadata", {}),
            temperature=response.get("temperature", 1.0),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            reasoning=first_output.get("reasoning"),
            finish_reason=incomplete.get("reason", "completed"),
        )