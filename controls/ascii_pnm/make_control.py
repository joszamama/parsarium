"""Create small, valid plain (ASCII) Netpbm controls."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTROLS = {
    "black-white.pbm": b"P1\n2 1\n0 1\n",
    "black-white.pgm": b"P2\n2 1\n255\n0 255\n",
    "red-green.ppm": b"P3\n2 1\n255\n255 0 0  0 255 0\n",
    "red-green-compact.ppm": b"P3\n2 1\n255\n255 0 0 0 255 0",
}

for name, contents in CONTROLS.items():
    (HERE / name).write_bytes(contents)
    print(f"{name}: {len(contents)} bytes")
