# PyMuPDF — SVG / Python

Pinned release: `2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pymupdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pymupdf
python3 parsarium.py run svg python pymupdf controls/svg/red-green.svg
python3 parsarium.py replay svg python pymupdf CORPUS_DIR runs/svg-pymupdf-replay
python3 parsarium.py afl build svg python pymupdf
python3 parsarium.py afl prepare svg python pymupdf runs/svg-pymupdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
