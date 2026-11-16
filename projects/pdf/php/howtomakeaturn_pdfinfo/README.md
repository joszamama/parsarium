# howtomakeaturn/pdfinfo — PDF / PHP

Pinned release: `1.1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/howtomakeaturn-pdfinfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php howtomakeaturn_pdfinfo
python3 parsarium.py run pdf php howtomakeaturn_pdfinfo controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php howtomakeaturn_pdfinfo CORPUS_DIR runs/pdf-howtomakeaturn_pdfinfo-replay
python3 parsarium.py afl build pdf php howtomakeaturn_pdfinfo
python3 parsarium.py afl prepare pdf php howtomakeaturn_pdfinfo runs/pdf-howtomakeaturn_pdfinfo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
