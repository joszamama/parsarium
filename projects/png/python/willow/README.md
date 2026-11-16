# Willow — PNG / Python

Pinned release: `1.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/willow/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python willow
python3 parsarium.py run png python willow controls/png/red-green.png
python3 parsarium.py replay png python willow CORPUS_DIR runs/png-willow-replay
python3 parsarium.py afl build png python willow
python3 parsarium.py afl prepare png python willow runs/png-willow-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
