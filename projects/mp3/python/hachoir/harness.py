"""Walk every MPEG Layer III frame header in local bytes using hachoir's mpeg_audio parser."""

from io import BytesIO

from hachoir.core import config
from hachoir.field import FieldError
from hachoir.parser import ValidateError
from hachoir.parser.audio.mpeg_audio import Frame, MpegAudioFile
from hachoir.stream import FileInputStream, StreamError

config.quiet = True


def parse_mp3(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    # The parser class is chosen explicitly instead of by guessParser, so no
    # other hachoir format parser runs; validate=True keeps MpegAudioFile's own
    # five-frame header check.
    parser = MpegAudioFile(FileInputStream(BytesIO(data)), validate=True)
    if [field.name for field in parser] != ["frames"]:
        return None
    frames = list(parser["frames"])
    # Full-input scope: every byte must belong to a complete Layer III frame;
    # leading padding, trailing raw bytes and truncated final frames are rejected.
    if not frames or any(not field.name.startswith("frame[") for field in frames):
        return None
    headers = set()
    for frame in frames:
        if (not frame.isValid() or frame["layer"].value != Frame.LAYER_III
                or frame.size != frame.getFrameSize() * 8):
            return None
        headers.add((frame["version"].display, frame["layer"].display,
                     frame.getSampleRate(), frame.getBitRate(),
                     frame["channel_mode"].display, frame.getNbChannel()))
    if len(headers) != 1 or sum(frame.size for frame in frames) != len(data) * 8:
        return None
    version, layer, sample_rate, bitrate, channel_mode, channels = headers.pop()
    return {"version": version, "layer": layer, "sample_rate": sample_rate,
            "bitrate": bitrate, "channel_mode": channel_mode, "channels": channels,
            "frames": len(frames), "frame_bytes": len(data)}


def fuzz_one_input(data: bytes):
    try:
        parse_mp3(data)
    except (ValidateError, FieldError, StreamError):
        # hachoir's rejection types: validation, field (ParserError,
        # MissingField) and stream (InputStreamError) errors.
        pass
