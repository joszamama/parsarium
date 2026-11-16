# mupdf — PDF / JavaScript

Pinned release: `1.28.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/mupdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript mupdf
python3 parsarium.py run pdf javascript mupdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript mupdf CORPUS_DIR runs/pdf-mupdf-replay
python3 parsarium.py afl build pdf javascript mupdf
python3 parsarium.py afl prepare pdf javascript mupdf runs/pdf-mupdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
