"""Byte-input harness for napari-netpbmfile 0.0.3 on ascii_pnm."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".ppm") as source:
        source.write(data)
        source.flush()
        return adapter.run('napari-netpbmfile', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
