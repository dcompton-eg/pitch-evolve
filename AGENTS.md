# Pitch-Evolve Agents

This document describes how agents should interact with this repository.

## Overview

Pitch-Evolve is a system that uses AI agents with evolving prompts to generate effective pitches for attracting new members to Go communities. The agents use pydantic for type validation and implement an evolutionary approach to improve the quality of generated pitches over time.

## Agent Architecture

Each agent in the system follows this basic architecture:

1. **Base Agent**: Defines the core interface for all agents in the system
2. **Pitch Generation Agent**: Specializes in creating compelling pitches based on target audience and community attributes
3. **Prompt Evolution Engine**: Implements strategies for evolving prompts based on evaluation feedback

All agents MUST be implemented using the pydantic-ai framework.
All agents should have strongly typed/structured outputs using pydantic.

## Evolution Strategy

The prompt evolution follows a tournament selection approach:

1. Initialize a population of prompt variants
2. Generate pitches using each prompt variant
3. Evaluate the pitches using predefined metrics
4. Select the top-performing prompts for "reproduction"
5. Create new prompt variants through recombination and mutation
6. Replace the old population with the new generation
7. Repeat the process for N generations

## Evaluation Framework

Pitches are evaluated on multiple dimensions:

- **Relevance**: How well the pitch addresses the needs and interests of the target audience
- **Persuasiveness**: How effectively the pitch motivates the audience to take action
- **Clarity**: How clear and easy to understand the pitch is
- **Distinctiveness**: How well the pitch stands out from generic content

## Repository Interaction Guidelines

- Run `pytest -q` before committing any changes to ensure the test suite passes.
- Include a short summary of the test output in the PR description.
- Model new agents after existing agents in agents/ directory
