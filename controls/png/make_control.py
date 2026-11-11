"""Generate a valid 2x1 RGBA PNG with red and green pixels."""

from pathlib import Path
import struct
import zlib


def chunk(kind: bytes, data: bytes) -> bytes:
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def main() -> None:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 2, 1, 8, 6, 0, 0, 0)
    # Filter 0, then two RGBA pixels: opaque red and opaque green.
    scanline = bytes((0, 255, 0, 0, 255, 0, 255, 0, 255))
    png = signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(scanline)) + chunk(b"IEND", b"")
    path = Path(__file__).with_name("red-green.png")
    path.write_bytes(png)
    print(f"{path}: {len(png)} bytes")
    tagged = signature + chunk(b"IHDR", ihdr) + chunk(b"tEXt", b"Title\x00Parsarium") + chunk(b"IDAT", zlib.compress(scanline)) + chunk(b"IEND", b"")
    tagged_path = Path(__file__).with_name("red-green-title.png")
    tagged_path.write_bytes(tagged)
    print(f"{tagged_path}: {len(tagged)} bytes")


if __name__ == "__main__":
    main()
