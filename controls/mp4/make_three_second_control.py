"""Restore a valid MP4 with enough samples for the Red5 MP4Reader API.

Generated with pinned FFmpeg 9.0.2 from a 16x16 red H.264 video at 25 fps
and silent 8 kHz AAC audio for three seconds:

  ffmpeg -f lavfi -i color=c=red:s=16x16:r=25:d=3 \
    -f lavfi -i anullsrc=r=8000:cl=mono -t 3 \
    -c:v libx264 -pix_fmt yuv420p -c:a aac -map_metadata -1 source.mp4

Committed source bytes make restoration independent of the local FFmpeg build.
"""

from base64 import b64decode
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = HERE / "red-av-3s.mp4"
SHA256 = "a153daff81e38744da7a653d44a4f381b7f4768d6f4148a00391b440af5ef308"


def main() -> None:
    data = b64decode((HERE / "source-red-av-3s.b64").read_text())
    assert sha256(data).hexdigest() == SHA256
    DEST.write_bytes(data)
    print(f"Wrote {len(data)} valid MP4 bytes with SHA-256 {SHA256}")


if __name__ == "__main__":
    main()
