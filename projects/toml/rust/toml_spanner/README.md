# toml-spanner — TOML / Rust

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/toml-spanner/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust toml_spanner
python3 parsarium.py run toml rust toml_spanner controls/toml/service-config.toml
python3 parsarium.py replay toml rust toml_spanner CORPUS_DIR runs/toml-toml_spanner-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust toml_spanner
python3 parsarium.py afl prepare toml rust toml_spanner runs/toml-toml_spanner-afl --fandango 100
python3 parsarium.py afl run runs/toml-toml_spanner-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** toml-spanner 1.0.3 parses into an arena-allocated, span-preserving Item tree with its own parser (src/parser.rs) and date-time type (src/time.rs). Only the toml_spanner crate is instrumented for AFL++.
