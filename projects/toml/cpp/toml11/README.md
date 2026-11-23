# toml11 — TOML / C++

Pinned release: `4.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/cpp/toml11/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml cpp toml11
python3 parsarium.py run toml cpp toml11 controls/toml/service-config.toml
python3 parsarium.py replay toml cpp toml11 CORPUS_DIR runs/toml-toml11-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml cpp toml11
python3 parsarium.py afl prepare toml cpp toml11 runs/toml-toml11-afl --fandango 100
python3 parsarium.py afl run runs/toml-toml11-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
