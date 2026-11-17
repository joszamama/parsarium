# PyYAML CSafeLoader (libyaml) — YAML / Python

Pinned release: `6.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/pyyaml-csafeloader-libyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python pyyaml_csafeloader
python3 parsarium.py run yaml python pyyaml_csafeloader controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python pyyaml_csafeloader CORPUS_DIR runs/yaml-pyyaml_csafeloader-replay
python3 parsarium.py afl build yaml python pyyaml_csafeloader
python3 parsarium.py afl prepare yaml python pyyaml_csafeloader runs/yaml-pyyaml_csafeloader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
