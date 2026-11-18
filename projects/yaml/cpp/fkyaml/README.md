# fkyaml — YAML / C++

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/cpp/fkyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml cpp fkyaml
python3 parsarium.py run yaml cpp fkyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml cpp fkyaml CORPUS_DIR runs/yaml-fkyaml-replay
python3 parsarium.py afl build yaml cpp fkyaml
python3 parsarium.py afl prepare yaml cpp fkyaml runs/yaml-fkyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
