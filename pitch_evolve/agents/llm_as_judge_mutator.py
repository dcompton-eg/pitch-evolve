from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from pitch_evolve.agents.llm_as_judge import JudgeFeedback, PitchScores


class MutatorDeps(BaseModel):
    """Runtime options for the mutator (tweak here if you need)."""


class MutatedPrompt(BaseModel):
    """Agent output: the improved prompt text."""
    prompt: str = Field(..., description="A rewritten prompt ready for reuse")


_mutator_agent = Agent[MutatorDeps, MutatedPrompt](
    "openai:gpt-4.1",
    deps_type=MutatorDeps,
    output_type=MutatedPrompt,
    model_settings={
        "temperature": 0.8,
        "top_p": 0.9,
        "presence_penalty": 0.4,
    },
    instructions=(
        "You are an expert prompt-engineer.\n"
        "Your goal: improve the **prompt** that generated a community-pitch so "
        "future pitches score higher under the across dimensions: creativity, "
        "persuasiveness, clarity, statistical grounding, thematic relevanc, flow.\n\n"
        "You will receive:\n"
        "1. The current prompt text.\n"
        "2. The pitch that prompt produced.\n"
        "3. Structured judge feedback:\n"
        "   • per-dimension 0-100 scores\n"
        "Guidelines:\n"
        "• Analyse the feedback and identify concrete weaknesses across each of the dimensions.\n"
        "• Rewrite or extend the *prompt* so it explicitly nudges the generator "
        "to fix those weaknesses (e.g. ask for a statistic, demand a stronger "
        "call-to-action, or whatever you feel will increase the overall score across dimensions for the next round).\n"
        "• Preserve any good parts of the original prompt and all explicit requirements; do **not** rewrite the pitch itself.\n\n"
        "Return ONLY the NEW PROMPT in the `prompt` field of the JSON schema."
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
