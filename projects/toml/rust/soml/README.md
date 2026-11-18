# soml — TOML / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/soml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust soml
python3 parsarium.py run toml rust soml controls/toml/service-config.toml
python3 parsarium.py replay toml rust soml CORPUS_DIR runs/toml-soml-replay
python3 parsarium.py afl build toml rust soml
python3 parsarium.py afl prepare toml rust soml runs/toml-soml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** soml 0.2.0 parses with its own parser (src/de/parser.rs) and fills its own Table/Value types through serde; serde itself is outside the coverage and AFL++ scope. Only the soml crate is instrumented for AFL++.
