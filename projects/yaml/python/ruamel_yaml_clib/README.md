# ruamel.yaml.clib — YAML / Python

Pinned release: `0.2.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/ruamel-yaml-clib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python ruamel_yaml_clib
python3 parsarium.py run yaml python ruamel_yaml_clib controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python ruamel_yaml_clib CORPUS_DIR runs/yaml-ruamel_yaml_clib-replay
python3 parsarium.py afl build yaml python ruamel_yaml_clib
python3 parsarium.py afl prepare yaml python ruamel_yaml_clib runs/yaml-ruamel_yaml_clib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
