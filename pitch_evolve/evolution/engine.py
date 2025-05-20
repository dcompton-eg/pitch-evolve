from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List
import os

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
    output_dir: str = "output"

    def evolve(self, generations: int = 1) -> List[str]:
        """Run prompt evolution for a number of generations."""
        os.makedirs(self.output_dir, exist_ok=True)
        for i in range(generations):
            scored = []
            for prompt in self.population:
                pitch = self.generator(prompt)
                feedback_result = self.evaluator(pitch, self.evaluation_prompt)
                feedback = getattr(feedback_result, "output", feedback_result)
                score = (
                    feedback.scores.average() if getattr(feedback, "scores", None) else 0.0
                )
                suggestion = getattr(feedback, "suggestion", "")
                scored.append((prompt, score, pitch, suggestion))

            avg_score = sum(s for _, s, _, _ in scored) / \
                len(scored) if scored else 0.0
            self.score_history.append(avg_score)

            scored.sort(key=lambda x: x[1], reverse=True)
            best_prompt, _, best_pitch, _ = scored[0]
            survivors = scored[: self.tournament_size]
            new_population = []

            for parent, _, _, suggestion in survivors:
                if suggestion and random.random() < self.mutation_rate:
                    new_population.append(
                        llm_mutate_prompt(parent, suggestion)
                    )
                else:
                    new_population.append(parent)

            while len(new_population) < len(self.population):
                parent, _, _, suggestion = random.choice(survivors)
                if suggestion and random.random() < self.mutation_rate:
                    new_population.append(
                        llm_mutate_prompt(parent, suggestion))
                else:
                    new_population.append(parent)

            self.history.append(new_population)
            self.population = new_population

            # write best prompt (after mutation) and best pitch
            prompt_path = os.path.join(
                self.output_dir, f"generation_{i + 1}_prompt.txt"
            )
            pitch_path = os.path.join(
                self.output_dir, f"generation_{i + 1}_pitch.txt"
            )
            best_prompt_text = new_population[0]
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(best_prompt_text)
            with open(pitch_path, "w", encoding="utf-8") as f:
                f.write(best_pitch)
        return self.population
