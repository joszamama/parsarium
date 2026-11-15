"""Parse PNG bytes with the pinned byteparse package."""
from byteparse.formats import PNGFile

def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    image = PNGFile.parse(data)
    return {"width": image.ihdr.width, "height": image.ihdr.height}

def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (EOFError, OSError, ValueError):
        pass
