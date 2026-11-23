# libfyaml — YAML / Python

Pinned release: `1.0.0rc2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/libfyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python libfyaml
python3 parsarium.py run yaml python libfyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python libfyaml CORPUS_DIR runs/yaml-libfyaml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml python libfyaml
python3 parsarium.py afl prepare yaml python libfyaml runs/yaml-libfyaml-afl --fandango 100
python3 parsarium.py afl run runs/yaml-libfyaml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
