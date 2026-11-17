"""Byte-input harness for open3d 0.20.0 on ascii_ply."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data:
        return None
    with tempfile.NamedTemporaryFile(suffix=".ply") as source:
        source.write(data)
        source.flush()
        return adapter.read_mesh(Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
