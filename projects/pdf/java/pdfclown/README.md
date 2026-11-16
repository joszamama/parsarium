# pdfclown — PDF / Java

Pinned release: `0.1.2-Beta`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/pdfclown/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java pdfclown
python3 parsarium.py run pdf java pdfclown controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java pdfclown CORPUS_DIR runs/pdf-pdfclown-replay
python3 parsarium.py afl build pdf java pdfclown
python3 parsarium.py afl prepare pdf java pdfclown runs/pdf-pdfclown-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
