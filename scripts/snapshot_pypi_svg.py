"""Capture bounded PyPI SVG leads and Python download signals."""

from pathlib import Path

from snapshot_pypi_png import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "data" / "python" / "svg",
         ("svg", "svg-", "svg2", "svg_", "pysvg", "svglib", "scour",
          "inkscape", "vector", "cairo", "rsvg", "resvg", "skia",
          "vips", "qt", "image"))
