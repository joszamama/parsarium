# jtoml — TOML / Java

Pinned release: `1.8.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/java/jtoml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml java jtoml
python3 parsarium.py run toml java jtoml controls/toml/service-config.toml
python3 parsarium.py replay toml java jtoml CORPUS_DIR runs/toml-jtoml-replay
python3 parsarium.py afl build toml java jtoml
python3 parsarium.py afl prepare toml java jtoml runs/toml-jtoml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
