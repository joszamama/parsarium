# json-c — JSON / C

Pinned release: `0.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/json-c/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c json-c
python3 parsarium.py run json c json-c controls/json/nested-object.json
python3 parsarium.py replay json c json-c CORPUS_DIR runs/json-json-c-replay
python3 parsarium.py afl build json c json-c
python3 parsarium.py afl prepare json c json-c runs/json-json-c-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
