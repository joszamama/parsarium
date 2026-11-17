# js-yaml — YAML / JavaScript

Pinned release: `5.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/javascript/js-yaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml javascript js_yaml
python3 parsarium.py run yaml javascript js_yaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml javascript js_yaml CORPUS_DIR runs/yaml-js_yaml-replay
python3 parsarium.py afl build yaml javascript js_yaml
python3 parsarium.py afl prepare yaml javascript js_yaml runs/yaml-js_yaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
