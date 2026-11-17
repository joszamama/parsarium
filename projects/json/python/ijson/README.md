# ijson — JSON / Python

Pinned release: `3.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/ijson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python ijson
python3 parsarium.py run json python ijson controls/json/structure.json
python3 parsarium.py replay json python ijson CORPUS_DIR runs/json-ijson-replay
python3 parsarium.py afl build json python ijson
python3 parsarium.py afl prepare json python ijson runs/json-ijson-afl
python3 scripts/verify_python_json_ijson_feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness uses the default `yajl2_c` backend and fails on any other. The image builds the sdist with yajl embedded, so it is not the official Linux wheel's linkage.
