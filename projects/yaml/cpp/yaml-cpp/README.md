# yaml-cpp — YAML / C++

Pinned release: `0.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/cpp/yaml-cpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml cpp yaml-cpp
python3 parsarium.py run yaml cpp yaml-cpp controls/yaml/catalog.yaml
python3 parsarium.py replay yaml cpp yaml-cpp CORPUS_DIR runs/yaml-yaml-cpp-replay
python3 parsarium.py afl build yaml cpp yaml-cpp
python3 parsarium.py afl prepare yaml cpp yaml-cpp runs/yaml-yaml-cpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
