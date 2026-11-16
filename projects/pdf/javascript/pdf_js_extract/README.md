# pdf.js-extract — PDF / JavaScript

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf-js-extract/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf_js_extract
python3 parsarium.py run pdf javascript pdf_js_extract controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf_js_extract CORPUS_DIR runs/pdf-pdf_js_extract-replay
python3 parsarium.py afl build pdf javascript pdf_js_extract
python3 parsarium.py afl prepare pdf javascript pdf_js_extract runs/pdf-pdf_js_extract-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
