from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List

from pitch_evolve.evals import PitchScores, heuristic_score


GeneratorFn = Callable[[str], str]
EvaluatorFn = Callable[[str], PitchScores]


@dataclass
class PromptEvolutionEngine:
    """Simple tournament-based prompt evolution."""

    population: List[str]
    generator: GeneratorFn
    evaluator: EvaluatorFn = heuristic_score
    tournament_size: int = 2
    mutation_rate: float = 0.3
    history: List[List[str]] = field(default_factory=list)

    def evolve(self, generations: int = 1) -> List[str]:
        """Run prompt evolution for a number of generations."""
        for _ in range(generations):
            scored = []
            for prompt in self.population:
                pitch = self.generator(prompt)
                score = self.evaluator(pitch).average()
                scored.append((prompt, score))

            scored.sort(key=lambda x: x[1], reverse=True)
            survivors = [p for p, _ in scored[: self.tournament_size]]
            new_population = survivors.copy()

            while len(new_population) < len(self.population):
                parent = random.choice(survivors)
                new_population.append(self._mutate(parent))

            self.history.append(new_population)
            self.population = new_population
        return self.population

    def _mutate(self, prompt: str) -> str:
        """Apply a simple textual mutation to a prompt."""
        if random.random() > self.mutation_rate:
            return prompt
        mutations = [
            "Please include a recent statistic in your answer.",
            "Emphasize community benefits.",
            "Use a creative hook at the beginning.",
            "Conclude with a strong call to action.",
        ]
        addition = random.choice(mutations)
        if addition not in prompt:
            return f"{prompt.strip()} {addition}"
        return prompt
