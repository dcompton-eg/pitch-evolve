from __future__ import annotations

from typing import Any

from pydantic import BaseModel
try:
    from pydantic_ai import Agent
except Exception:  # pragma: no cover - optional dependency
    Agent = None


class MutatedPrompt(BaseModel):
    """Structured output containing the mutated prompt."""

    prompt: str


if Agent is not None:
    _mutate_agent = Agent[
        Any,
        MutatedPrompt,
    ](
        "openai:gpt-4o",
        instructions=
        """You rewrite prompts. Given a base prompt and a suggestion, apply the suggestion to produce a new prompt. Only return the mutated prompt in the 'prompt' field.""",
        model_settings={"temperature": 0.2, "max_tokens": 512},
    )
else:  # pragma: no cover - environment may lack pydantic_ai
    _mutate_agent = None


def llm_mutate_prompt(prompt: str, suggestion: str) -> str:
    """Mutate ``prompt`` using ``suggestion`` via an LLM.

    Falls back to simple concatenation if the LLM call fails.
    """
    query = (
        "Base prompt:\n" + prompt.strip() + "\n\nSuggestion:\n" + suggestion.strip()
    )
    if _mutate_agent is not None:
        try:
            result = _mutate_agent.run_sync(query)
            return result.prompt
        except Exception:
            pass
    # Offline fallback
    if suggestion and suggestion not in prompt:
        return f"{prompt.strip()} {suggestion.strip()}"
    return prompt
