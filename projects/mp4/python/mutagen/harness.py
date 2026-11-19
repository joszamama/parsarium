"""Parse MP4 audio metadata from bytes using Mutagen."""

from io import BytesIO

from mutagen import MutagenError
from mutagen.mp4 import MP4


def parse_mp4(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    audio = MP4(BytesIO(data))
    if audio.tags is None or not audio.tags.get("\u00a9nam"):
        return {}
    return {"title": str(audio.tags["\u00a9nam"][0])}


def fuzz_one_input(data: bytes):
    try:
        parse_mp4(data)
    except MutagenError:
        pass
