# java-warc — HTTP/1.1 / Java

- **Pinned release:** `1.2.1`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status, Content-Type and body from local stream
- **Underlying family:** java-warc response wrapper over Apache HttpComponents Core 4.x parser
- **Local input API:** `new ResponseContentBlockFactory(new HeaderParser()).newResponseContentBlock(local InputStream); getStatusCode(), getMimeType(), getPayloadAsString()`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/github/bottomless-archive-project/java-warc/1.2.1/java-warc-1.2.1-sources.jar>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "status": 200,
  "content_type": "text/plain",
  "body": "parsarium"
}
```

Public ResponseContentBlockFactory accepts a raw local HTTP response InputStream without a WARC container and returns a structured response block. Its POM depends on httpcore 4.4.14; the combined adapter classpath resolves httpcore 4.4.16. Counted as a separate Maven package path, not an independent parser engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/java_warc/README.md)

```sh
python3 parsarium.py build http11 java java_warc
python3 parsarium.py run http11 java java_warc controls/http11/response.http
```
