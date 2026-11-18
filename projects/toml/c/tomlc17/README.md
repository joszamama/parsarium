# tomlc17 — TOML / C

Pinned release: `R261116`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/c/tomlc17/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml c tomlc17
python3 parsarium.py run toml c tomlc17 controls/toml/service-config.toml
python3 parsarium.py replay toml c tomlc17 CORPUS_DIR runs/toml-tomlc17-replay
python3 parsarium.py afl build toml c tomlc17
python3 parsarium.py afl prepare toml c tomlc17 runs/toml-tomlc17-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
