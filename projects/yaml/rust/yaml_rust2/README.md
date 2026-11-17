# yaml-rust2 — YAML / Rust

Pinned release: `0.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/yaml-rust2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust yaml_rust2
python3 parsarium.py run yaml rust yaml_rust2 controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust yaml_rust2 CORPUS_DIR runs/yaml-yaml_rust2-replay
python3 parsarium.py afl build yaml rust yaml_rust2
python3 parsarium.py afl prepare yaml rust yaml_rust2 runs/yaml-yaml_rust2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** yaml_rust2::YamlLoader::load_from_str on local UTF-8 text with exactly one document required. yaml-rust2 is the maintained fork of yaml-rust (yaml-rust lineage) with its own scanner, parser and loader; the loader replaces aliases with the anchored node and resolves plain scalars itself (Real values keep their source text and are converted with Yaml::as_f64 by the harness). Hash keys must be strings for the typed tree. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
