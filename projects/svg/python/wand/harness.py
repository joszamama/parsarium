"""Byte-input harness for Wand 0.7.2 on svg."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".svg") as source:
        source.write(data)
        source.flush()
        return adapter.parse('Wand', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
