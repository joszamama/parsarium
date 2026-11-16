# spatie/pdf-to-text — PDF / PHP

Pinned release: `1.55.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/spatie-pdf-to-text/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php spatie_pdf_to_text
python3 parsarium.py run pdf php spatie_pdf_to_text controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php spatie_pdf_to_text CORPUS_DIR runs/pdf-spatie_pdf_to_text-replay
python3 parsarium.py afl build pdf php spatie_pdf_to_text
python3 parsarium.py afl prepare pdf php spatie_pdf_to_text runs/pdf-spatie_pdf_to_text-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
