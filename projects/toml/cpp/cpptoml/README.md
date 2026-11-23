# cpptoml — TOML / C++

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/cpp/cpptoml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml cpp cpptoml
python3 parsarium.py run toml cpp cpptoml controls/toml/service-config.toml
python3 parsarium.py replay toml cpp cpptoml CORPUS_DIR runs/toml-cpptoml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml cpp cpptoml
python3 parsarium.py afl prepare toml cpp cpptoml runs/toml-cpptoml-afl --fandango 100
python3 parsarium.py afl run runs/toml-cpptoml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
