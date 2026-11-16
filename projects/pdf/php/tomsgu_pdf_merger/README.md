# tomsgu/pdf-merger — PDF / PHP

Pinned release: `v0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/tomsgu-pdf-merger/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php tomsgu_pdf_merger
python3 parsarium.py run pdf php tomsgu_pdf_merger controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php tomsgu_pdf_merger CORPUS_DIR runs/pdf-tomsgu_pdf_merger-replay
python3 parsarium.py afl build pdf php tomsgu_pdf_merger
python3 parsarium.py afl prepare pdf php tomsgu_pdf_merger runs/pdf-tomsgu_pdf_merger-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
