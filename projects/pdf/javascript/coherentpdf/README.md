# coherentpdf — PDF / JavaScript

Pinned release: `2.5.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/coherentpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript coherentpdf
python3 parsarium.py run pdf javascript coherentpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript coherentpdf CORPUS_DIR runs/pdf-coherentpdf-replay
python3 parsarium.py afl build pdf javascript coherentpdf
python3 parsarium.py afl prepare pdf javascript coherentpdf runs/pdf-coherentpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
