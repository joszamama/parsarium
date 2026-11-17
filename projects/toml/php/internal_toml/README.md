# internal/toml — TOML / PHP

Pinned release: `1.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/php/internal-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml php internal_toml
python3 parsarium.py run toml php internal_toml controls/toml/service-config.toml
python3 parsarium.py replay toml php internal_toml CORPUS_DIR runs/toml-internal_toml-replay
python3 parsarium.py afl build toml php internal_toml
python3 parsarium.py afl prepare toml php internal_toml runs/toml-internal_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
