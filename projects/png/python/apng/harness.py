"""Parse PNG bytes with the pinned apng package."""
from apng import PNG
import tempfile

def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".png") as source:
        source.write(data)
        source.flush()
        image = PNG.open(source.name)
    return {"width": image.width, "height": image.height,
            "chunks": [chunk.type for chunk in image.chunks]}

def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (EOFError, OSError, ValueError):
        pass
