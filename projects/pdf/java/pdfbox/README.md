# pdfbox — PDF / Java

Pinned release: `3.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/pdfbox/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java pdfbox
python3 parsarium.py run pdf java pdfbox controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java pdfbox CORPUS_DIR runs/pdf-pdfbox-replay
python3 parsarium.py afl build pdf java pdfbox
python3 parsarium.py afl prepare pdf java pdfbox runs/pdf-pdfbox-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
