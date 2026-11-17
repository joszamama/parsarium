# yaml — YAML / JavaScript

Pinned release: `2.9.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript yaml
python3 parsarium.py run yaml javascript yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript yaml CORPUS_DIR runs/yaml-yaml-replay
python3 parsarium.py afl build yaml javascript yaml
python3 parsarium.py afl prepare yaml javascript yaml runs/yaml-yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
