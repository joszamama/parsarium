# yaml-eslint-parser — YAML / JavaScript

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml-eslint-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml_eslint_parser
python3 parsarium.py run yaml javascript yaml_eslint_parser controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml_eslint_parser CORPUS_DIR runs/yaml-yaml_eslint_parser-replay
python3 parsarium.py afl build yaml javascript yaml_eslint_parser
python3 parsarium.py afl prepare yaml javascript yaml_eslint_parser runs/yaml-yaml_eslint_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
