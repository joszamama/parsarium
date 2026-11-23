# http_parser — HTTP/1.1 / Rust

Pinned release: `0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/rust/http-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 rust http_parser
python3 parsarium.py run http11 rust http_parser controls/http11/request.http
python3 parsarium.py replay http11 rust http_parser CORPUS_DIR runs/http11-http_parser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build http11 rust http_parser
python3 parsarium.py afl prepare http11 rust http_parser runs/http11-http_parser-afl --fandango 100
python3 parsarium.py afl run runs/http11-http_parser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
