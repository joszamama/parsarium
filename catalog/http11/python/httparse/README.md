# httparse — HTTP/1.1 / Python

- **Pinned release:** `0.2.1`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** Rust httparse binding
- **Local input API:** `httparse.RequestParser().parse(bytes)`
- **Documentation:** [API reference](<https://pypi.org/project/httparse/0.2.1/>)
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

[Docker harness and verification receipt](../../../../projects/http11/python/httparse/README.md)

```sh
python3 parsarium.py build http11 python httparse
python3 parsarium.py run http11 python httparse controls/http11/request.http
```
