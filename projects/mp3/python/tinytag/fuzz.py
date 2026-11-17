"""Atheris byte-input entry point for this parser."""
import sys
import atheris
with atheris.instrument_imports():
    from harness import fuzz_one_input
atheris.Setup(sys.argv, fuzz_one_input)
atheris.Fuzz()
