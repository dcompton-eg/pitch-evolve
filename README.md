# Pitch-Evolve

Pitch-Evolve is a Python package that demonstrates how AI agents leverage prompt-evolution to improve the quality of text content over multiple generations/rounds.  The use-case is the generation of a pitch to join a programming language community, but this technique can be applied to any content where prompt engineering could improve the quality of output.

## Features

- **PitchWriter Agent** – generates a short, source-backed pitch using a search tool and returns structured output.
- **LLM-as-Judge** – scores pitches across creativity, persuasiveness, clarity, statistical grounding and thematic relevance.
- **LLM-as-Judge-Mutator** – mutates prompts based on feedback from judge and pitch.
- **PromptEvolutionEngine** – performs tournament-style selection and mutation of prompts to gradually improve scores.
- **Command line interface** – run a single pitch or evolve a prompt across several generations.

## Getting Started

1. Run `./setup.sh` to create a virtual environment and install dependencies.
2. Add your API keys to the generated `.env` file.
3. Activate the environment with `source venv/bin/activate`.
4. Use `python -m pitch_evolve.cli pitch "your base prompt"` to generate a pitch or
   `python -m pitch_evolve.cli evolve "your base prompt"` to start prompt evolution.

Test the package by running `pytest -q`.


## Docs

See docs/ directory for more information about strategies employed in this repository
