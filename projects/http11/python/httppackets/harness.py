"""Byte-input harness for httppackets 0.1.0a0 on http11."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".http") as source:
        source.write(data)
        source.flush()
        return adapter.parse('httppackets', data)


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
