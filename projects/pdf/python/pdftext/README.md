# pdftext — PDF / Python

Pinned release: `0.7.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdftext/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdftext
python3 parsarium.py run pdf python pdftext controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdftext CORPUS_DIR runs/pdf-pdftext-replay
python3 parsarium.py afl build pdf python pdftext
python3 parsarium.py afl prepare pdf python pdftext runs/pdf-pdftext-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
