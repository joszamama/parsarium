# toml-eslint-parser — TOML / JavaScript

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/toml-eslint-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript toml_eslint_parser
python3 parsarium.py run toml javascript toml_eslint_parser controls/toml/service-config.toml
python3 parsarium.py replay toml javascript toml_eslint_parser CORPUS_DIR runs/toml-toml_eslint_parser-replay
python3 parsarium.py afl build toml javascript toml_eslint_parser
python3 parsarium.py afl prepare toml javascript toml_eslint_parser runs/toml-toml_eslint_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
