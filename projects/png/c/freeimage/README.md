# freeimage — PNG / C

Pinned release: `3.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/freeimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c freeimage
python3 parsarium.py run png c freeimage controls/png/red-green.png
python3 parsarium.py replay png c freeimage CORPUS_DIR runs/png-freeimage-replay
python3 parsarium.py afl build png c freeimage
python3 parsarium.py afl prepare png c freeimage runs/png-freeimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
