# toml_dom — TOML / Rust

Pinned release: `0.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/toml-dom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust toml_dom
python3 parsarium.py run toml rust toml_dom controls/toml/service-config.toml
python3 parsarium.py replay toml rust toml_dom CORPUS_DIR runs/toml-toml_dom-replay
python3 parsarium.py afl build toml rust toml_dom
python3 parsarium.py afl prepare toml rust toml_dom runs/toml-toml_dom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** toml_dom 0.6.0 parses plain TOML with its own parser (src/parser.rs) into a format-preserving CST and DOM; its ATML mode is not used. Only the toml_dom crate is instrumented for AFL++.
