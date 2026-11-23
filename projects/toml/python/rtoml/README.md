# rtoml — TOML / Python

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/rtoml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python rtoml
python3 parsarium.py run toml python rtoml controls/toml/service-config.toml
python3 parsarium.py replay toml python rtoml CORPUS_DIR runs/toml-rtoml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build toml python rtoml
python3 parsarium.py afl prepare toml python rtoml runs/toml-rtoml-afl --fandango 100
python3 parsarium.py afl run runs/toml-rtoml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
