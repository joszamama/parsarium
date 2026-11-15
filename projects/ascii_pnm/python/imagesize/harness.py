"""Parse ASCII PNM bytes with the pinned imagesize package."""
import imagesize
import tempfile

def parse_pnm(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".ppm") as source:
        source.write(data)
        source.flush()
        width, height = imagesize.get(source.name)
    return {"width": width, "height": height}

def fuzz_one_input(data: bytes):
    try:
        parse_pnm(data)
    except (EOFError, OSError, ValueError):
        pass
