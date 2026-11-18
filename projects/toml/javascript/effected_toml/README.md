# @effected/toml — TOML / JavaScript

Pinned release: `0.20.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/effected-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript effected_toml
python3 parsarium.py run toml javascript effected_toml controls/toml/service-config.toml
python3 parsarium.py replay toml javascript effected_toml CORPUS_DIR runs/toml-effected_toml-replay
python3 parsarium.py afl build toml javascript effected_toml
python3 parsarium.py afl prepare toml javascript effected_toml runs/toml-effected_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
