# toml11 — TOML / C++

Pinned release: `4.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/cpp/toml11/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml cpp toml11
python3 parsarium.py run toml cpp toml11 controls/toml/service-config.toml
python3 parsarium.py replay toml cpp toml11 CORPUS_DIR runs/toml-toml11-replay
python3 parsarium.py afl build toml cpp toml11
python3 parsarium.py afl prepare toml cpp toml11 runs/toml-toml11-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
