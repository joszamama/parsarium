# saphyr-parser — YAML / Rust

Pinned release: `0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/saphyr-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust saphyr_parser
python3 parsarium.py run yaml rust saphyr_parser controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust saphyr_parser CORPUS_DIR runs/yaml-saphyr_parser-replay
python3 parsarium.py afl build yaml rust saphyr_parser
python3 parsarium.py afl prepare yaml rust saphyr_parser runs/yaml-saphyr_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** saphyr_parser::Parser::new_from_str event stream on local UTF-8 text with exactly one document required; the harness assembles the typed tree from the events, copies the anchored node for each Alias event, and types plain scalars with the YAML 1.2 core-schema patterns (null, bool, int, float, otherwise str) as the C and C++ YAML harnesses do; quoted and block scalars are str. saphyr-parser is the parser half of saphyr, which continues yaml-rust2 (yaml-rust lineage). Mapping keys must be untagged scalars. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
