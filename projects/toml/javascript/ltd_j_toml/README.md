# @ltd/j-toml — TOML / JavaScript

Pinned release: `1.38.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/ltd-j-toml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript ltd_j_toml
python3 parsarium.py run toml javascript ltd_j_toml controls/toml/service-config.toml
python3 parsarium.py replay toml javascript ltd_j_toml CORPUS_DIR runs/toml-ltd_j_toml-replay
python3 parsarium.py afl build toml javascript ltd_j_toml
python3 parsarium.py afl prepare toml javascript ltd_j_toml runs/toml-ltd_j_toml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
