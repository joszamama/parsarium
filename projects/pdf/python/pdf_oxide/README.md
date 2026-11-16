# pdf_oxide — PDF / Python

Pinned release: `0.3.78`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdf-oxide/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdf_oxide
python3 parsarium.py run pdf python pdf_oxide controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdf_oxide CORPUS_DIR runs/pdf-pdf_oxide-replay
python3 parsarium.py afl build pdf python pdf_oxide
python3 parsarium.py afl prepare pdf python pdf_oxide runs/pdf-pdf_oxide-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
