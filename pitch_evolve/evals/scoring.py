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


def heuristic_score(text: str) -> PitchScores:
    """Return simple heuristic-based scores for a pitch.

    The heuristics are deliberately lightweight so they can run in
    constrained environments without external dependencies.
    """

    words = re.findall(r"\b\w+\b", text.lower())
    unique_ratio = len(set(words)) / max(len(words), 1)

    creativity = 5 if unique_ratio > 0.6 else 3 if unique_ratio > 0.4 else 1

    persuasive_patterns = r"\b(join|sign\s*up|be part|get involved|participate)\b"
    persuasiveness = 5 if re.search(persuasive_patterns, text, re.I) else 2

    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    clarity = 5 if avg_word_len <= 5 else 2

    statistical_grounding = 5 if re.search(r"\d", text) else 1

    thematic_relevance = (
        5
        if re.search(r"\bgo\b", text, re.I) or "community" in text.lower()
        else 2
    )

    return PitchScores(
        creativity=creativity,
        persuasiveness=persuasiveness,
        clarity=clarity,
        statistical_grounding=statistical_grounding,
        thematic_relevance=thematic_relevance,
    )


def llm_judge_score(text: str, evaluation_prompt: str, model_name: str = "gpt-4") -> Optional[PitchScores]:
    """Placeholder for LLM-as-a-judge scoring.

    This function is structured so that it can call an LLM to score the text
    according to the provided ``evaluation_prompt``. In offline environments it
    simply returns ``None``.
    """

    try:
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
        if len(numbers) >= 5:
            return PitchScores(*numbers[:5])
    except Exception:
        pass
    return None
