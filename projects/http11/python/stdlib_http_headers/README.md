# http.client.parse_headers — HTTP/1.1 / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/http11/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build http11 python stdlib_http_headers
python3 parsarium.py run http11 python stdlib_http_headers controls/http11/response.http
python3 parsarium.py replay http11 python stdlib_http_headers CORPUS_DIR runs/http11-stdlib_http_headers-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build http11 python stdlib_http_headers
python3 parsarium.py afl prepare http11 python stdlib_http_headers runs/http11-stdlib_http_headers-afl --fandango 100
python3 parsarium.py afl run runs/http11-stdlib_http_headers-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
