# tomlkit — TOML / Python

Pinned release: `0.15.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/tomlkit/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python tomlkit
python3 parsarium.py run toml python tomlkit controls/toml/service-config.toml
python3 parsarium.py replay toml python tomlkit CORPUS_DIR runs/toml-tomlkit-replay
python3 parsarium.py afl build toml python tomlkit
python3 parsarium.py afl prepare toml python tomlkit runs/toml-tomlkit-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
