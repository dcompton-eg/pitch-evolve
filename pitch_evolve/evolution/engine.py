from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List
import os

from pitch_evolve.agents.llm_as_judge import JudgeFeedback, llm_as_judge
from pitch_evolve.agents.llm_as_judge_mutator import llm_as_judge_mutator
from pitch_evolve.evolution.mutator import llm_mutate_prompt


GeneratorFn = Callable[[str], str]
EvaluatorFn = Callable[[str], JudgeFeedback]


@dataclass
class PromptEvolutionEngine:
    """Simple tournament-based prompt evolution."""

    population: List[str]
    generator: GeneratorFn
    evaluator: EvaluatorFn = llm_as_judge
    tournament_size: int = 2
    mutation_rate: float = 0.5
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
                feedback_result = self.evaluator(pitch)
                feedback = getattr(feedback_result, "output", feedback_result)
                score = (
                    feedback.scores.average() if getattr(feedback, "scores", None) else 0.0
                )
                scored.append((prompt, score, pitch, feedback))

            avg_score = sum(s for _, s, _, _ in scored) / \
                len(scored) if scored else 0.0
            self.score_history.append(avg_score)

            # log all of the scores for this generation:
            for z in scored:
                print(f"score:{z[1]}, prompt:{z[0]}\n")

            scored.sort(key=lambda x: x[1], reverse=True)
            best_prompt, _, best_pitch, _ = scored[0]
            survivors = scored[: self.tournament_size]
            new_population = [best_prompt]  # include best prompt

            # TODO: implement elitism
            for parent_prompt, _, parent_pitch, parent_feedback in survivors:
                if random.random() < self.mutation_rate:
                    new_population.append(
                        llm_as_judge_mutator(
                            parent_feedback, parent_pitch, parent_prompt)
                    )
                else:
                    new_population.append(parent_prompt)

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
