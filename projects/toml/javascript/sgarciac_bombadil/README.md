# @sgarciac/bombadil — TOML / JavaScript

Pinned release: `2.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/toml/javascript/sgarciac-bombadil/README.md)

## Run from the repository root

```sh
python3 parsarium.py build toml javascript sgarciac_bombadil
python3 parsarium.py run toml javascript sgarciac_bombadil controls/toml/service-config.toml
python3 parsarium.py replay toml javascript sgarciac_bombadil CORPUS_DIR runs/toml-sgarciac_bombadil-replay
python3 parsarium.py afl build toml javascript sgarciac_bombadil
python3 parsarium.py afl prepare toml javascript sgarciac_bombadil runs/toml-sgarciac_bombadil-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
