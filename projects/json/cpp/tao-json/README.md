# taoJSON — JSON / C++

Pinned release: `1.0.0-beta.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/taojson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp tao-json
python3 parsarium.py run json cpp tao-json controls/json/nested-object.json
python3 parsarium.py replay json cpp tao-json CORPUS_DIR runs/json-tao-json-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json cpp tao-json
python3 parsarium.py afl prepare json cpp tao-json runs/json-tao-json-afl --fandango 100
python3 parsarium.py afl run runs/json-tao-json-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
