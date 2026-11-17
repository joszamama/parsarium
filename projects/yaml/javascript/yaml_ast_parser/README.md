# yaml-ast-parser — YAML / JavaScript

Pinned release: `0.0.43`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml-ast-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml_ast_parser
python3 parsarium.py run yaml javascript yaml_ast_parser controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml_ast_parser CORPUS_DIR runs/yaml-yaml_ast_parser-replay
python3 parsarium.py afl build yaml javascript yaml_ast_parser
python3 parsarium.py afl prepare yaml javascript yaml_ast_parser runs/yaml-yaml_ast_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
