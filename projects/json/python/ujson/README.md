# ujson — JSON / Python

Pinned release: `6.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/ujson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python ujson
python3 parsarium.py run json python ujson controls/json/structure.json
python3 parsarium.py replay json python ujson CORPUS_DIR runs/json-ujson-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json python ujson
python3 parsarium.py afl prepare json python ujson runs/json-ujson-afl --fandango 100
python3 parsarium.py afl run runs/json-ujson-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
