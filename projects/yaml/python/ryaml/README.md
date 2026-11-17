# ryaml — YAML / Python

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/yaml/python/ryaml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build yaml python ryaml
python3 parsarium.py run yaml python ryaml controls/yaml/catalog.yaml
python3 parsarium.py replay yaml python ryaml CORPUS_DIR runs/yaml-ryaml-replay
python3 parsarium.py afl build yaml python ryaml
python3 parsarium.py afl prepare yaml python ryaml runs/yaml-ryaml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
