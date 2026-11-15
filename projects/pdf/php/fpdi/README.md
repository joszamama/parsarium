# setasign/fpdi — PDF / PHP

Pinned release: `v2.6.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/setasign-fpdi/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php fpdi
python3 parsarium.py run pdf php fpdi controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php fpdi CORPUS_DIR runs/pdf-fpdi-replay
python3 parsarium.py afl build pdf php fpdi
python3 parsarium.py afl prepare pdf php fpdi runs/pdf-fpdi-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
