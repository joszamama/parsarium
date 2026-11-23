# parse-raw-http — HTTP/1.1 / JavaScript

Pinned release: `0.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/parse-raw-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript parse_raw_http
python3 parsarium.py run http11 javascript parse_raw_http controls/http11/response.http
python3 parsarium.py replay http11 javascript parse_raw_http CORPUS_DIR runs/http11-parse_raw_http-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build http11 javascript parse_raw_http
python3 parsarium.py afl prepare http11 javascript parse_raw_http runs/http11-parse_raw_http-afl --fandango 100
python3 parsarium.py afl run runs/http11-parse_raw_http-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
