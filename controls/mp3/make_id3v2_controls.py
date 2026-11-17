"""Restore a fixed valid MP3 with ID3v2.3 tags from committed source bytes.

The source was generated once with FFmpeg: one second of 440 Hz mono audio at
8000 Hz, MP3 32 kbit/s, and ID3v2.3 title/artist/album tags. Verification
requires only Python to restore the exact source bytes.
"""

from base64 import b64decode
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parent
data = b64decode((root / "id3v2-source.b64").read_text())
expected_sha256 = "d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad"
assert sha256(data).hexdigest() == expected_sha256
assert data[:4] == b"ID3\x03"
out = root / "id3v2-tagged-tone.mp3"
out.write_bytes(data)
print(f"Wrote {len(data)} MP3 bytes with SHA-256 {expected_sha256}")

# A second valid tagged control uses MPEG-1 Layer III at 44.1 kHz. It was
# generated once with FFmpeg 9.0.2 from a one-second 440 Hz sine wave, 64 kbit/s
# mono libmp3lame audio, and the same ID3v2.3 title/artist/album fields.
data_44k = b64decode((root / "id3v2-source-44k.b64").read_text())
expected_44k_sha256 = "c8ca0d2c5a224ceccf150f06b9ad4de9eca753f8ce4b4817b95de0aeb07fd307"
assert sha256(data_44k).hexdigest() == expected_44k_sha256
assert data_44k[:4] == b"ID3\x03"
out_44k = root / "id3v2-tagged-tone-44k.mp3"
out_44k.write_bytes(data_44k)
print(f"Wrote {len(data_44k)} MP3 bytes with SHA-256 {expected_44k_sha256}")

# A third valid ID3v2.3 control has 18 seconds of 8 kHz mono 32 kbit/s MP3.
# Its larger file supports MediaInfo wrappers that require at least 65,536
# input bytes. The source was generated once with FFmpeg 9.0.2 from an 18-second
# 440 Hz sine wave and the same title/artist/album, then committed as base64.
data_long = b64decode((root / "id3v2-source-long.b64").read_text())
expected_long_sha256 = "2b085bb9e5bef6bb4254233a9d6bf0652ced4589373600cff3b8ddab07909dac"
assert sha256(data_long).hexdigest() == expected_long_sha256
assert data_long[:4] == b"ID3\x03" and len(data_long) == 72941
out_long = root / "id3v2-tagged-tone-long.mp3"
out_long.write_bytes(data_long)
print(f"Wrote {len(data_long)} MP3 bytes with SHA-256 {expected_long_sha256}")

# Derive an ID3v2.4 control from the same valid MPEG audio frames. ID3v2.4
# uses synchsafe frame lengths, unlike the ID3v2.3 source above.
def synchsafe(value: int) -> bytes:
    assert 0 <= value < 1 << 28
    return bytes((value >> shift) & 0x7f for shift in (21, 14, 7, 0))


original_tag_size = sum((byte & 0x7f) << shift for byte, shift in zip(data[6:10], (21, 14, 7, 0)))
audio_frames = data[10 + original_tag_size:]
assert audio_frames[:2] == b"\xff\xe3"
frames = b""
for frame_id, value in ((b"TIT2", "Parsarium"), (b"TPE1", "Control"), (b"TALB", "Pilot")):
    payload = b"\x03" + value.encode("utf-8")
    frames += frame_id + synchsafe(len(payload)) + b"\x00\x00" + payload
data_v24 = b"ID3\x04\x00\x00" + synchsafe(len(frames)) + frames + audio_frames
expected_v24_sha256 = "a5337540e40f66d89398dbc29e366034d21ec5ba5f0cd539392cddb07530616d"
assert sha256(data_v24).hexdigest() == expected_v24_sha256
out_v24 = root / "id3v2-tagged-tone-v24.mp3"
out_v24.write_bytes(data_v24)
print(f"Wrote {len(data_v24)} ID3v2.4 MP3 bytes with SHA-256 {expected_v24_sha256}")
