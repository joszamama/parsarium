# libfyaml — YAML / Python

Pinned release: `1.0.0rc2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/libfyaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python libfyaml
python3 parsarium.py run yaml python libfyaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python libfyaml CORPUS_DIR runs/yaml-libfyaml-replay
python3 parsarium.py afl build yaml python libfyaml
python3 parsarium.py afl prepare yaml python libfyaml runs/yaml-libfyaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
