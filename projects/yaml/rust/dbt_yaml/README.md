# dbt-yaml — YAML / Rust

Pinned release: `0.10.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/dbt-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust dbt_yaml
python3 parsarium.py run yaml rust dbt_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust dbt_yaml CORPUS_DIR runs/yaml-dbt_yaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust dbt_yaml
python3 parsarium.py afl prepare yaml rust dbt_yaml runs/yaml-dbt_yaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-dbt_yaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** dbt_yaml::from_str::<dbt_yaml::Value> on one YAML document from local UTF-8 text with default features (no yaml_11). dbt-yaml is dbt Labs' fork of serde_yaml with a span-carrying Value and reworked deserializer, driving the same unsafe-libyaml 0.2.11 crate (libyaml family); it expands aliases and resolves plain scalars itself. Spans are ignored by the harness, mapping keys must be strings and explicit tags are rejected. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
