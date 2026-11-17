"""Atheris byte-input bridge; verification only invokes fixed valid files."""

import sys

import atheris

with atheris.instrument_imports():
    from harness import fuzz_one_input

atheris.Setup(sys.argv, fuzz_one_input)
atheris.Fuzz()
