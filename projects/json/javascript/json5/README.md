# json5 — JSON / JavaScript

Pinned release: `2.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/json5/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript json5
python3 parsarium.py run json javascript json5 controls/json/nested-object.json
python3 parsarium.py replay json javascript json5 CORPUS_DIR runs/json-json5-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json javascript json5
python3 parsarium.py afl prepare json javascript json5 runs/json-json5-afl --fandango 100
python3 parsarium.py afl run runs/json-json5-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
