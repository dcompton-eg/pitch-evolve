from pitch_evolve.evolution.mutator import llm_mutate_prompt


def test_llm_mutate_prompt_fallback():
    prompt = "Write a short pitch."
    suggestion = "Add a statistic."
    mutated = llm_mutate_prompt(prompt, suggestion)
    assert suggestion in mutated
