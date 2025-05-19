import argparse
from .agents.pitch_writer import pitch_writer_agent, PitchWriterDeps


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Go community pitch")
    parser.add_argument("prompt", help="Prompt text for the agent")
    parser.add_argument("--recency", default="m", help="Search recency filter")
    parser.add_argument("--max-results", type=int, default=3, help="Number of search results")
    parser.add_argument("--query-budget", type=int, default=5, help="Number of web queries allowed")
    args = parser.parse_args()

    deps = PitchWriterDeps(
        max_results=args.max_results,
        query_budget=args.query_budget,
        recency=args.recency,
    )
    result = pitch_writer_agent.run_sync(args.prompt, deps=deps)
    print(result.output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

