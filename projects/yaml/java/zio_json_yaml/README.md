# zio-json-yaml — YAML / Java

Pinned release: `1.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/zio-json-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java zio_json_yaml
python3 parsarium.py run yaml java zio_json_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java zio_json_yaml CORPUS_DIR runs/yaml-zio_json_yaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml java zio_json_yaml
python3 parsarium.py afl prepare yaml java zio_json_yaml runs/yaml-zio_json_yaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-zio_json_yaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
