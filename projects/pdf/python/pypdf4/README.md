# PyPDF4 — PDF / Python

Pinned release: `1.27.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pypdf4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pypdf4
python3 parsarium.py run pdf python pypdf4 controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pypdf4 CORPUS_DIR runs/pdf-pypdf4-replay
python3 parsarium.py afl build pdf python pypdf4
python3 parsarium.py afl prepare pdf python pypdf4 runs/pdf-pypdf4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
