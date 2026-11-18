# json.h — JSON / C

Pinned release: `pre-ai`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/json-h/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c json-h
python3 parsarium.py run json c json-h controls/json/nested-object.json
python3 parsarium.py replay json c json-h CORPUS_DIR runs/json-json-h-replay
python3 parsarium.py afl build json c json-h
python3 parsarium.py afl prepare json c json-h runs/json-json-h-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
