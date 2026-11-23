# granit-parser — YAML / Rust

Pinned release: `2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/rust/granit-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml rust granit_parser
python3 parsarium.py run yaml rust granit_parser controls/yaml/catalog.yaml
python3 parsarium.py replay yaml rust granit_parser CORPUS_DIR runs/yaml-granit_parser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml rust granit_parser
python3 parsarium.py afl prepare yaml rust granit_parser runs/yaml-granit_parser-afl --fandango 100
python3 parsarium.py afl run runs/yaml-granit_parser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** granit_parser::Parser::new_from_str event stream on local UTF-8 text with exactly one document required; the harness assembles the typed tree from the events, copies the anchored node for each Alias event, skips Comment/Anchor metadata events, and types plain scalars with the YAML 1.2 core-schema patterns (null, bool, int, float, otherwise str) as the C and C++ YAML harnesses do; quoted and block scalars are str. granit-parser is a fork of saphyr-parser (yaml-rust lineage). Mapping keys must be untagged scalars. The schema-neutral controls do not test tags, merge keys, multi-document streams or YAML 1.1-only scalars.
