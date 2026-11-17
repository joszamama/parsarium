# night-config-toml — TOML / Java

Pinned release: `3.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/java/night-config-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml java night_config_toml
python3 parsarium.py run toml java night_config_toml controls/toml/service-config.toml
python3 parsarium.py replay toml java night_config_toml CORPUS_DIR runs/toml-night_config_toml-replay
python3 parsarium.py afl build toml java night_config_toml
python3 parsarium.py afl prepare toml java night_config_toml runs/toml-night_config_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
