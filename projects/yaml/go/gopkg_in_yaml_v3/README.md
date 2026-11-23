# gopkg.in/yaml.v3 — YAML / Go

Pinned release: `v3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/gopkg-in-yaml-v3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go gopkg_in_yaml_v3
python3 parsarium.py run yaml go gopkg_in_yaml_v3 controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go gopkg_in_yaml_v3 CORPUS_DIR runs/yaml-gopkg_in_yaml_v3-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml go gopkg_in_yaml_v3
python3 parsarium.py afl prepare yaml go gopkg_in_yaml_v3 runs/yaml-gopkg_in_yaml_v3-afl --fandango 100
python3 parsarium.py afl run runs/yaml-gopkg_in_yaml_v3-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
