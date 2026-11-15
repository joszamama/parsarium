"""Atheris entry point; the valid-control runner does not start a campaign."""

import sys

import atheris

with atheris.instrument_imports():
    from harness import fuzz_one_input

atheris.Setup(sys.argv, fuzz_one_input)
atheris.Fuzz()
