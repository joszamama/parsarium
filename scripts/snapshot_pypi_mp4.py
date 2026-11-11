"""Capture bounded PyPI MP4 leads and within-Python download signals."""

from pathlib import Path

from snapshot_pypi_png import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "data" / "python" / "mp4",
         ("mp4", "mpeg4", "video", "media", "ffmpeg", "isobmff", "movie", "codec", "box"))
