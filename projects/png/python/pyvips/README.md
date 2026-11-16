# pyvips — PNG / Python

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pyvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pyvips
python3 parsarium.py run png python pyvips controls/png/red-green.png
python3 parsarium.py replay png python pyvips CORPUS_DIR runs/png-pyvips-replay
python3 parsarium.py afl build png python pyvips
python3 parsarium.py afl prepare png python pyvips runs/png-pyvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
