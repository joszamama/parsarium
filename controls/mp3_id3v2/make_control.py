"""Restore a fixed valid MP3 with ID3v2.3 tags from committed source bytes.

The source was generated once with FFmpeg: one second of 440 Hz mono audio at
8000 Hz, MP3 32 kbit/s, and ID3v2.3 title/artist/album tags. Verification
requires only Python to restore the exact source bytes.
"""

from base64 import b64decode
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parent
data = b64decode((root / "source.b64").read_text())
expected_sha256 = "d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad"
assert sha256(data).hexdigest() == expected_sha256
assert data[:4] == b"ID3\x03"
out = root / "tone-tags.mp3"
out.write_bytes(data)
print(f"Wrote {len(data)} MP3 bytes with SHA-256 {expected_sha256}")

# A second valid tagged control uses MPEG-1 Layer III at 44.1 kHz. It was
# generated once with FFmpeg 9.0.2 from a one-second 440 Hz sine wave, 64 kbit/s
# mono libmp3lame audio, and the same ID3v2.3 title/artist/album fields.
data_44k = b64decode((root / "source-44k.b64").read_text())
expected_44k_sha256 = "c8ca0d2c5a224ceccf150f06b9ad4de9eca753f8ce4b4817b95de0aeb07fd307"
assert sha256(data_44k).hexdigest() == expected_44k_sha256
assert data_44k[:4] == b"ID3\x03"
out_44k = root / "tone-tags-44k.mp3"
out_44k.write_bytes(data_44k)
print(f"Wrote {len(data_44k)} MP3 bytes with SHA-256 {expected_44k_sha256}")
