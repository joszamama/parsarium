# jsonparse — JSON / JavaScript

Pinned release: `1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/jsonparse/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript jsonparse
python3 parsarium.py run json javascript jsonparse controls/json/nested-object.json
python3 parsarium.py replay json javascript jsonparse CORPUS_DIR runs/json-jsonparse-replay
python3 parsarium.py afl build json javascript jsonparse
python3 parsarium.py afl prepare json javascript jsonparse runs/json-jsonparse-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
