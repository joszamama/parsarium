# hjson — JSON / Python

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/hjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python hjson
python3 parsarium.py run json python hjson controls/json/structure.json
python3 parsarium.py replay json python hjson CORPUS_DIR runs/json-hjson-replay
python3 parsarium.py afl build json python hjson
python3 parsarium.py afl prepare json python hjson runs/json-hjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
