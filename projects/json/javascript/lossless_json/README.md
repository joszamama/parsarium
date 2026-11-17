# lossless-json — JSON / JavaScript

Pinned release: `4.3.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/lossless-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript lossless_json
python3 parsarium.py run json javascript lossless_json controls/json/nested-object.json
python3 parsarium.py replay json javascript lossless_json CORPUS_DIR runs/json-lossless_json-replay
python3 parsarium.py afl build json javascript lossless_json
python3 parsarium.py afl prepare json javascript lossless_json runs/json-lossless_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
