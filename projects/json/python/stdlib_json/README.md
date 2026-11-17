# json — JSON / Python

Pinned release: `3.14.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json python stdlib_json
python3 parsarium.py run json python stdlib_json controls/json/structure.json
python3 parsarium.py replay json python stdlib_json CORPUS_DIR runs/json-stdlib_json-replay
python3 parsarium.py afl build json python stdlib_json
python3 parsarium.py afl prepare json python stdlib_json runs/json-stdlib_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
