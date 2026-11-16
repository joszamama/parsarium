# matplotlib — PNG / Python

Pinned release: `3.11.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/matplotlib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python matplotlib
python3 parsarium.py run png python matplotlib controls/png/red-green.png
python3 parsarium.py replay png python matplotlib CORPUS_DIR runs/png-matplotlib-replay
python3 parsarium.py afl build png python matplotlib
python3 parsarium.py afl prepare png python matplotlib runs/png-matplotlib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
