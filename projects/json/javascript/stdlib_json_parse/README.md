# JSON.parse — JSON / JavaScript

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/javascript/json/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build json javascript stdlib_json_parse
python3 parsarium.py run json javascript stdlib_json_parse controls/json/nested-object.json
python3 parsarium.py replay json javascript stdlib_json_parse CORPUS_DIR runs/json-stdlib_json_parse-replay
python3 parsarium.py afl build json javascript stdlib_json_parse
python3 parsarium.py afl prepare json javascript stdlib_json_parse runs/json-stdlib_json_parse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
