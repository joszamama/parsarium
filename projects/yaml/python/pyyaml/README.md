# PyYAML — YAML / Python

Pinned release: `6.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/pyyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python pyyaml
python3 parsarium.py run yaml python pyyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python pyyaml CORPUS_DIR runs/yaml-pyyaml-replay
python3 parsarium.py afl build yaml python pyyaml
python3 parsarium.py afl prepare yaml python pyyaml runs/yaml-pyyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
