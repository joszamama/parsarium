# @visulima/yaml — YAML / JavaScript

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/visulima-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript visulima_yaml
python3 parsarium.py run yaml javascript visulima_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript visulima_yaml CORPUS_DIR runs/yaml-visulima_yaml-replay
python3 parsarium.py afl build yaml javascript visulima_yaml
python3 parsarium.py afl prepare yaml javascript visulima_yaml runs/yaml-visulima_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
