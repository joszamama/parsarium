# tornado — HTTP/1.1 / Python

- **Pinned release:** `6.6.1`
- **Upstream:** [source repository](<https://github.com/tornadoweb/tornado>) · [PyPI](<https://pypi.org/project/tornado/>)
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status, headers and body
- **Underlying family:** Tornado Python HTTP/1 parser
- **Local input API:** `tornado.http1connection.HTTP1Connection(local IOStream, is_client=True).read_response(delegate)`
- **Documentation:** [API reference](<https://www.tornadoweb.org/en/stable/http1connection.html>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "status": 200,
  "content_type": "text/plain",
  "body": "parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/python/tornado/README.md)

```sh
python3 parsarium.py build http11 python tornado
python3 parsarium.py run http11 python tornado controls/http11/response.http
```
