from pitch_evolve.evolution import PromptEvolutionEngine
from pitch_evolve.evals import heuristic_score


def dummy_generator(prompt: str) -> str:
    return f"{prompt} Join our Go community of 1000 engineers."


def test_evolution_runs():
    engine = PromptEvolutionEngine(
        population=["Write a short pitch." for _ in range(3)],
        generator=dummy_generator,
        evaluator=heuristic_score,
    )
    result = engine.evolve(generations=2)
    assert len(result) == 3
