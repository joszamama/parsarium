# go.yaml.in/yaml/v4 — YAML / Go

Pinned release: `v4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/go-yaml-in-yaml-v4/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go go_yaml_in_yaml_v4
python3 parsarium.py run yaml go go_yaml_in_yaml_v4 controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go go_yaml_in_yaml_v4 CORPUS_DIR runs/yaml-go_yaml_in_yaml_v4-replay
python3 parsarium.py afl build yaml go go_yaml_in_yaml_v4
python3 parsarium.py afl prepare yaml go go_yaml_in_yaml_v4 runs/yaml-go_yaml_in_yaml_v4-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
