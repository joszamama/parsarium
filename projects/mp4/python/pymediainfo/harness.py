"""Byte-input harness for pymediainfo 7.0.1 on mp4."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".mp4") as source:
        source.write(data)
        source.flush()
        return adapter.parse('pymediainfo', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
