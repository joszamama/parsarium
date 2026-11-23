# salsify/json-streaming-parser — JSON / PHP

Pinned release: `v8.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/salsify-json-streaming-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php salsify_json_streaming_parser
python3 parsarium.py run json php salsify_json_streaming_parser controls/json/nested-object.json
python3 parsarium.py replay json php salsify_json_streaming_parser CORPUS_DIR runs/json-salsify_json_streaming_parser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json php salsify_json_streaming_parser
python3 parsarium.py afl prepare json php salsify_json_streaming_parser runs/json-salsify_json_streaming_parser-afl --fandango 100
python3 parsarium.py afl run runs/json-salsify_json_streaming_parser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
