# yaml.min — YAML / JavaScript

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml-min/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml_min
python3 parsarium.py run yaml javascript yaml_min controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml_min CORPUS_DIR runs/yaml-yaml_min-replay
python3 parsarium.py afl build yaml javascript yaml_min
python3 parsarium.py afl prepare yaml javascript yaml_min runs/yaml-yaml_min-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
