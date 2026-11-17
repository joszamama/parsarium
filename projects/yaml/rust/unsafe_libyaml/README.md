# unsafe-libyaml — YAML / Rust

Pinned release: `0.2.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/unsafe-libyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust unsafe_libyaml
python3 parsarium.py run yaml rust unsafe_libyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust unsafe_libyaml CORPUS_DIR runs/yaml-unsafe_libyaml-replay
python3 parsarium.py afl build yaml rust unsafe_libyaml
python3 parsarium.py afl prepare yaml rust unsafe_libyaml runs/yaml-unsafe_libyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** unsafe-libyaml's documented libyaml document API (yaml_parser_initialize, yaml_parser_set_input_string, yaml_parser_load, yaml_document_get_root_node/get_node) on local UTF-8 bytes, with exactly one document required. unsafe-libyaml is a c2rust translation of libyaml and the same crate the selected serde_yaml path drives, so this path is in the libyaml family. libyaml's loader points aliases at the anchored node and reports scalar style but does not resolve plain scalars: the harness types plain scalars with the YAML 1.2 core-schema patterns (null, bool, int, float, otherwise str), as the C libyaml harness does. Mapping keys must be scalars. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
