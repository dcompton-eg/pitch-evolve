# Automated Pitch Generation

This document summarises the evaluation and prompt evolution strategy from the
original PDF. It outlines how pitches can be automatically scored and how
prompts are evolved over time using a tournament style search.

The repository now includes an LLM-as-judge scoring helper and a
`PromptEvolutionEngine` which implements tournament based optimisation of
prompts. The judge returns both numeric scores and a suggestion for improving
the prompt.

Prompt mutation can also be handled by an LLM powered by `pydantic-ai`. The
`llm_mutate_prompt` helper invokes the `openai:gpt-4o` model and returns a
structured ``MutatedPrompt`` object containing only the revised prompt text.
