from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class PitchScores:
    """Container for pitch evaluation scores."""

    creativity: int
    persuasiveness: int
    clarity: int
    statistical_grounding: int
    thematic_relevance: int

    def average(self) -> float:
        """Return the average score across all dimensions."""
        return (
            self.creativity
            + self.persuasiveness
            + self.clarity
            + self.statistical_grounding
            + self.thematic_relevance
        ) / 5.0


@dataclass
class JudgeFeedback:
    """Scores and an optional prompt improvement suggestion."""

    scores: Optional[PitchScores] = None
    suggestion: str = ""


def llm_judge_score(
    text: str, evaluation_prompt: str, model_name: str = "gpt-4"
) -> JudgeFeedback:
    """Placeholder for LLM-as-a-judge scoring.

    This function is structured so that it can call an LLM to score the text
    and provide a prompt improvement suggestion according to the provided
    ``evaluation_prompt``. In offline environments it simply returns empty
    feedback.
    """

    try:  # pragma: no cover - optional network call
        import openai  # imported lazily so tests do not require it

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": evaluation_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        content = response.choices[0].message.content
        numbers = list(map(int, re.findall(r"(\d)", content)))
        suggestion_match = re.search(r"suggestion:\s*(.*)", content, re.I)
        scores = PitchScores(*numbers[:5]) if len(numbers) >= 5 else None
        suggestion = suggestion_match.group(1).strip() if suggestion_match else ""
        return JudgeFeedback(scores=scores, suggestion=suggestion)
    except Exception:
        pass

    return JudgeFeedback()
