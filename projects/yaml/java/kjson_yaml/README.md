# kjson-yaml — YAML / Java

Pinned release: `3.15`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/kjson-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java kjson_yaml
python3 parsarium.py run yaml java kjson_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java kjson_yaml CORPUS_DIR runs/yaml-kjson_yaml-replay
python3 parsarium.py afl build yaml java kjson_yaml
python3 parsarium.py afl prepare yaml java kjson_yaml runs/yaml-kjson_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
