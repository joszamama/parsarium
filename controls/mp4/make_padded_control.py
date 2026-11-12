"""Derive a valid large MP4 control for APIs with a minimum file-size check.

The original ftyp, moov, free, and mdat boxes are preserved byte-for-byte.
An additional top-level free box contains only padding and carries no media.
"""

from hashlib import sha256
from pathlib import Path
from struct import pack

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "red-av.mp4"
DEST = HERE / "red-av-padded.mp4"
SOURCE_SHA256 = "10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643"
FREE_SIZE = 65536


def main() -> None:
    source = SOURCE.read_bytes()
    assert sha256(source).hexdigest() == SOURCE_SHA256
    result = source + pack(">I4s", FREE_SIZE, b"free") + bytes(FREE_SIZE - 8)
    DEST.write_bytes(result)
    print(f"{DEST.relative_to(HERE.parent.parent)}: {len(result)} bytes, sha256={sha256(result).hexdigest()}")


if __name__ == "__main__":
    main()
