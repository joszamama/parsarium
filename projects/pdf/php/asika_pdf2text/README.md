# asika/pdf2text — PDF / PHP

Pinned release: `1.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/asika-pdf2text/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php asika_pdf2text
python3 parsarium.py run pdf php asika_pdf2text controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php asika_pdf2text CORPUS_DIR runs/pdf-asika_pdf2text-replay
python3 parsarium.py afl build pdf php asika_pdf2text
python3 parsarium.py afl prepare pdf php asika_pdf2text runs/pdf-asika_pdf2text-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
