"""Parse mp4 bytes with pinned TinyTag."""
import tempfile
from tinytag import TinyTag, TinyTagException

def parse_mp4(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".mp4") as source:
        source.write(data)
        source.flush()
        tag = TinyTag.get(source.name)
    return {'title': tag.title, 'duration_seconds': round(tag.duration, 3)}

def fuzz_one_input(data: bytes):
    try:
        parse_mp4(data)
    except (TinyTagException, EOFError, OSError, ValueError):
        pass
