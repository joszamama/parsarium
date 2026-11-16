# rasgapdf — PDF / JavaScript

Pinned release: `0.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/rasgapdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript rasgapdf
python3 parsarium.py run pdf javascript rasgapdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript rasgapdf CORPUS_DIR runs/pdf-rasgapdf-replay
python3 parsarium.py afl build pdf javascript rasgapdf
python3 parsarium.py afl prepare pdf javascript rasgapdf runs/pdf-rasgapdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
