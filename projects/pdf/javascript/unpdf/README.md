# unpdf — PDF / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/unpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript unpdf
python3 parsarium.py run pdf javascript unpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript unpdf CORPUS_DIR runs/pdf-unpdf-replay
python3 parsarium.py afl build pdf javascript unpdf
python3 parsarium.py afl prepare pdf javascript unpdf runs/pdf-unpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
