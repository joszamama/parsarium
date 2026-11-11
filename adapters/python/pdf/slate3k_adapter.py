"""Isolated Slate3k adapter: pdfminer3k shares pdfminer import paths."""

import json
import sys

import slate3k


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as stream:
        pages = slate3k.PDF(stream)
    print(json.dumps({"pages": len(pages), "text": " ".join(pages[0].split())},
                     sort_keys=True))
