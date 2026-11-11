"""Capture bounded PyPI PDF leads and comparable Python download signals."""

from pathlib import Path

from snapshot_pypi_png import main


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "data" / "python" / "pdf",
         ("pdf", "pypdf", "pdfminer", "poppler", "document", "page", "extract", "reader", "markdown"))
