# fkyaml — YAML / C++

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/cpp/fkyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml cpp fkyaml
python3 parsarium.py run yaml cpp fkyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml cpp fkyaml CORPUS_DIR runs/yaml-fkyaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml cpp fkyaml
python3 parsarium.py afl prepare yaml cpp fkyaml runs/yaml-fkyaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-fkyaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
