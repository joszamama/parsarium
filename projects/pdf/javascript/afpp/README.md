# afpp — PDF / JavaScript

Pinned release: `3.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/afpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript afpp
python3 parsarium.py run pdf javascript afpp controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript afpp CORPUS_DIR runs/pdf-afpp-replay
python3 parsarium.py afl build pdf javascript afpp
python3 parsarium.py afl prepare pdf javascript afpp runs/pdf-afpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
