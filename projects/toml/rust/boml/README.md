# boml — TOML / Rust

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/boml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust boml
python3 parsarium.py run toml rust boml controls/toml/service-config.toml
python3 parsarium.py replay toml rust boml CORPUS_DIR runs/toml-boml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust boml
python3 parsarium.py afl prepare toml rust boml runs/toml-boml-afl --fandango 100
python3 parsarium.py afl run runs/toml-boml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** boml 2.0.1 has no dependencies: it scans the text, parses keys, tables and values itself and returns a TomlTable of TomlValue variants (Integer, Float, String, Boolean, OffsetDateTime, DateTime, Date, Time, Array, Table). Only the boml crate is instrumented for AFL++.
