from __future__ import annotations
from typing import Dict, Any, Optional

from pitch_evolve.tools.web_search import web_search

try:
    from pydantic_ai import Agent, RunContext
except Exception:  # pragma: no cover - optional dependency
    Agent = None
    RunContext = None
from pydantic import BaseModel, Field
from pitch_evolve.tools.file_tools import write_file
from pitch_evolve.prompts import utils as prompt_utils


class PitchWriterOutput(BaseModel):
    topic: str = Field(..., description="A short description of the topic")
    output: str = Field(..., description="The final output")
    sources: Dict[str, Any] = Field(
        default_factory=dict, description='A mapping of footnote key 1...n to source value object {"title", "date", "url"}"')


class PitchWriterDeps(BaseModel):
    query_budget: int = 5
    max_results: int = 3
    recency: str = "m"

    async def search(self, query: str, recency: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """
        Search the web with query budget tracking
        """
        if self.query_budget <= 0:
            raise RuntimeError("Query budget exhausted")
        self.query_budget -= 1
        max_results = max_results or self.max_results

        results = web_search(
            query, recency=recency, max_results=max_results)
        return {
            "results": results,
            "query_budget_remaining": self.query_budget,
        }


if Agent is not None:
    pitch_writer_agent = Agent[PitchWriterDeps, PitchWriterOutput](
        "openai:gpt-4.1",
        deps_type=PitchWriterDeps,
        output_type=PitchWriterOutput,
        tools=[write_file],
        instructions=prompt_utils.load("prompts/pitcher.txt"),
        model_settings={"temperature": 0.7, "max_tokens": 4096},
    )
else:  # pragma: no cover - environment may lack pydantic_ai
    pitch_writer_agent = None


if pitch_writer_agent is not None:
    @pitch_writer_agent.tool
    async def web_search(
        ctx: RunContext[PitchWriterDeps],
        query: str,
        recency: str,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """Retrieve information from the web using Tavily's search engine."""

        return await ctx.deps.search(query, recency=recency, max_results=max_results)

if __name__ == "__main__":
    prompt = """
        Write a pitch for a community initiative. Include relevant research and statistics.
        Address appropriate audience demographics and back up claims with data.
        Output the pitch to a file named pitch.md when complete.
    """

    deps = PitchWriterDeps(max_results=3, query_budget=10, recency="m")
    result = pitch_writer_agent.run_sync(prompt, deps=deps)

    # pretty-print without deprecated .json()
    print(result.output.model_dump_json(indent=2))

