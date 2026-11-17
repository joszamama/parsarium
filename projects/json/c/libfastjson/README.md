# libfastjson — JSON / C

Pinned release: `1.2609.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/libfastjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c libfastjson
python3 parsarium.py run json c libfastjson controls/json/nested-object.json
python3 parsarium.py replay json c libfastjson CORPUS_DIR runs/json-libfastjson-replay
python3 parsarium.py afl build json c libfastjson
python3 parsarium.py afl prepare json c libfastjson runs/json-libfastjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
