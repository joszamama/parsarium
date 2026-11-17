# @amritk/yaml — YAML / JavaScript

Pinned release: `0.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/amritk-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript amritk_yaml
python3 parsarium.py run yaml javascript amritk_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript amritk_yaml CORPUS_DIR runs/yaml-amritk_yaml-replay
python3 parsarium.py afl build yaml javascript amritk_yaml
python3 parsarium.py afl prepare yaml javascript amritk_yaml runs/yaml-amritk_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
