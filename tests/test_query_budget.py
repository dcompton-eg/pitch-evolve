import os
os.environ.setdefault("OPENAI_API_KEY", "sk-test")

import pytest

from pitch_evolve.agents import PitchWriterDeps


@pytest.mark.asyncio
async def test_search_stops_at_budget_one():
    deps = PitchWriterDeps(query_budget=2, max_results=1)

    # First search should succeed and decrement budget
    res1 = await deps.search("go", recency="m")
    assert res1["query_budget_remaining"] == 1
    assert "budget_exhausted" not in res1

    # Next search should not be executed and should signal exhaustion
    res2 = await deps.search("go", recency="m")
    assert res2["budget_exhausted"] is True
    assert res2["query_budget_remaining"] == 1
