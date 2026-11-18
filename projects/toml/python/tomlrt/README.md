# tomlrt — TOML / Python

Pinned release: `2.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/python/tomlrt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml python tomlrt
python3 parsarium.py run toml python tomlrt controls/toml/service-config.toml
python3 parsarium.py replay toml python tomlrt CORPUS_DIR runs/toml-tomlrt-replay
python3 parsarium.py afl build toml python tomlrt
python3 parsarium.py afl prepare toml python tomlrt runs/toml-tomlrt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
