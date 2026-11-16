# gufy/pdftohtml-php — PDF / PHP

Pinned release: `v2.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/gufy-pdftohtml-php/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php gufy_pdftohtml_php
python3 parsarium.py run pdf php gufy_pdftohtml_php controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php gufy_pdftohtml_php CORPUS_DIR runs/pdf-gufy_pdftohtml_php-replay
python3 parsarium.py afl build pdf php gufy_pdftohtml_php
python3 parsarium.py afl prepare pdf php gufy_pdftohtml_php runs/pdf-gufy_pdftohtml_php-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
