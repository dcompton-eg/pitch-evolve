import os
os.environ.setdefault("OPENAI_API_KEY", "sk-test")

from pitch_evolve.agents import llm_mutate_prompt


def test_llm_mutate_prompt_fallback():
    prompt = "Write a short pitch."
    suggestion = "Add a statistic."
    mutated = llm_mutate_prompt(prompt, suggestion)
    assert suggestion in mutated
