# cjson — JSON / C

Pinned release: `1.7.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/cjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c cjson
python3 parsarium.py run json c cjson controls/json/nested-object.json
python3 parsarium.py replay json c cjson CORPUS_DIR runs/json-cjson-replay
python3 parsarium.py afl build json c cjson
python3 parsarium.py afl prepare json c cjson runs/json-cjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
