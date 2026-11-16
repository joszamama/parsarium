"""Byte-input harness for ffmpeg-python 0.2.0 on mp3_id3v2."""
import tempfile
from pathlib import Path
import adapter


def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".mp3") as source:
        source.write(data)
        source.flush()
        return adapter.parse('ffmpeg-python', Path(source.name))


def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, UnicodeError, ValueError):
        pass
