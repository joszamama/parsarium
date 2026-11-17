# snakeyaml-engine — YAML / Java

Pinned release: `3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/snakeyaml-engine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java snakeyaml_engine
python3 parsarium.py run yaml java snakeyaml_engine controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java snakeyaml_engine CORPUS_DIR runs/yaml-snakeyaml_engine-replay
python3 parsarium.py afl build yaml java snakeyaml_engine
python3 parsarium.py afl prepare yaml java snakeyaml_engine runs/yaml-snakeyaml_engine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
