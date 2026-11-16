# smalot/pdfparser — PDF / PHP

Pinned release: `v2.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/smalot-pdfparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php smalot_pdfparser
python3 parsarium.py run pdf php smalot_pdfparser controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php smalot_pdfparser CORPUS_DIR runs/pdf-smalot_pdfparser-replay
python3 parsarium.py afl build pdf php smalot_pdfparser
python3 parsarium.py afl prepare pdf php smalot_pdfparser runs/pdf-smalot_pdfparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
