# tomlplusplus — TOML / C++

Pinned release: `3.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/cpp/tomlplusplus/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml cpp tomlplusplus
python3 parsarium.py run toml cpp tomlplusplus controls/toml/service-config.toml
python3 parsarium.py replay toml cpp tomlplusplus CORPUS_DIR runs/toml-tomlplusplus-replay
python3 parsarium.py afl build toml cpp tomlplusplus
python3 parsarium.py afl prepare toml cpp tomlplusplus runs/toml-tomlplusplus-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
