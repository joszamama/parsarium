# kabosu — TOML / Rust

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/kabosu/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust kabosu
python3 parsarium.py run toml rust kabosu controls/toml/service-config.toml
python3 parsarium.py replay toml rust kabosu CORPUS_DIR runs/toml-kabosu-replay
python3 parsarium.py afl build toml rust kabosu
python3 parsarium.py afl prepare toml rust kabosu runs/toml-kabosu-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** kabosu 0.2.1 parses TOML 1.0.0 with its own dependency-free lexer and parser into a span-carrying model. Only the kabosu crate is instrumented for AFL++.
