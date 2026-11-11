"""Capture bounded PyPI ZIP leads, pinned release hashes, and download signals."""

from pathlib import Path
from snapshot_pypi_png import main

ROOT = Path(__file__).resolve().parents[1]
TERMS = ("zip", "unzip", "archive", "deflate", "libarchive",
         "zipp", "pyzip", "fsspec", "patool")

if __name__ == "__main__":
    main(ROOT / "data" / "python" / "zip", TERMS)
