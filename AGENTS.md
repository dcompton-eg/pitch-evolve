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

## Example Agents

### Basic Pitch Agent

A simple agent that creates introductory pitches for Go communities based on a target audience's background and interests.

### Personalized Pitch Agent

An advanced agent that tailors pitches to specific individual attributes, creating highly personalized invitations to join a Go community.

### Multi-channel Pitch Agent

An agent specialized in generating pitches adapted to different communication channels (social media, email, in-person, etc.).

## Integration

The agents are designed to be integrated with:

1. Web applications for community managers
2. Email marketing systems
3. Social media management platforms
4. Community management tools

## Future Development

Planned enhancements include:

- Support for multimodal pitch generation (text, images, video scripts)
- Fine-tuning on real-world feedback data
- A/B testing framework for pitch effectiveness
- Localization support for international Go communities

## Repository Interaction Guidelines

- Run `pytest -q` before committing any changes to ensure the test suite passes.
- Commit code directly to the main branch (no extra branches).
- Include a short summary of the test output in the PR description.
