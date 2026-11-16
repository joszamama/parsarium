# http.server.BaseHTTPRequestHandler — HTTP/1.1 / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/http11/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build http11 python stdlib_http_server
python3 parsarium.py run http11 python stdlib_http_server controls/http11/request.http
python3 parsarium.py replay http11 python stdlib_http_server CORPUS_DIR runs/http11-stdlib_http_server-replay
python3 parsarium.py afl build http11 python stdlib_http_server
python3 parsarium.py afl prepare http11 python stdlib_http_server runs/http11-stdlib_http_server-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
