# PyYAML — YAML / Python

Pinned release: `6.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/pyyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python pyyaml
python3 parsarium.py run yaml python pyyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python pyyaml CORPUS_DIR runs/yaml-pyyaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml python pyyaml
python3 parsarium.py afl prepare yaml python pyyaml runs/yaml-pyyaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-pyyaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
