# purrphp/yaml — YAML / PHP

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/php/purrphp-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml php purrphp_yaml
python3 parsarium.py run yaml php purrphp_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml php purrphp_yaml CORPUS_DIR runs/yaml-purrphp_yaml-replay
python3 parsarium.py afl build yaml php purrphp_yaml
python3 parsarium.py afl prepare yaml php purrphp_yaml runs/yaml-purrphp_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
