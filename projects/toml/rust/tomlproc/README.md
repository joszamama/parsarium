# tomlproc — TOML / Rust

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/rust/tomlproc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml rust tomlproc
python3 parsarium.py run toml rust tomlproc controls/toml/service-config.toml
python3 parsarium.py replay toml rust tomlproc CORPUS_DIR runs/toml-tomlproc-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml rust tomlproc
python3 parsarium.py afl prepare toml rust tomlproc runs/toml-tomlproc-afl --fandango 100
python3 parsarium.py afl run runs/toml-tomlproc-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** tomlproc 0.1.2 parses with its own dependency-free parser (src/parser.rs) into a plain value tree with its own Datetime type (src/datetime.rs). Only the tomlproc crate is instrumented for AFL++.
