"""Parse MPEG audio and its ID3v2 tags from bytes using Mutagen."""

from io import BytesIO

from mutagen import MutagenError
from mutagen.mp3 import MP3


def parse_mp3(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    audio = MP3(BytesIO(data))
    if audio.tags is None or not all(key in audio.tags for key in ("TIT2", "TPE1", "TALB")):
        return None
    return {"title": str(audio.tags["TIT2"]).strip("\x00"),
            "artist": str(audio.tags["TPE1"]).strip("\x00"),
            "album": str(audio.tags["TALB"]).strip("\x00")}


def fuzz_one_input(data: bytes):
    try:
        parse_mp3(data)
    except MutagenError:
        pass
