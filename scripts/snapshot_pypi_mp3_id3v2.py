"""Capture bounded PyPI MP3/ID3v2 leads and within-Python download signals."""

from pathlib import Path

from snapshot_pypi_png import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "data" / "python" / "mp3_id3v2",
         ("mp3", "id3", "audio", "music", "tag", "mpeg", "ffmpeg", "media", "sound"))
