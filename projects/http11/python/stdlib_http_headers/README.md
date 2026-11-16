# http.client.parse_headers — HTTP/1.1 / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/http11/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build http11 python stdlib_http_headers
python3 parsarium.py run http11 python stdlib_http_headers controls/http11/response.http
python3 parsarium.py replay http11 python stdlib_http_headers CORPUS_DIR runs/http11-stdlib_http_headers-replay
python3 parsarium.py afl build http11 python stdlib_http_headers
python3 parsarium.py afl prepare http11 python stdlib_http_headers runs/http11-stdlib_http_headers-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
