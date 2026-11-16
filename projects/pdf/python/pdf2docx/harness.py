"""Byte-input harness for pdf2docx 0.5.13 on pdf."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".pdf") as source:
        source.write(data)
        source.flush()
        return adapter.parse('pdf2docx', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
