# pdf-text-reader — PDF / JavaScript

Pinned release: `5.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf-text-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf_text_reader
python3 parsarium.py run pdf javascript pdf_text_reader controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf_text_reader CORPUS_DIR runs/pdf-pdf_text_reader-replay
python3 parsarium.py afl build pdf javascript pdf_text_reader
python3 parsarium.py afl prepare pdf javascript pdf_text_reader runs/pdf-pdf_text_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
