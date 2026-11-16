# clawpdf — PDF / JavaScript

Pinned release: `0.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/clawpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript clawpdf
python3 parsarium.py run pdf javascript clawpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript clawpdf CORPUS_DIR runs/pdf-clawpdf-replay
python3 parsarium.py afl build pdf javascript clawpdf
python3 parsarium.py afl prepare pdf javascript clawpdf runs/pdf-clawpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
