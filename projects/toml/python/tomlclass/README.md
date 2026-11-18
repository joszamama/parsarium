# tomlclass — TOML / Python

Pinned release: `0.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/tomlclass/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python tomlclass
python3 parsarium.py run toml python tomlclass controls/toml/service-config.toml
python3 parsarium.py replay toml python tomlclass CORPUS_DIR runs/toml-tomlclass-replay
python3 parsarium.py afl build toml python tomlclass
python3 parsarium.py afl prepare toml python tomlclass runs/toml-tomlclass-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
