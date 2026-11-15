# pdf-lib — PDF / JavaScript

Pinned release: `1.17.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/pdf-lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript pdf_lib
python3 parsarium.py run pdf javascript pdf_lib controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript pdf_lib CORPUS_DIR runs/pdf-pdf_lib-replay
python3 parsarium.py afl build pdf javascript pdf_lib
python3 parsarium.py afl prepare pdf javascript pdf_lib runs/pdf-pdf_lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
