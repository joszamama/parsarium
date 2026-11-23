# cjson — JSON / C

Pinned release: `1.7.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/cjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c cjson
python3 parsarium.py run json c cjson controls/json/nested-object.json
python3 parsarium.py replay json c cjson CORPUS_DIR runs/json-cjson-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json c cjson
python3 parsarium.py afl prepare json c cjson runs/json-cjson-afl --fandango 100
python3 parsarium.py afl run runs/json-cjson-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
