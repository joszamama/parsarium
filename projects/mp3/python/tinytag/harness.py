"""Parse MP3 bytes with pinned TinyTag."""
import tempfile
from tinytag import TinyTag, TinyTagException

def parse_mp3(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".mp3") as source:
        source.write(data)
        source.flush()
        tag = TinyTag.get(source.name)
    return {'title': tag.title, 'artist': tag.artist, 'album': tag.album}

def fuzz_one_input(data: bytes):
    try:
        parse_mp3(data)
    except (TinyTagException, EOFError, OSError, ValueError):
        pass
