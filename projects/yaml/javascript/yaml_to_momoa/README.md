# yaml-to-momoa — YAML / JavaScript

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml-to-momoa/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml_to_momoa
python3 parsarium.py run yaml javascript yaml_to_momoa controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml_to_momoa CORPUS_DIR runs/yaml-yaml_to_momoa-replay
python3 parsarium.py afl build yaml javascript yaml_to_momoa
python3 parsarium.py afl prepare yaml javascript yaml_to_momoa runs/yaml-yaml_to_momoa-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
