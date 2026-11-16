# pdfx — PDF / Python

Pinned release: `1.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfx
python3 parsarium.py run pdf python pdfx controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfx CORPUS_DIR runs/pdf-pdfx-replay
python3 parsarium.py afl build pdf python pdfx
python3 parsarium.py afl prepare pdf python pdfx runs/pdf-pdfx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
