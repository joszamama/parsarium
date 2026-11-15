"""Parse PNG chunks with the pinned pngtools package."""

import tempfile

from pngtools import get_type_of_chunk, read_file


def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".png") as source:
        source.write(data)
        source.flush()
        chunks = read_file(source.name)
    return {"chunks": [get_type_of_chunk(chunk).decode("ascii") for chunk in chunks]}


def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (EOFError, OSError, ValueError):
        pass
