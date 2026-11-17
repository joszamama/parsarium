"""Check the two untagged MP3 controls by walking their MPEG audio frame headers.

Both files were generated once with FFmpeg 9.0.2 and libmp3lame, with ID3v2,
ID3v1 and the Xing/Info frame disabled:

  ffmpeg -fflags +bitexact -f lavfi -i sine=frequency=440:sample_rate=44100:duration=0.25 \
    -ac 1 -c:a libmp3lame -b:a 64k -flags +bitexact -write_xing 0 -id3v2_version 0 \
    -write_id3v1 0 -map_metadata -1 tone-44k-mono.mp3
  ffmpeg -fflags +bitexact -f lavfi -i sine=frequency=660:sample_rate=22050:duration=0.25 \
    -ac 2 -c:a libmp3lame -b:a 32k -flags +bitexact -write_xing 0 -id3v2_version 0 \
    -write_id3v1 0 -map_metadata -1 tone-22k-stereo.mp3

This walker is an independent oracle for the frame counts the Rust harness
reports. It reads only the four-byte headers and follows frame lengths to EOF.
"""

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BITRATES = {  # kbit/s, Layer III
    1: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
    2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}
RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}
CONTROLS = {
    "tone-44k-mono.mp3": "9bcbe84e7a36645c09464e671b81af90766e569d07f1b4e214b8cf87b46bf328",
    "tone-22k-stereo.mp3": "871bfdb49897b4e2e1994987862aca928f4f6438f731831e3c7662579fb8c000",
}


def walk(data: bytes) -> dict:
    offset, frames, headers = 0, 0, set()
    while offset < len(data):
        b1, b2, b3 = data[offset + 1], data[offset + 2], data[offset + 3]
        assert data[offset] == 0xFF and b1 & 0xE0 == 0xE0, f"no frame sync at {offset}"
        version_bits, layer_bits = (b1 >> 3) & 3, (b1 >> 1) & 3
        assert layer_bits == 1 and version_bits != 1, "not MPEG Layer III"
        lsf = version_bits != 3
        bitrate = BITRATES[2 if lsf else 1][b2 >> 4] * 1000
        rate = RATES[version_bits][(b2 >> 2) & 3]
        channels = 1 if b3 >> 6 == 3 else 2
        length = (72 if lsf else 144) * bitrate // rate + ((b2 >> 1) & 1)
        headers.add((rate, channels, bitrate, 576 if lsf else 1152))
        offset += length
        frames += 1
    assert offset == len(data) and len(headers) == 1
    rate, channels, bitrate, samples = headers.pop()
    return {"sample_rate": rate, "channels": channels, "frames": frames,
            "frame_bytes": len(data), "samples_per_frame": samples, "bitrate": bitrate}


if __name__ == "__main__":
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == digest, name
        assert data[:3] != b"ID3" and data[-128:-125] != b"TAG"
        print(name, json.dumps(walk(data)))
