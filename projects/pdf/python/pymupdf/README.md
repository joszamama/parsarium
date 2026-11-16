# PyMuPDF — PDF / Python

Pinned release: `2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pymupdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pymupdf
python3 parsarium.py run pdf python pymupdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pymupdf CORPUS_DIR runs/pdf-pymupdf-replay
python3 parsarium.py afl build pdf python pymupdf
python3 parsarium.py afl prepare pdf python pymupdf runs/pdf-pymupdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
