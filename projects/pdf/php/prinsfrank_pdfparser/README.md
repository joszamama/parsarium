# prinsfrank/pdfparser — PDF / PHP

Pinned release: `v4.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/prinsfrank-pdfparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php prinsfrank_pdfparser
python3 parsarium.py run pdf php prinsfrank_pdfparser controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php prinsfrank_pdfparser CORPUS_DIR runs/pdf-prinsfrank_pdfparser-replay
python3 parsarium.py afl build pdf php prinsfrank_pdfparser
python3 parsarium.py afl prepare pdf php prinsfrank_pdfparser runs/pdf-prinsfrank_pdfparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
