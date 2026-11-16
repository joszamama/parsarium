# pdfjet — PDF / Java

Pinned release: `9.1.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/pdfjet/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java pdfjet
python3 parsarium.py run pdf java pdfjet controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java pdfjet CORPUS_DIR runs/pdf-pdfjet-replay
python3 parsarium.py afl build pdf java pdfjet
python3 parsarium.py afl prepare pdf java pdfjet runs/pdf-pdfjet-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
