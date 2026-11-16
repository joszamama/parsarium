"""Byte-input harness for polyxios 0.5.1 on ascii_ply."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".ply") as source:
        source.write(data)
        source.flush()
        return adapter.parse('polyxios', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
