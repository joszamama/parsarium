# pdf2docx — PDF / Python

Pinned release: `0.5.13`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdf2docx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdf2docx
python3 parsarium.py run pdf python pdf2docx controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdf2docx CORPUS_DIR runs/pdf-pdf2docx-replay
python3 parsarium.py afl build pdf python pdf2docx
python3 parsarium.py afl prepare pdf python pdf2docx runs/pdf-pdf2docx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
