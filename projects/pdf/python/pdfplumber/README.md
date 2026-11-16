# pdfplumber — PDF / Python

Pinned release: `0.11.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfplumber/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfplumber
python3 parsarium.py run pdf python pdfplumber controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfplumber CORPUS_DIR runs/pdf-pdfplumber-replay
python3 parsarium.py afl build pdf python pdfplumber
python3 parsarium.py afl prepare pdf python pdfplumber runs/pdf-pdfplumber-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
