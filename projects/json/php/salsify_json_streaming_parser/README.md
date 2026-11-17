# salsify/json-streaming-parser — JSON / PHP

Pinned release: `v8.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/salsify-json-streaming-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php salsify_json_streaming_parser
python3 parsarium.py run json php salsify_json_streaming_parser controls/json/nested-object.json
python3 parsarium.py replay json php salsify_json_streaming_parser CORPUS_DIR runs/json-salsify_json_streaming_parser-replay
python3 parsarium.py afl build json php salsify_json_streaming_parser
python3 parsarium.py afl prepare json php salsify_json_streaming_parser runs/json-salsify_json_streaming_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
