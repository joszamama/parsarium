# pdf2image — PDF / Python

Pinned release: `1.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdf2image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdf2image
python3 parsarium.py run pdf python pdf2image controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdf2image CORPUS_DIR runs/pdf-pdf2image-replay
python3 parsarium.py afl build pdf python pdf2image
python3 parsarium.py afl prepare pdf python pdf2image runs/pdf-pdf2image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
