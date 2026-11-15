"""Parse PNG bytes with the pinned imagesize package."""
import imagesize
import tempfile

def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".png") as source:
        source.write(data)
        source.flush()
        width, height = imagesize.get(source.name)
    return {"width": width, "height": height}

def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (EOFError, OSError, ValueError):
        pass
