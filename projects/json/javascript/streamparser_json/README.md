# @streamparser/json — JSON / JavaScript

Pinned release: `0.0.26`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/streamparser-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript streamparser_json
python3 parsarium.py run json javascript streamparser_json controls/json/nested-object.json
python3 parsarium.py replay json javascript streamparser_json CORPUS_DIR runs/json-streamparser_json-replay
python3 parsarium.py afl build json javascript streamparser_json
python3 parsarium.py afl prepare json javascript streamparser_json runs/json-streamparser_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
