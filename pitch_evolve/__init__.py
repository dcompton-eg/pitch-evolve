"""Pitch-Evolve package."""

import importlib

__all__ = [
    "pitch_writer_agent",
    "PitchWriterDeps",
    "PitchWriterOutput",
]


def __getattr__(name):
    if name in __all__:
        module = importlib.import_module("pitch_evolve.agents.pitch_writer")
        globals()["pitch_writer_agent"] = module.pitch_writer_agent
        globals()["PitchWriterDeps"] = module.PitchWriterDeps
        globals()["PitchWriterOutput"] = module.PitchWriterOutput
        return globals()[name]
    raise AttributeError(name)
