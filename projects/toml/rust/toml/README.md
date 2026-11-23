# toml — TOML / Rust

Pinned release: `1.2.1+spec-1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust toml
python3 parsarium.py run toml rust toml controls/toml/service-config.toml
python3 parsarium.py replay toml rust toml CORPUS_DIR runs/toml-toml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust toml
python3 parsarium.py afl prepare toml rust toml runs/toml-toml-afl --fandango 100
python3 parsarium.py afl run runs/toml-toml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** toml 1.2.1 has no parser of its own below the event level: toml::from_str lexes and parses through toml_parser 1.1.5 (Source::lex, parse_document events) and toml builds DeTable/DeValue and the toml::Table/Value tree from those events. toml_edit 0.25.19 drives the same toml_parser crate, so the two paths share the toml_parser family. Datetime values are toml_datetime 1.1.3 structs (date, time, offset parts); the harness converts offset date-times to the UTC instant arithmetically. Feature defaults: preserve_order is off, so tables are BTreeMap-backed.
