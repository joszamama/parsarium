# @decimalturn/toml-patch — TOML / JavaScript

Pinned release: `3.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/decimalturn-toml-patch/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript decimalturn_toml_patch
python3 parsarium.py run toml javascript decimalturn_toml_patch controls/toml/service-config.toml
python3 parsarium.py replay toml javascript decimalturn_toml_patch CORPUS_DIR runs/toml-decimalturn_toml_patch-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml javascript decimalturn_toml_patch
python3 parsarium.py afl prepare toml javascript decimalturn_toml_patch runs/toml-decimalturn_toml_patch-afl --fandango 100
python3 parsarium.py afl run runs/toml-decimalturn_toml_patch-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
