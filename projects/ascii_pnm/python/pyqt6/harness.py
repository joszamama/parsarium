"""Byte-input harness for PyQt6 6.12.0 on ascii_pnm."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".ppm") as source:
        source.write(data)
        source.flush()
        return adapter.run('PyQt6', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
