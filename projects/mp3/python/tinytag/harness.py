"""Parse untagged MPEG Layer III frame headers from bytes using TinyTag."""

from io import BytesIO
import inspect

from tinytag import TinyTag, TinyTagException
from tinytag.tinytag import _ID3, _MPEG


def class_lines(cls) -> range:
    lines, first = inspect.getsourcelines(cls)
    return range(first, first + len(lines))


# TinyTag dispatches untagged frame-sync input to _MPEG; tagged input goes to
# _ID3, which only delegates the audio part to _MPEG.
MPEG_LINES = class_lines(_MPEG)
ID3_LINES = class_lines(_ID3)


def parse_mp3(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    tag = TinyTag.get(file_obj=BytesIO(data))
    if type(tag) is not _MPEG or tag.duration is None:
        return None
    return {"sample_rate": tag.samplerate, "channels": tag.channels,
            "bitrate_kbps": tag.bitrate,
            "duration_us": round(tag.duration * 1_000_000)}


def fuzz_one_input(data: bytes):
    try:
        parse_mp3(data)
    except TinyTagException:
        pass
