# http-pyparser — HTTP/1.1 / Python

- **Pinned release:** `0.5.1`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request method, target and Host
- **Underlying family:** http-pyparser Python parser
- **Local input API:** `http_pyparser.HTTPParser().parser(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/http-pyparser/0.5.1/>)
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

[Docker harness and verification receipt](../../../../projects/http11/python/http_pyparser/README.md)

```sh
python3 parsarium.py build http11 python http_pyparser
python3 parsarium.py run http11 python http_pyparser controls/http11/request.http
```
