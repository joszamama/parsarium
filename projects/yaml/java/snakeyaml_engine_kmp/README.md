# snakeyaml-engine-kmp — YAML / Java

Pinned release: `5.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/java/snakeyaml-engine-kmp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml java snakeyaml_engine_kmp
python3 parsarium.py run yaml java snakeyaml_engine_kmp controls/yaml/catalog.yaml
python3 parsarium.py replay yaml java snakeyaml_engine_kmp CORPUS_DIR runs/yaml-snakeyaml_engine_kmp-replay
python3 parsarium.py afl build yaml java snakeyaml_engine_kmp
python3 parsarium.py afl prepare yaml java snakeyaml_engine_kmp runs/yaml-snakeyaml_engine_kmp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
