# pdfnaut — PDF / Python

Pinned release: `0.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pdfnaut/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pdfnaut
python3 parsarium.py run pdf python pdfnaut controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pdfnaut CORPUS_DIR runs/pdf-pdfnaut-replay
python3 parsarium.py afl build pdf python pdfnaut
python3 parsarium.py afl prepare pdf python pdfnaut runs/pdf-pdfnaut-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
