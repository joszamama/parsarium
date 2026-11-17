# laminas/laminas-json — JSON / PHP

Pinned release: `3.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/laminas-laminas-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php laminas_json
python3 parsarium.py run json php laminas_json controls/json/nested-object.json
python3 parsarium.py replay json php laminas_json CORPUS_DIR runs/json-laminas_json-replay
python3 parsarium.py afl build json php laminas_json
python3 parsarium.py afl prepare json php laminas_json runs/json-laminas_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
