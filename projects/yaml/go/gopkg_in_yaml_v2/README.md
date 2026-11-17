# gopkg.in/yaml.v2 — YAML / Go

Pinned release: `v2.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/go/gopkg-in-yaml-v2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml go gopkg_in_yaml_v2
python3 parsarium.py run yaml go gopkg_in_yaml_v2 controls/yaml/catalog.yaml
python3 parsarium.py replay yaml go gopkg_in_yaml_v2 CORPUS_DIR runs/yaml-gopkg_in_yaml_v2-replay
python3 parsarium.py afl build yaml go gopkg_in_yaml_v2
python3 parsarium.py afl prepare yaml go gopkg_in_yaml_v2 runs/yaml-gopkg_in_yaml_v2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
