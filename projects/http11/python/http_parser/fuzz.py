"""Atheris byte-input entry for the pinned native HTTP parser."""

import sys
import atheris

with atheris.instrument_imports():
    from harness import fuzz_one_input

atheris.Setup(sys.argv, fuzz_one_input)
atheris.Fuzz()
