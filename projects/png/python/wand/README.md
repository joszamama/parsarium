# Wand — PNG / Python

Pinned release: `0.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/wand/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python wand
python3 parsarium.py run png python wand controls/png/red-green.png
python3 parsarium.py replay png python wand CORPUS_DIR runs/png-wand-replay
python3 parsarium.py afl build png python wand
python3 parsarium.py afl prepare png python wand runs/png-wand-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
