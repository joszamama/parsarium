# ruamel.yaml.clib — YAML / Python

Pinned release: `0.2.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/ruamel-yaml-clib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python ruamel_yaml_clib
python3 parsarium.py run yaml python ruamel_yaml_clib controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python ruamel_yaml_clib CORPUS_DIR runs/yaml-ruamel_yaml_clib-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml python ruamel_yaml_clib
python3 parsarium.py afl prepare yaml python ruamel_yaml_clib runs/yaml-ruamel_yaml_clib-afl --fandango 100
python3 parsarium.py afl run runs/yaml-ruamel_yaml_clib-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
