# jackson-core — JSON / Java

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/jackson-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java jackson_core
python3 parsarium.py run json java jackson_core controls/json/nested-object.json
python3 parsarium.py replay json java jackson_core CORPUS_DIR runs/json-jackson_core-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json java jackson_core
python3 parsarium.py afl prepare json java jackson_core runs/json-jackson_core-afl --fandango 100
python3 parsarium.py afl run runs/json-jackson_core-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
