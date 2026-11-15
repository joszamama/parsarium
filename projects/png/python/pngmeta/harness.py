"""Parse PNG metadata bytes with the pinned pngmeta package."""
from pngmeta import PngMeta
import tempfile

def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".png") as source:
        source.write(data)
        source.flush()
        title = PngMeta(source.name).get("Title")
    return {"title": title}

def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (EOFError, OSError, ValueError):
        pass
