from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field

try:
    from pydantic_ai import Agent, RunContext
except Exception:  # pragma: no cover - optional dependency
    Agent = None
    RunContext = None

from pitch_evolve.evals.scoring import PitchScores, JudgeFeedback


class JudgeDeps(BaseModel):
    """Runtime options for the judge agent."""

    model_name: str = "gpt-4o"


if Agent is not None:
    _judge_agent = Agent[JudgeDeps, JudgeFeedback](
        "openai:gpt-4o",
        deps_type=JudgeDeps,
        output_type=JudgeFeedback,
        instructions=(
            "You evaluate community pitches. "
            "Return JSON with numeric 1-5 scores for creativity, persuasiveness, "
            "clarity, statistical grounding, and thematic relevance in a 'scores' object. "
            "Also provide a short improvement suggestion in the 'suggestion' field."
        ),
        model_settings={"temperature": 0},
    )
else:  # pragma: no cover - environment may lack pydantic_ai
    _judge_agent = None


def llm_as_judge(text: str, evaluation_prompt: str, model_name: str = "gpt-4o") -> JudgeFeedback:
    """Evaluate ``text`` using ``evaluation_prompt`` via the LLM judge agent."""

    query = evaluation_prompt.strip() + "\n" + text.strip()

    if _judge_agent is not None:
        try:
            return _judge_agent.run_sync(query, deps=JudgeDeps(model_name=model_name))
        except Exception:
            pass

    # Fallback to simple regex parsing of the evaluation prompt results
    numbers = list(map(int, re.findall(r"(\d)", text)))
    scores = PitchScores(*numbers[:5]) if len(numbers) >= 5 else None
    return JudgeFeedback(scores=scores, suggestion="")
