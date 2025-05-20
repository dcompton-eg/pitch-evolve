from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class JudgeDeps(BaseModel):
    """Runtime options for the judge agent."""


class PitchScores(BaseModel):
    """Container for pitch evaluation scores."""

    creativity: int = Field(..., ge=0, le=100)
    persuasiveness: int = Field(..., ge=0, le=100)
    clarity: int = Field(..., ge=0, le=100)
    statistical_grounding: int = Field(..., ge=0, le=100)
    thematic_relevance: int = Field(..., ge=0, le=100)

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


_judge_agent = Agent[JudgeDeps, JudgeFeedback](
    "openai:gpt-4.1",
    deps_type=JudgeDeps,
    output_type=JudgeFeedback,
    instructions=(
        "You evaluate community pitches."
        "Evaluate the pitch, providing a score from 0-100 for each of the items."
    ),
    model_settings={"temperature": 0.1},
)


def llm_as_judge(pitch: str) -> JudgeFeedback:
    """Evaluate ``text`` using ``evaluation_prompt`` via the LLM judge agent."""

    return _judge_agent.run_sync(pitch, deps=JudgeDeps())
