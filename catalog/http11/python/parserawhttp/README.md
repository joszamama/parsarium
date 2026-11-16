# ParseRawHTTP — HTTP/1.1 / Python

- **Pinned release:** `1.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request method, target and Host
- **Underlying family:** ParseRawHTTP Python parser with CPython http.server
- **Local input API:** `ParseRawHTTP.ParseRawHTTP(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/ParseRawHTTP/1.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/python/parserawhttp/README.md)

```sh
python3 parsarium.py build http11 python parserawhttp
python3 parsarium.py run http11 python parserawhttp controls/http11/request.http
```
