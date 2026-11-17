# libfyaml — YAML / C

Pinned release: `0.9.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/c/libfyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml c libfyaml
python3 parsarium.py run yaml c libfyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml c libfyaml CORPUS_DIR runs/yaml-libfyaml-replay
python3 parsarium.py afl build yaml c libfyaml
python3 parsarium.py afl prepare yaml c libfyaml runs/yaml-libfyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
