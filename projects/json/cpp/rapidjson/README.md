# RapidJSON — JSON / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/rapidjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp rapidjson
python3 parsarium.py run json cpp rapidjson controls/json/nested-object.json
python3 parsarium.py replay json cpp rapidjson CORPUS_DIR runs/json-rapidjson-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json cpp rapidjson
python3 parsarium.py afl prepare json cpp rapidjson runs/json-rapidjson-afl --fandango 100
python3 parsarium.py afl run runs/json-rapidjson-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
