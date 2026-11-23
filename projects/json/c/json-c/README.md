# json-c — JSON / C

Pinned release: `0.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/json-c/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c json-c
python3 parsarium.py run json c json-c controls/json/nested-object.json
python3 parsarium.py replay json c json-c CORPUS_DIR runs/json-json-c-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json c json-c
python3 parsarium.py afl prepare json c json-c runs/json-json-c-afl --fandango 100
python3 parsarium.py afl run runs/json-json-c-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
