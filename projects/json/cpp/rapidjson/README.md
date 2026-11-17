# RapidJSON — JSON / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/rapidjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp rapidjson
python3 parsarium.py run json cpp rapidjson controls/json/nested-object.json
python3 parsarium.py replay json cpp rapidjson CORPUS_DIR runs/json-rapidjson-replay
python3 parsarium.py afl build json cpp rapidjson
python3 parsarium.py afl prepare json cpp rapidjson runs/json-rapidjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
