# orjson — JSON / Python

Pinned release: `3.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/orjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python orjson
python3 parsarium.py run json python orjson controls/json/structure.json
python3 parsarium.py replay json python orjson CORPUS_DIR runs/json-orjson-replay
python3 parsarium.py afl build json python orjson
python3 parsarium.py afl prepare json python orjson runs/json-orjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
