# h11r — HTTP/1.1 / Python

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** h11r Rust/httparse core
- **Local input API:** `h11r.Connection(Role.SERVER).receive_data(bytes); next_event()`
- **Documentation:** [API reference](<https://pypi.org/project/h11r/0.2.0/>)
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

[Docker harness and verification receipt](../../../../projects/http11/python/h11r/README.md)

```sh
python3 parsarium.py build http11 python h11r
python3 parsarium.py run http11 python h11r controls/http11/request.http
```
