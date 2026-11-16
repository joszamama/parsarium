# pdfquery — PDF / Python

Pinned release: `0.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfquery/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfquery
python3 parsarium.py run pdf python pdfquery controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfquery CORPUS_DIR runs/pdf-pdfquery-replay
python3 parsarium.py afl build pdf python pdfquery
python3 parsarium.py afl prepare pdf python pdfquery runs/pdf-pdfquery-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
