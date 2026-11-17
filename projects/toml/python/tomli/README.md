# tomli — TOML / Python

Pinned release: `2.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/tomli/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python tomli
python3 parsarium.py run toml python tomli controls/toml/service-config.toml
python3 parsarium.py replay toml python tomli CORPUS_DIR runs/toml-tomli-replay
python3 parsarium.py afl build toml python tomli
python3 parsarium.py afl prepare toml python tomli runs/toml-tomli-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
