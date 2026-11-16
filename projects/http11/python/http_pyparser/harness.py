"""Byte-input harness for http-pyparser 0.5.1 on http11."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".http") as source:
        source.write(data)
        source.flush()
        return adapter.parse('http-pyparser', data)


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
