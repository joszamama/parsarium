# jodd-http — HTTP/1.1 / Java

- **Pinned release:** `6.3.0`
- **Upstream:** [source repository](<https://github.com/oblac/jodd-http>) · [Maven Central](<https://central.sonatype.com/artifact/org.jodd/jodd-http>)
- **License:** BSD-2-Clause
- **Parsed scope:** HTTP/1.1 request line and headers from local stream
- **Underlying family:** Jodd HTTP native request parser
- **Local input API:** `jodd.http.HttpRequest.readFrom(local InputStream); method(), path(), queryString(), httpVersion(), header(name)`
- **Documentation:** [API reference](<https://http.jodd.org/connection>)
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

[Docker harness and verification receipt](../../../../projects/http11/java/jodd_http/README.md)

```sh
python3 parsarium.py build http11 java jodd_http
python3 parsarium.py run http11 java jodd_http controls/http11/request.http
```
