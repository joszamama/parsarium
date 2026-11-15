"""Parse WAVE stream metadata from bytes using Mutagen."""

from io import BytesIO

from mutagen import MutagenError
from mutagen.wave import WAVE


def parse_wav(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    audio = WAVE(BytesIO(data))
    return {"sample_rate": int(audio.info.sample_rate),
            "channels": int(audio.info.channels),
            "bits_per_sample": int(audio.info.bits_per_sample)}


def fuzz_one_input(data: bytes):
    try:
        parse_wav(data)
    except MutagenError:
        pass
