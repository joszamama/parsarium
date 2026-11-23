# snakeyaml-engine-kmp — YAML / Java

Pinned release: `5.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/snakeyaml-engine-kmp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java snakeyaml_engine_kmp
python3 parsarium.py run yaml java snakeyaml_engine_kmp controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java snakeyaml_engine_kmp CORPUS_DIR runs/yaml-snakeyaml_engine_kmp-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build yaml java snakeyaml_engine_kmp
python3 parsarium.py afl prepare yaml java snakeyaml_engine_kmp runs/yaml-snakeyaml_engine_kmp-afl --fandango 100
python3 parsarium.py afl run runs/yaml-snakeyaml_engine_kmp-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
