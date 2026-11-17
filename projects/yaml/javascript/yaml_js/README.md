# yaml-js — YAML / JavaScript

Pinned release: `0.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml_js
python3 parsarium.py run yaml javascript yaml_js controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml_js CORPUS_DIR runs/yaml-yaml_js-replay
python3 parsarium.py afl build yaml javascript yaml_js
python3 parsarium.py afl prepare yaml javascript yaml_js runs/yaml-yaml_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
