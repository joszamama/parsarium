# boundwize/jsonrecast — JSON / PHP

Pinned release: `1.0.37`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/boundwize-jsonrecast/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php boundwize_jsonrecast
python3 parsarium.py run json php boundwize_jsonrecast controls/json/nested-object.json
python3 parsarium.py replay json php boundwize_jsonrecast CORPUS_DIR runs/json-boundwize_jsonrecast-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json php boundwize_jsonrecast
python3 parsarium.py afl prepare json php boundwize_jsonrecast runs/json-boundwize_jsonrecast-afl --fandango 100
python3 parsarium.py afl run runs/json-boundwize_jsonrecast-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
