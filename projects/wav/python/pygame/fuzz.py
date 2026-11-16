"""Atheris entry point for the pygame WAV harness."""

import sys

import atheris

with atheris.instrument_imports():
    from harness import test_one_input

atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
