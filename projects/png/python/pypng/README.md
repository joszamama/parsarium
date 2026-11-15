# pypng — PNG / Python

Pinned release: `0.20220715.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pypng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pypng
python3 parsarium.py run png python pypng controls/png/red-green.png
python3 parsarium.py replay png python pypng CORPUS_DIR runs/png-pypng-replay
python3 parsarium.py afl build png python pypng
python3 parsarium.py afl prepare png python pypng runs/png-pypng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
