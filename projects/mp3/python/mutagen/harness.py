"""Parse untagged MPEG Layer III frame headers from bytes using Mutagen."""

from io import BytesIO

from mutagen import MutagenError
from mutagen.mp3 import MP3


def parse_mp3(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    audio = MP3(BytesIO(data))
    info = audio.info
    if audio.tags is not None or info.layer != 3 or info.sketchy:
        return None
    return {"version": info.version, "layer": info.layer,
            "sample_rate": info.sample_rate, "channels": info.channels,
            "bitrate": info.bitrate, "length_us": round(info.length * 1_000_000)}


def fuzz_one_input(data: bytes):
    try:
        parse_mp3(data)
    except MutagenError:
        pass
