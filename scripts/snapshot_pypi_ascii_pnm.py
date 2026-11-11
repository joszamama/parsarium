"""Capture bounded PyPI ASCII PNM leads and comparable adoption metrics."""

from pathlib import Path
from snapshot_pypi_png import main

ROOT = Path(__file__).resolve().parents[1]
TERMS = ("pnm", "ppm", "pgm", "pbm", "netpbm", "imageio", "imread",
         "pillow", "opencv", "qt", "wx", "vips")

if __name__ == "__main__":
    main(ROOT / "data" / "python" / "ascii_pnm", TERMS)
