"""Read WAV bytes through CPython's wave parser."""

from io import BytesIO
import struct
import wave


def parse_wav(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with wave.open(BytesIO(data), "rb") as reader:
        params = reader.getparams()
        if params.nchannels != 1 or params.sampwidth != 2:
            return None
        frames = reader.readframes(min(4, params.nframes))
    if len(frames) % 2:
        return None
    samples = list(struct.unpack(f"<{len(frames) // 2}h", frames))
    return {"sample_rate": params.framerate, "channels": params.nchannels,
            "bits_per_sample": params.sampwidth * 8, "samples": samples}


def fuzz_one_input(data: bytes):
    try:
        parse_wav(data)
    except (wave.Error, EOFError):
        pass
