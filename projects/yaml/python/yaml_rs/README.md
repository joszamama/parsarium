# yaml-rs — YAML / Python

Pinned release: `0.1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/yaml-rs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python yaml_rs
python3 parsarium.py run yaml python yaml_rs controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python yaml_rs CORPUS_DIR runs/yaml-yaml_rs-replay
python3 parsarium.py afl build yaml python yaml_rs
python3 parsarium.py afl prepare yaml python yaml_rs runs/yaml-yaml_rs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
