# joelwurtz/json-stream-polyfill — JSON / PHP

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/php/joelwurtz-json-stream-polyfill/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json php joelwurtz_json_stream_polyfill
python3 parsarium.py run json php joelwurtz_json_stream_polyfill controls/json/nested-object.json
python3 parsarium.py replay json php joelwurtz_json_stream_polyfill CORPUS_DIR runs/json-joelwurtz_json_stream_polyfill-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build json php joelwurtz_json_stream_polyfill
python3 parsarium.py afl prepare json php joelwurtz_json_stream_polyfill runs/json-joelwurtz_json_stream_polyfill-afl --fandango 100
python3 parsarium.py afl run runs/json-joelwurtz_json_stream_polyfill-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
