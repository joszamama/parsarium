# parserheader — HTTP/1.1 / Python

- **Pinned release:** `0.38.3`
- **License:** BSD
- **Parsed scope:** HTTP header fields only
- **Underlying family:** parserheader Python parser
- **Local input API:** `parserheader.parserheader(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/parserheader/0.38.3/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "host": "example.test",
  "x_parsarium": "yes"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/python/parserheader/README.md)

```sh
python3 parsarium.py build http11 python parserheader
python3 parsarium.py run http11 python parserheader controls/http11/request.http
```
