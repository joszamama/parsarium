# openpdf — PNG / Java

Pinned release: `3.0.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/openpdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java openpdf
python3 parsarium.py run png java openpdf controls/png/red-green.png
python3 parsarium.py replay png java openpdf CORPUS_DIR runs/png-openpdf-replay
python3 parsarium.py afl build png java openpdf
python3 parsarium.py afl prepare png java openpdf runs/png-openpdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
