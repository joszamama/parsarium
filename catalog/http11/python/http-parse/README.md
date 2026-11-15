# http-parse — HTTP/1.1 / Python

- **Pinned release:** `0.1.5`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request method, target and Host
- **Underlying family:** http-parse Python parser
- **Local input API:** `http_parse.parse(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/http-parse/0.1.5/>)
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

[Docker harness and verification receipt](../../../../projects/http11/python/http_parse/README.md)

```sh
python3 parsarium.py build http11 python http_parse
python3 parsarium.py run http11 python http_parse controls/http11/request.http
```
