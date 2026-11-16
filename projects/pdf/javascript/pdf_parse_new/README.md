# pdf-parse-new — PDF / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf-parse-new/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf_parse_new
python3 parsarium.py run pdf javascript pdf_parse_new controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf_parse_new CORPUS_DIR runs/pdf-pdf_parse_new-replay
python3 parsarium.py afl build pdf javascript pdf_parse_new
python3 parsarium.py afl prepare pdf javascript pdf_parse_new runs/pdf-pdf_parse_new-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
