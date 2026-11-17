# srsly — YAML / Python

Pinned release: `3.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/srsly/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python srsly
python3 parsarium.py run yaml python srsly controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python srsly CORPUS_DIR runs/yaml-srsly-replay
python3 parsarium.py afl build yaml python srsly
python3 parsarium.py afl prepare yaml python srsly runs/yaml-srsly-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
