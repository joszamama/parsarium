# serde-saphyr — YAML / Rust

Pinned release: `2.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/serde-saphyr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust serde_saphyr
python3 parsarium.py run yaml rust serde_saphyr controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust serde_saphyr CORPUS_DIR runs/yaml-serde_saphyr-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust serde_saphyr
python3 parsarium.py afl prepare yaml rust serde_saphyr runs/yaml-serde_saphyr-afl --fandango 100
python3 parsarium.py afl run runs/yaml-serde_saphyr-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** serde_saphyr::from_str into the harness's order-keeping Deserialize type (deserialize_any visitor) on one YAML document from local UTF-8 text. serde-saphyr has no Value type of its own; it replays aliases and resolves plain scalars itself (bool, int, float, null, otherwise str; quoted and block scalars stay strings). Its event parser is granit-parser, a fork of saphyr-parser (yaml-rust lineage). Mapping keys must be strings. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
