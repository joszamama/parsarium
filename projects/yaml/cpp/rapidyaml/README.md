# rapidyaml — YAML / C++

Pinned release: `0.16.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/cpp/rapidyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml cpp rapidyaml
python3 parsarium.py run yaml cpp rapidyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml cpp rapidyaml CORPUS_DIR runs/yaml-rapidyaml-replay
python3 parsarium.py afl build yaml cpp rapidyaml
python3 parsarium.py afl prepare yaml cpp rapidyaml runs/yaml-rapidyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
