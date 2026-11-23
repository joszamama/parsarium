# JSON.parse — JSON / JavaScript

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/javascript/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json javascript stdlib_json_parse
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-object.json
python3 parsarium.py replay json javascript stdlib_json_parse CORPUS_DIR runs/json-stdlib_json_parse-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json javascript stdlib_json_parse
python3 parsarium.py afl prepare json javascript stdlib_json_parse runs/json-stdlib_json_parse-afl --fandango 100
python3 parsarium.py afl run runs/json-stdlib_json_parse-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
