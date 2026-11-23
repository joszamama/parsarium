"""Read WAV bytes through CPython's wave parser."""

from io import BytesIO
import wave


def parse_wav(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with wave.open(BytesIO(data), "rb") as reader:
        params = reader.getparams()
        # The first four interleaved samples: enough frames to hold them.
        wanted = -(-4 // params.nchannels) if params.nchannels else 0
        frames = reader.readframes(min(wanted, params.nframes))
    width = params.sampwidth
    count = min(4, len(frames) // width) if width else 0
    # wave returns raw little-endian samples; 8-bit WAV samples are unsigned.
    samples = [int.from_bytes(frames[i * width:(i + 1) * width], "little", signed=width > 1)
               for i in range(count)]
    return {"sample_rate": params.framerate, "channels": params.nchannels,
            "bits_per_sample": params.sampwidth * 8, "samples": samples}


def fuzz_one_input(data: bytes):
    try:
        parse_wav(data)
    except (wave.Error, EOFError):
        pass
