# @stoplight/yaml — YAML / JavaScript

Pinned release: `4.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/stoplight-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript stoplight_yaml
python3 parsarium.py run yaml javascript stoplight_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript stoplight_yaml CORPUS_DIR runs/yaml-stoplight_yaml-replay
python3 parsarium.py afl build yaml javascript stoplight_yaml
python3 parsarium.py afl prepare yaml javascript stoplight_yaml runs/yaml-stoplight_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
