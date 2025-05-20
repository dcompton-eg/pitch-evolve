from __future__ import annotations

import re
from typing import Optional


from pydantic import BaseModel, Field


class PitchScores(BaseModel):
    """Container for pitch evaluation scores."""

    creativity: int = Field(..., ge=1, le=5)
    persuasiveness: int = Field(..., ge=1, le=5)
    clarity: int = Field(..., ge=1, le=5)
    statistical_grounding: int = Field(..., ge=1, le=5)
    thematic_relevance: int = Field(..., ge=1, le=5)

    def average(self) -> float:
        """Return the average score across all dimensions."""
        return (
            self.creativity
            + self.persuasiveness
            + self.clarity
            + self.statistical_grounding
            + self.thematic_relevance
        ) / 5.0


class JudgeFeedback(BaseModel):
    """Scores and an optional prompt improvement suggestion."""

    scores: Optional[PitchScores] = None
    suggestion: str = ""


def llm_judge_score(
    text: str, evaluation_prompt: str, model_name: str = "gpt-4o"
) -> JudgeFeedback:
    """Score ``text`` using the ``llm_as_judge`` agent.

    Parameters
    ----------
    text:
        The candidate pitch to evaluate.
    evaluation_prompt:
        Instructions describing how the pitch should be scored.
    model_name:
        Optional model name override for the underlying LLM.

    Returns
    -------
    JudgeFeedback
        Structured scores and an improvement suggestion.
    """

    try:
        from pitch_evolve.agents.llm_as_judge import llm_as_judge

        return llm_as_judge(text, evaluation_prompt, model_name=model_name)
    except Exception:  # pragma: no cover - optional network call
        pass

    return JudgeFeedback()
