# ssl-proxies — HTTP/1.1 / Java

- **Pinned release:** `2.1.0`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status and headers from local stream
- **Underlying family:** JGlobus native HTTP response parser
- **Local input API:** `new org.globus.util.http.HTTPResponseParser(local InputStream); getStatusCode(), getMessage(), getContentType(), getContentLength()`
- **Documentation:** [API reference](<https://javadoc.io/static/org.jglobus/ssl-proxies/2.1.0/org/globus/util/http/HTTPResponseParser.html>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "status": 200,
  "message": "OK",
  "content_type": "text/plain",
  "content_length": 9
}
```

The ssl-proxies artifact includes its own HTTPParser and HTTPResponseParser classes. The response parser reads the local InputStream directly and reports status, reason and headers; the valid control verifies those fields, not response body handling. Apache-2.0 header is in the pinned source JAR.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/ssl_proxies/README.md)

```sh
python3 parsarium.py build http11 java ssl_proxies
python3 parsarium.py run http11 java ssl_proxies controls/http11/response.http
```
