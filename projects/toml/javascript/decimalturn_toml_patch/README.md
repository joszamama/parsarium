# @decimalturn/toml-patch — TOML / JavaScript

Pinned release: `3.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/decimalturn-toml-patch/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript decimalturn_toml_patch
python3 parsarium.py run toml javascript decimalturn_toml_patch controls/toml/service-config.toml
python3 parsarium.py replay toml javascript decimalturn_toml_patch CORPUS_DIR runs/toml-decimalturn_toml_patch-replay
python3 parsarium.py afl build toml javascript decimalturn_toml_patch
python3 parsarium.py afl prepare toml javascript decimalturn_toml_patch runs/toml-decimalturn_toml_patch-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
