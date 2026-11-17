# libyaml — YAML / C

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/c/libyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml c libyaml
python3 parsarium.py run yaml c libyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml c libyaml CORPUS_DIR runs/yaml-libyaml-replay
python3 parsarium.py afl build yaml c libyaml
python3 parsarium.py afl prepare yaml c libyaml runs/yaml-libyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
