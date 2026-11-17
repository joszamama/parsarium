# yyjson — JSON / C

Pinned release: `0.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/yyjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c yyjson
python3 parsarium.py run json c yyjson controls/json/nested-object.json
python3 parsarium.py replay json c yyjson CORPUS_DIR runs/json-yyjson-replay
python3 parsarium.py afl build json c yyjson
python3 parsarium.py afl prepare json c yyjson runs/json-yyjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
