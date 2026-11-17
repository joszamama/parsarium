# yamlcore — YAML / Python

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/yamlcore/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python yamlcore
python3 parsarium.py run yaml python yamlcore controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python yamlcore CORPUS_DIR runs/yaml-yamlcore-replay
python3 parsarium.py afl build yaml python yamlcore
python3 parsarium.py afl prepare yaml python yamlcore runs/yaml-yamlcore-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
