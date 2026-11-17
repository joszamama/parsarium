# smol-toml — TOML / JavaScript

Pinned release: `1.9.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/smol-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript smol_toml
python3 parsarium.py run toml javascript smol_toml controls/toml/service-config.toml
python3 parsarium.py replay toml javascript smol_toml CORPUS_DIR runs/toml-smol_toml-replay
python3 parsarium.py afl build toml javascript smol_toml
python3 parsarium.py afl prepare toml javascript smol_toml runs/toml-smol_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
