"""Capture bounded PyPI WAV leads, pinned releases, and download signals."""

from pathlib import Path
from snapshot_pypi_png import main

ROOT = Path(__file__).resolve().parents[1]
TERMS = ("wav", "wave", "audio", "sound", "riff", "pcm", "sndfile", "media", "tag")

if __name__ == "__main__":
    main(ROOT / "data" / "python" / "wav", TERMS)
