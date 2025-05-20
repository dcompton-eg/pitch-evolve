from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from pitch_evolve.agents.llm_as_judge import JudgeFeedback, PitchScores


class MutatorDeps(BaseModel):
    """Runtime options for the mutator (tweak here if you need)."""
    # put knobs like `max_tokens` etc. if required later


class MutatedPrompt(BaseModel):
    """Agent output: the improved prompt text."""
    prompt: str = Field(..., description="A rewritten prompt ready for reuse")


_mutator_agent = Agent[MutatorDeps, MutatedPrompt](
    "openai:gpt-4o",
    deps_type=MutatorDeps,
    output_type=MutatedPrompt,
    model_settings={
        # higher temperature encourages exploration; adjust to taste
        "temperature": 0.7,
        "top_p": 0.9,
        "presence_penalty": 0.4,
    },
    instructions=(
        "You are an expert prompt-engineer.\n"
        "Your goal: improve the **prompt** that generated a community-pitch so "
        "future pitches score higher under the rubric (creativity, "
        "persuasiveness, clarity, statistical grounding, thematic relevance).\n\n"
        "You will receive:\n"
        "1. The current prompt text.\n"
        "2. The pitch that prompt produced.\n"
        "3. Structured judge feedback:\n"
        "   • per-dimension 0-100 scores\n"
        "   • a short human-readable suggestion string\n\n"
        "Guidelines:\n"
        "• Analyse the feedback and identify concrete weaknesses.\n"
        "• Rewrite or extend the *prompt* so it explicitly nudges the generator "
        "to fix those weaknesses (e.g. ask for a statistic, demand a stronger "
        "call-to-action, etc.).\n"
        "• Preserve any good parts of the original prompt; do **not** rewrite "
        "the pitch itself.\n\n"
        "Return ONLY the new prompt in the `prompt` field of the JSON schema."
    ),
)


def llm_as_judge_mutator(
    feedback: JudgeFeedback,
    pitch: str,
    prompt: str,
) -> str:
    """
    Mutate the given `prompt` based on `feedback` about the `pitch`.

    Returns
    -------
    str
        The improved prompt text to be used in the next generation.
    """

    # Build a single string payload; you could switch to structured
    # function-calling if your infra supports it.
    payload = (
        "### ORIGINAL PROMPT\n"
        f"{prompt}\n\n"
        "### PITCH PRODUCED BY THE PROMPT\n"
        f"{pitch}\n\n"
        "### JUDGE FEEDBACK (JSON)\n"
        f"{feedback.model_dump_json(indent=2)}"
    )

    mutated = _mutator_agent.run_sync(payload, deps=MutatorDeps())
    return mutated.output.prompt
