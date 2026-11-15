"""Parse wav bytes with pinned TinyTag."""
import tempfile
from tinytag import TinyTag, TinyTagException

def parse_wav(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".wav") as source:
        source.write(data)
        source.flush()
        tag = TinyTag.get(source.name)
    return {'sample_rate': int(tag.samplerate), 'channels': int(tag.channels), 'duration_seconds': tag.duration}

def fuzz_one_input(data: bytes):
    try:
        parse_wav(data)
    except (TinyTagException, EOFError, OSError, ValueError):
        pass
