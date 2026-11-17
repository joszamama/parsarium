# JSONStream — JSON / JavaScript

Pinned release: `1.3.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/jsonstream/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript jsonstream
python3 parsarium.py run json javascript jsonstream controls/json/nested-object.json
python3 parsarium.py replay json javascript jsonstream CORPUS_DIR runs/json-jsonstream-replay
python3 parsarium.py afl build json javascript jsonstream
python3 parsarium.py afl prepare json javascript jsonstream runs/json-jsonstream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
