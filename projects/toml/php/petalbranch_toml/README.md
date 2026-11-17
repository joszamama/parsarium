# petalbranch/toml — TOML / PHP

Pinned release: `v1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/php/petalbranch-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml php petalbranch_toml
python3 parsarium.py run toml php petalbranch_toml controls/toml/service-config.toml
python3 parsarium.py replay toml php petalbranch_toml CORPUS_DIR runs/toml-petalbranch_toml-replay
python3 parsarium.py afl build toml php petalbranch_toml
python3 parsarium.py afl prepare toml php petalbranch_toml runs/toml-petalbranch_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
