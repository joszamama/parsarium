# symfony/yaml — YAML / PHP

Pinned release: `v8.1.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/php/symfony-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml php symfony_yaml
python3 parsarium.py run yaml php symfony_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml php symfony_yaml CORPUS_DIR runs/yaml-symfony_yaml-replay
python3 parsarium.py afl build yaml php symfony_yaml
python3 parsarium.py afl prepare yaml php symfony_yaml runs/yaml-symfony_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
