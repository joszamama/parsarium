# leptonica — PNG / C

Pinned release: `1.87.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/leptonica/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c leptonica
python3 parsarium.py run png c leptonica controls/png/red-green.png
python3 parsarium.py replay png c leptonica CORPUS_DIR runs/png-leptonica-replay
python3 parsarium.py afl build png c leptonica
python3 parsarium.py afl prepare png c leptonica runs/png-leptonica-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
