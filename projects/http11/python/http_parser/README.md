# http-parser — HTTP/1.1 / Python

Pinned release: `0.9.0`, running on CPython 3.10.16. This release's native extension bundles the Node http-parser C implementation, so the harness instruments both the Python binding and `http_parser.c` while `HttpParser.execute` parses local request bytes.

[Manifest](manifest.json) · [verification receipt](verification.json) · [API and parser family](../../../../catalog/http11/python/http-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python http_parser
python3 parsarium.py run http11 python http_parser controls/http11/request.http
python3 parsarium.py replay http11 python http_parser CORPUS_DIR runs/http11-http-parser-replay
python3 parsarium.py afl build http11 python http_parser
python3 parsarium.py afl prepare http11 python http_parser runs/http11-http-parser-afl
```

Replace `CORPUS_DIR` with a directory of HTTP/1.1 request files. The AFL++ command prepares a seeded run; it does not start a campaign.
