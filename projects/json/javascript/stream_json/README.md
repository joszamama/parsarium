# stream-json — JSON / JavaScript

Pinned release: `3.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/stream-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript stream_json
python3 parsarium.py run json javascript stream_json controls/json/nested-object.json
python3 parsarium.py replay json javascript stream_json CORPUS_DIR runs/json-stream_json-replay
python3 parsarium.py afl build json javascript stream_json
python3 parsarium.py afl prepare json javascript stream_json runs/json-stream_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
