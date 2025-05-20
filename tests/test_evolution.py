import os
os.environ.setdefault("OPENAI_API_KEY", "sk-test")

from pitch_evolve.evolution import PromptEvolutionEngine
from pitch_evolve.evals import JudgeFeedback, PitchScores


def dummy_generator(prompt: str) -> str:
    return f"{prompt} Join our Go community of 1000 engineers."


def test_evolution_runs():
    def dummy_evaluator(text: str, prompt: str) -> JudgeFeedback:
        return JudgeFeedback(
            scores=PitchScores(
                creativity=1,
                persuasiveness=1,
                clarity=1,
                statistical_grounding=1,
                thematic_relevance=1,
            ),
            suggestion="Add a stat.",
        )

    engine = PromptEvolutionEngine(
        population=["Write a short pitch." for _ in range(3)],
        generator=dummy_generator,
        evaluator=dummy_evaluator,
        mutation_rate=1.0,
    )
    result = engine.evolve(generations=1)
    assert len(result) == 3
    assert any("Add a stat." in p for p in result)
    assert engine.score_history == [1.0]

    # verify output files were written
    with open("output/generation_1_prompt.txt", "r", encoding="utf-8") as f:
        prompt_text = f.read()
    with open("output/generation_1_pitch.txt", "r", encoding="utf-8") as f:
        pitch_text = f.read()
    assert "Add a stat." in prompt_text
    assert "Join our Go community" in pitch_text

