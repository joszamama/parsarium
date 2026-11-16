# openpdf — PDF / Java

Pinned release: `3.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/openpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java openpdf
python3 parsarium.py run pdf java openpdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java openpdf CORPUS_DIR runs/pdf-openpdf-replay
python3 parsarium.py afl build pdf java openpdf
python3 parsarium.py afl prepare pdf java openpdf runs/pdf-openpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
