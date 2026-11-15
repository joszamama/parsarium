# apng — PNG / Python

Pinned release: `0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/apng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python apng
python3 parsarium.py run png python apng controls/png/red-green.png
python3 parsarium.py replay png python apng CORPUS_DIR runs/png-apng-replay
python3 parsarium.py afl build png python apng
python3 parsarium.py afl prepare png python apng runs/png-apng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
