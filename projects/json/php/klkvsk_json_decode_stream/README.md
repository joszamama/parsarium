# klkvsk/json-decode-stream — JSON / PHP

Pinned release: `v1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/klkvsk-json-decode-stream/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php klkvsk_json_decode_stream
python3 parsarium.py run json php klkvsk_json_decode_stream controls/json/nested-object.json
python3 parsarium.py replay json php klkvsk_json_decode_stream CORPUS_DIR runs/json-klkvsk_json_decode_stream-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json php klkvsk_json_decode_stream
python3 parsarium.py afl prepare json php klkvsk_json_decode_stream runs/json-klkvsk_json_decode_stream-afl --fandango 100
python3 parsarium.py afl run runs/json-klkvsk_json_decode_stream-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
