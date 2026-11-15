"""Byte-input harness for zipfile36 0.1.3 on zip."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".zip") as source:
        source.write(data)
        source.flush()
        return adapter.run('zipfile36', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
