"""Byte-input harness for audiomath 1.23.0 on mp4."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".mp4") as source:
        source.write(data)
        source.flush()
        return adapter.parse('audiomath', source.name)


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
