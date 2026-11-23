# soml — TOML / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/soml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust soml
python3 parsarium.py run toml rust soml controls/toml/service-config.toml
python3 parsarium.py replay toml rust soml CORPUS_DIR runs/toml-soml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust soml
python3 parsarium.py afl prepare toml rust soml runs/toml-soml-afl --fandango 100
python3 parsarium.py afl run runs/toml-soml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** soml 0.2.0 parses with its own parser (src/de/parser.rs) and fills its own Table/Value types through serde; serde itself is outside the coverage and AFL++ scope. Only the soml crate is instrumented for AFL++.
