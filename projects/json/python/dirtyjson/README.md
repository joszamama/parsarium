# dirtyjson — JSON / Python

Pinned release: `1.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/dirtyjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python dirtyjson
python3 parsarium.py run json python dirtyjson controls/json/structure.json
python3 parsarium.py replay json python dirtyjson CORPUS_DIR runs/json-dirtyjson-replay
python3 parsarium.py afl build json python dirtyjson
python3 parsarium.py afl prepare json python dirtyjson runs/json-dirtyjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
