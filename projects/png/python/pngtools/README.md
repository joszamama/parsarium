# pngtools — PNG / Python

Pinned release: `1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pngtools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pngtools
python3 parsarium.py run png python pngtools controls/png/red-green.png
python3 parsarium.py replay png python pngtools CORPUS_DIR runs/png-pngtools-replay
python3 parsarium.py afl build png python pngtools
python3 parsarium.py afl prepare png python pngtools runs/png-pngtools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
