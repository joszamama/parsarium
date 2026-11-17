# seld/jsonlint — JSON / PHP

Pinned release: `1.12.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/seld-jsonlint/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php seld_jsonlint
python3 parsarium.py run json php seld_jsonlint controls/json/nested-object.json
python3 parsarium.py replay json php seld_jsonlint CORPUS_DIR runs/json-seld_jsonlint-replay
python3 parsarium.py afl build json php seld_jsonlint
python3 parsarium.py afl prepare json php seld_jsonlint runs/json-seld_jsonlint-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
