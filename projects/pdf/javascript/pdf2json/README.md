# pdf2json — PDF / JavaScript

Pinned release: `4.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf2json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf2json
python3 parsarium.py run pdf javascript pdf2json controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf2json CORPUS_DIR runs/pdf-pdf2json-replay
python3 parsarium.py afl build pdf javascript pdf2json
python3 parsarium.py afl prepare pdf javascript pdf2json runs/pdf-pdf2json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
