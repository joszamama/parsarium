"""Isolated PDFx adapter: its pinned pdfminer.six conflicts with pdfplumber."""

import json
import sys

import pdfx


if __name__ == "__main__":
    metadata = pdfx.PDFx(sys.argv[1]).get_metadata()
    print(json.dumps({"pages": metadata["Pages"], "title": metadata["Title"]},
                     sort_keys=True))
