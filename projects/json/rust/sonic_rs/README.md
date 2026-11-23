# sonic-rs — JSON / Rust

Pinned release: `0.5.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/sonic-rs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust sonic_rs
python3 parsarium.py run json rust sonic_rs controls/json/nested-object.json
python3 parsarium.py replay json rust sonic_rs CORPUS_DIR runs/json-sonic_rs-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json rust sonic_rs
python3 parsarium.py afl prepare json rust sonic_rs runs/json-sonic_rs-afl --fandango 100
python3 parsarium.py afl run runs/json-sonic_rs-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
