# toml-spanner — TOML / Rust

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/toml-spanner/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust toml_spanner
python3 parsarium.py run toml rust toml_spanner controls/toml/service-config.toml
python3 parsarium.py replay toml rust toml_spanner CORPUS_DIR runs/toml-toml_spanner-replay
python3 parsarium.py afl build toml rust toml_spanner
python3 parsarium.py afl prepare toml rust toml_spanner runs/toml-toml_spanner-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** toml-spanner 1.0.3 parses into an arena-allocated, span-preserving Item tree with its own parser (src/parser.rs) and date-time type (src/time.rs). Only the toml_spanner crate is instrumented for AFL++.
