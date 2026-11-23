# yaml-rust — YAML / Rust

Pinned release: `0.4.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/yaml-rust/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust yaml_rust
python3 parsarium.py run yaml rust yaml_rust controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust yaml_rust CORPUS_DIR runs/yaml-yaml_rust-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust yaml_rust
python3 parsarium.py afl prepare yaml rust yaml_rust runs/yaml-yaml_rust-afl --fandango 100
python3 parsarium.py afl run runs/yaml-yaml_rust-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** yaml_rust::YamlLoader::load_from_str on local UTF-8 text with exactly one document required. yaml-rust has its own pure-Rust scanner, parser and loader; the loader replaces aliases with the anchored node and resolves plain scalars itself (Real values keep their source text and are converted with Yaml::as_f64 by the harness). Hash keys must be strings for the typed tree. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
