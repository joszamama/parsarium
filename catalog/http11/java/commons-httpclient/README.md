# commons-httpclient — HTTP/1.1 / Java

- **Pinned release:** `3.1`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/commons-httpclient/commons-httpclient>)
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status line and headers from local stream
- **Underlying family:** Apache Commons HttpClient 3.x native HTTP response-head parser
- **Local input API:** `HttpParser.readLine(local InputStream, US-ASCII) + new StatusLine(line) + HttpParser.parseHeaders(same local InputStream, US-ASCII); getHttpVersion(), getStatusCode(), getReasonPhrase(), Header.getValue()`
- **Documentation:** [API reference](<https://hc.apache.org/httpclient-legacy/apidocs/org/apache/commons/httpclient/HttpParser.html>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "version": "HTTP/1.1",
  "status": 200,
  "reason": "OK",
  "content_type": "text/plain",
  "content_length": 9
}
```

The legacy Apache Commons HttpClient 3.1 package provides its own public status-line and header parser APIs; the adapter uses both on one local InputStream. It is the predecessor project of HttpComponents but a distinct package and parser implementation line. Only the response head is tested.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/commons_httpclient/README.md)

```sh
python3 parsarium.py build http11 java commons_httpclient
python3 parsarium.py run http11 java commons_httpclient controls/http11/response.http
```
