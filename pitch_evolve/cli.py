from .evolution import PromptEvolutionEngine
from .agents.pitch_writer import pitch_writer_agent, PitchWriterDeps
import argparse
import copy

import matplotlib.pyplot as plt
import os
import logfire
from pathlib import Path


logfire.configure(token=os.getenv("LOGFIRE_API_KEY"))
logfire.instrument_openai()


def read_prompt_from_file(file_path: str) -> str:
    """Read a prompt from a file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    return path.read_text().strip()


def run_pitch(prompt: str, deps: PitchWriterDeps) -> None:
    """Generate a single pitch and print the JSON output."""
    if pitch_writer_agent is None:
        print({"topic": prompt, "output": prompt, "sources": {}})
        return

    result = pitch_writer_agent.run_sync(prompt, deps=deps)
    print(result.output.model_dump_json(indent=2))


def run_evolution(prompt: str, deps: PitchWriterDeps, generations: int, population: int) -> None:
    """Run prompt evolution and plot average scores."""

    def generate(p: str) -> str:
        if pitch_writer_agent is None:
            return p
        return pitch_writer_agent.run_sync(p, deps=copy.deepcopy(deps)).output.output

    engine = PromptEvolutionEngine(
        population=[prompt for _ in range(population)],
        generator=generate,
    )
    engine.evolve(generations=generations)

    plt.plot(range(1, len(engine.score_history) + 1),
             engine.score_history, marker="o")
    plt.xlabel("Generation")
    plt.ylabel("Average score")
    plt.title("Pitch quality over generations")
    plt.tight_layout()
    plt.savefig("evolution_scores.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pitch-Evolve CLI")
    sub = parser.add_subparsers(dest="command")

    pitch_cmd = sub.add_parser("pitch", help="Generate a single pitch")
    prompt_group = pitch_cmd.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text for the agent")
    prompt_group.add_argument("--prompt-file", help="File containing the prompt text")
    pitch_cmd.add_argument("--recency", default="m",
                           help="Search recency filter")
    pitch_cmd.add_argument("--max-results", type=int,
                           default=3, help="Number of search results")
    pitch_cmd.add_argument("--query-budget", type=int,
                           default=5, help="Number of web queries allowed")

    evo_cmd = sub.add_parser(
        "evolve", help="Evolve a prompt over multiple rounds")
    prompt_group = evo_cmd.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Base prompt text")
    prompt_group.add_argument("--prompt-file", help="File containing the base prompt text")
    evo_cmd.add_argument("--generations", type=int,
                         default=3, help="Number of evolution rounds")
    evo_cmd.add_argument("--population", type=int,
                         default=4, help="Population size")
    evo_cmd.add_argument("--recency", default="m",
                         help="Search recency filter")
    evo_cmd.add_argument("--max-results", type=int,
                         default=3, help="Number of search results")
    evo_cmd.add_argument("--query-budget", type=int,
                         default=5, help="Number of web queries allowed")

    args = parser.parse_args()

    if args.command is None:
        args.command = "pitch"

    deps = PitchWriterDeps(
        max_results=args.max_results,
        query_budget=args.query_budget,
        recency=args.recency,
    )

    # Determine the prompt text
    prompt = None
    if args.prompt_file:
        prompt = read_prompt_from_file(args.prompt_file)
    elif hasattr(args, 'prompt') and args.prompt:
        prompt = args.prompt
    
    if not prompt:
        parser.error("Either --prompt or --prompt-file must be provided")

    if args.command == "evolve":
        run_evolution(prompt, deps, args.generations, args.population)
    else:
        run_pitch(prompt, deps)


if __name__ == "__main__":
    main()
