from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List

from pitch_evolve.evals import JudgeFeedback, llm_judge_score
from pitch_evolve.evolution.mutator import llm_mutate_prompt


GeneratorFn = Callable[[str], str]
EvaluatorFn = Callable[[str, str], JudgeFeedback]


@dataclass
class PromptEvolutionEngine:
    """Simple tournament-based prompt evolution."""

    population: List[str]
    generator: GeneratorFn
    evaluator: EvaluatorFn = llm_judge_score
    evaluation_prompt: str = "Score this pitch from 1-5 for creativity, persuasiveness, clarity, statistical grounding, and thematic relevance. Then provide a one-sentence suggestion for improving the prompt."
    tournament_size: int = 2
    mutation_rate: float = 0.1
    history: List[List[str]] = field(default_factory=list)
    score_history: List[float] = field(default_factory=list)

    def evolve(self, generations: int = 1) -> List[str]:
        """Run prompt evolution for a number of generations."""
        for _ in range(generations):
            scored = []
            for prompt in self.population:
                pitch = self.generator(prompt)
                feedback_result = self.evaluator(pitch, self.evaluation_prompt)
                # Access the JudgeFeedback object from AgentRunResult
                feedback = feedback_result.output
                score = feedback.scores.average() if feedback.scores else 0.0
                scored.append((prompt, score, feedback.suggestion))

            avg_score = sum(s for _, s, _ in scored) / \
                len(scored) if scored else 0.0
            self.score_history.append(avg_score)

            scored.sort(key=lambda x: x[1], reverse=True)
            survivors = scored[: self.tournament_size]
            new_population = [p for p, _, _ in survivors]

            while len(new_population) < len(self.population):
                parent, _, suggestion = random.choice(survivors)
                if suggestion and random.random() < self.mutation_rate:
                    new_population.append(
                        llm_mutate_prompt(parent, suggestion))
                else:
                    new_population.append(parent)

            self.history.append(new_population)
            self.population = new_population
        return self.population
