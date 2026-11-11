"""Capture bounded PyPI HTTP/1.1 leads and comparable Python downloads."""

from pathlib import Path

from snapshot_pypi_png import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "data" / "python" / "http11",
         ("http", "h11", "h1parser", "request", "response", "proxy",
          "websocket", "tornado", "twisted", "header"))
