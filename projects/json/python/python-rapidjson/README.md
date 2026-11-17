# python-rapidjson — JSON / Python

Pinned release: `1.26`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/python-rapidjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python python-rapidjson
python3 parsarium.py run json python python-rapidjson controls/json/structure.json
python3 parsarium.py replay json python python-rapidjson CORPUS_DIR runs/json-python-rapidjson-replay
python3 parsarium.py afl build json python python-rapidjson
python3 parsarium.py afl prepare json python python-rapidjson runs/json-python-rapidjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
