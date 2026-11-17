# zio-json-yaml — YAML / Java

Pinned release: `1.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/zio-json-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java zio_json_yaml
python3 parsarium.py run yaml java zio_json_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java zio_json_yaml CORPUS_DIR runs/yaml-zio_json_yaml-replay
python3 parsarium.py afl build yaml java zio_json_yaml
python3 parsarium.py afl prepare yaml java zio_json_yaml runs/yaml-zio_json_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
