# pdftotext — PDF / Python

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdftotext/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdftotext
python3 parsarium.py run pdf python pdftotext controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdftotext CORPUS_DIR runs/pdf-pdftotext-replay
python3 parsarium.py afl build pdf python pdftotext
python3 parsarium.py afl prepare pdf python pdftotext runs/pdf-pdftotext-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
