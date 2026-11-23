# jackson-dataformat-toml — TOML / Java

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/java/jackson-dataformat-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml java jackson_dataformat_toml
python3 parsarium.py run toml java jackson_dataformat_toml controls/toml/service-config.toml
python3 parsarium.py replay toml java jackson_dataformat_toml CORPUS_DIR runs/toml-jackson_dataformat_toml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml java jackson_dataformat_toml
python3 parsarium.py afl prepare toml java jackson_dataformat_toml runs/toml-jackson_dataformat_toml-afl --fandango 100
python3 parsarium.py afl run runs/toml-jackson_dataformat_toml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
