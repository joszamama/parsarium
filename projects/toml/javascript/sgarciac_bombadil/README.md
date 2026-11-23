# @sgarciac/bombadil — TOML / JavaScript

Pinned release: `2.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/sgarciac-bombadil/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript sgarciac_bombadil
python3 parsarium.py run toml javascript sgarciac_bombadil controls/toml/service-config.toml
python3 parsarium.py replay toml javascript sgarciac_bombadil CORPUS_DIR runs/toml-sgarciac_bombadil-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml javascript sgarciac_bombadil
python3 parsarium.py afl prepare toml javascript sgarciac_bombadil runs/toml-sgarciac_bombadil-afl --fandango 100
python3 parsarium.py afl run runs/toml-sgarciac_bombadil-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
