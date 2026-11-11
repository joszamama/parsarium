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
