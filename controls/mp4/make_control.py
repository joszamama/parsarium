"""Restore the pinned valid MP4 control from its committed base64 source.

The source was generated once with FFmpeg using a 2×2 red H.264 frame, one
second of silent 8 kHz AAC audio, a Parsarium title tag, and a fixed 2020
creation time. Committing the bytes makes the control
independent of a system FFmpeg version for future verification.
"""

from base64 import b64decode
from hashlib import sha256
from pathlib import Path

root = Path(__file__).resolve().parent
data = b64decode((root / "source.b64").read_text())
expected_sha256 = "10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643"
assert sha256(data).hexdigest() == expected_sha256
out = root / "red-av.mp4"
out.write_bytes(data)
print(f"Wrote {len(data)} MP4 bytes with SHA-256 {expected_sha256}")
