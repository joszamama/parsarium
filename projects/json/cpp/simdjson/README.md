# simdjson — JSON / C++

Pinned release: `5.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/simdjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp simdjson
python3 parsarium.py run json cpp simdjson controls/json/nested-object.json
python3 parsarium.py replay json cpp simdjson CORPUS_DIR runs/json-simdjson-replay
python3 parsarium.py afl build json cpp simdjson
python3 parsarium.py afl prepare json cpp simdjson runs/json-simdjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
