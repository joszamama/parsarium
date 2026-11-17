# json-bigint — JSON / JavaScript

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, parser family, and limits](../../../../catalog/json/javascript/json-bigint/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript json_bigint
python3 parsarium.py run json javascript json_bigint controls/json/nested-object.json
python3 parsarium.py replay json javascript json_bigint CORPUS_DIR runs/json-json_bigint-replay
python3 parsarium.py afl build json javascript json_bigint
python3 parsarium.py afl prepare json javascript json_bigint runs/json-json_bigint-afl
```

Replace `CORPUS_DIR` with a directory of JSON files. The AFL++ command prepares a seeded run; it does not start a campaign. The bridge maps only `json-bigint/lib/parse.js` source ranges to feedback.
