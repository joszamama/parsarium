"""Restore a valid MP4 control without optional user metadata.

The source bytes came from FFmpeg 9.0.2 with a red 2x2 H.264 frame and silent
8 kHz AAC audio for one second:

  ffmpeg -f lavfi -i color=c=red:s=2x2:r=1:d=1 \
    -f lavfi -i anullsrc=r=8000:cl=mono -t 1 \
    -c:v libx264 -pix_fmt yuv420p -c:a aac \
    -map_metadata -1 -metadata encoder= source.mp4

Its optional moov/udta box was removed and the moov box size was updated.
The moov box follows mdat, so media chunk offsets were unchanged. The
resulting two-stream MP4 was checked with FFprobe and JAAD. Pinned base64
bytes make restoration independent of local FFmpeg builds.
"""

from base64 import b64decode
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = HERE / "red-av-no-udta.mp4"
SHA256 = "6c181e06c4a1ccdce7b55b39580bbf80286bd5949660bce1aebbb00dd4baebc7"


def main() -> None:
    data = b64decode((HERE / "source-no-udta.b64").read_text())
    assert sha256(data).hexdigest() == SHA256
    DEST.write_bytes(data)
    print(f"Wrote {len(data)} valid MP4 bytes with SHA-256 {SHA256}")


if __name__ == "__main__":
    main()
