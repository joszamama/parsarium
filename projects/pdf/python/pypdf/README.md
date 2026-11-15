# pypdf — PDF / Python

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/python/pypdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf python pypdf
python3 parsarium.py run pdf python pypdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf python pypdf CORPUS_DIR runs/pdf-pypdf-replay
python3 parsarium.py afl build pdf python pypdf
python3 parsarium.py afl prepare pdf python pypdf runs/pdf-pypdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
