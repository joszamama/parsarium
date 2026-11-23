# noyalib — YAML / Rust

Pinned release: `0.0.62`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/noyalib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust noyalib
python3 parsarium.py run yaml rust noyalib controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust noyalib CORPUS_DIR runs/yaml-noyalib-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust noyalib
python3 parsarium.py afl prepare yaml rust noyalib runs/yaml-noyalib-afl --fandango 100
python3 parsarium.py afl run runs/yaml-noyalib-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** noyalib::from_str::<noyalib::Value> on one YAML document from local UTF-8 text with default features. noyalib has its own pure-Rust scanner, parser and loader (no libyaml or yaml-rust code); it expands aliases and resolves plain scalars itself, and its Mapping is an IndexMap in source order with String keys. Explicit tags are rejected by the harness. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
