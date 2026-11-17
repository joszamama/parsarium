# toml_edit — TOML / Rust

Pinned release: `0.25.19+spec-1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/toml-edit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust toml_edit
python3 parsarium.py run toml rust toml_edit controls/toml/service-config.toml
python3 parsarium.py replay toml rust toml_edit CORPUS_DIR runs/toml-toml_edit-replay
python3 parsarium.py afl build toml rust toml_edit
python3 parsarium.py afl prepare toml rust toml_edit runs/toml-toml_edit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** toml_edit 0.25.19 lexes and parses through toml_parser 1.1.5 (the same crate toml 1.2.1 drives) and builds its own format-preserving Document/Item/Value tree with decor and spans; the two paths share the toml_parser family. Only decoded values are observed, not the preserved formatting. Datetime values are toml_datetime 1.1.3 structs; the harness converts offset date-times to the UTC instant arithmetically. Tables are IndexMaps with std RandomState hashing.
