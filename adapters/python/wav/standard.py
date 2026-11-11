"""Parse a valid local PCM WAV with the CPython wave module."""

import json
import struct
import sys
import wave


def main(path):
    with wave.open(path, "rb") as reader:
        frames = reader.readframes(reader.getnframes())
        return {"sample_rate": reader.getframerate(), "channels": reader.getnchannels(),
                "bits_per_sample": reader.getsampwidth() * 8,
                "samples": list(struct.unpack("<4h", frames))}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: standard.py CONTROL_PATH")
    print(json.dumps(main(sys.argv[1])))
