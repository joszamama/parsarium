# pcrov/jsonreader — JSON / PHP

Pinned release: `1.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/pcrov-jsonreader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php pcrov_jsonreader
python3 parsarium.py run json php pcrov_jsonreader controls/json/nested-object.json
python3 parsarium.py replay json php pcrov_jsonreader CORPUS_DIR runs/json-pcrov_jsonreader-replay
python3 parsarium.py afl build json php pcrov_jsonreader
python3 parsarium.py afl prepare json php pcrov_jsonreader runs/json-pcrov_jsonreader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
