# saphyr — YAML / Rust

Pinned release: `0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/saphyr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust saphyr
python3 parsarium.py run yaml rust saphyr controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust saphyr CORPUS_DIR runs/yaml-saphyr-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust saphyr
python3 parsarium.py afl prepare yaml rust saphyr runs/yaml-saphyr-afl --fandango 100
python3 parsarium.py afl run runs/yaml-saphyr-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** saphyr::Yaml::load_from_str (LoadableYamlNode) on local UTF-8 text with exactly one document required. saphyr's YamlLoader builds the Yaml tree from saphyr-parser events, copies the anchored node for aliases and resolves plain scalars into Scalar values itself (early_parse default); mappings are hashlink LinkedHashMaps in source order. saphyr-parser is also a selected path (yaml-rust lineage). Mapping keys must be strings for the typed tree and explicit tags are rejected by the harness. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
