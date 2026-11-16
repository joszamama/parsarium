# pdf-parse — PDF / JavaScript

Pinned release: `2.4.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf-parse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf_parse
python3 parsarium.py run pdf javascript pdf_parse controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf_parse CORPUS_DIR runs/pdf-pdf_parse-replay
python3 parsarium.py afl build pdf javascript pdf_parse
python3 parsarium.py afl prepare pdf javascript pdf_parse runs/pdf-pdf_parse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
