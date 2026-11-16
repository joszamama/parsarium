# rawhttp-core — HTTP/1.1 / Java

- **Pinned release:** `2.6.0`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local stream
- **Underlying family:** RawHTTP native HTTP/1.1 parser
- **Local input API:** `new rawhttp.core.RawHttp().parseRequest(local InputStream); getMethod(), getUri(), getStartLine().getHttpVersion(), getHeaders()`
- **Documentation:** [API reference](<https://github.com/renatoathaydes/rawhttp>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "HTTP/1.1",
  "host": "example.test",
  "x_parsarium": "yes"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/rawhttp_core/README.md)

```sh
python3 parsarium.py build http11 java rawhttp_core
python3 parsarium.py run http11 java rawhttp_core controls/http11/request.http
```
