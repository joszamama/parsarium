# serde_yaml — YAML / Rust

Pinned release: `0.9.34+deprecated`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/serde-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust serde_yaml
python3 parsarium.py run yaml rust serde_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust serde_yaml CORPUS_DIR runs/yaml-serde_yaml-replay
python3 parsarium.py afl build yaml rust serde_yaml
python3 parsarium.py afl prepare yaml rust serde_yaml runs/yaml-serde_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** serde_yaml::from_str::<Value> on one YAML document from local UTF-8 text. serde_yaml expands aliases and resolves plain scalars itself (true/false, null/~, decimal ints and floats); the event scanner and parser are unsafe-libyaml, a c2rust translation of libyaml, so this path is in the libyaml family. Mapping keys must be strings for the typed tree and explicit tags are rejected by the harness. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
