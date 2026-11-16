# parse-raw-http — HTTP/1.1 / JavaScript

Pinned release: `0.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/parse-raw-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript parse_raw_http
python3 parsarium.py run http11 javascript parse_raw_http controls/http11/response.http
python3 parsarium.py replay http11 javascript parse_raw_http CORPUS_DIR runs/http11-parse_raw_http-replay
python3 parsarium.py afl build http11 javascript parse_raw_http
python3 parsarium.py afl prepare http11 javascript parse_raw_http runs/http11-parse_raw_http-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
