# boml — TOML / Rust

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/boml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust boml
python3 parsarium.py run toml rust boml controls/toml/service-config.toml
python3 parsarium.py replay toml rust boml CORPUS_DIR runs/toml-boml-replay
python3 parsarium.py afl build toml rust boml
python3 parsarium.py afl prepare toml rust boml runs/toml-boml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** boml 2.0.1 has no dependencies: it scans the text, parses keys, tables and values itself and returns a TomlTable of TomlValue variants (Integer, Float, String, Boolean, OffsetDateTime, DateTime, Date, Time, Array, Table). Only the boml crate is instrumented for AFL++.
