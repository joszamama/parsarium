# json-parser — JSON / C

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/json-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c json-parser
python3 parsarium.py run json c json-parser controls/json/nested-object.json
python3 parsarium.py replay json c json-parser CORPUS_DIR runs/json-json-parser-replay
python3 parsarium.py afl build json c json-parser
python3 parsarium.py afl prepare json c json-parser runs/json-json-parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
