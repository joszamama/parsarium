# http1_1-parser — HTTP/1.1 / Java

- **Pinned release:** `2.1.109`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** WebPieces HTTP/1.1 parser
- **Local input API:** `HttpParserFactory.createParser(...); parser.parse(parser.prepareToParse(), DataWrapper wrapping local bytes); Memento.getParsedMessages()`
- **Documentation:** [API reference](<https://github.com/deanhiller/webpieces/blob/master/http/http1_1-parser/src/main/java/org/webpieces/httpparser/api/HttpParser.java>)
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

[Docker harness and verification receipt](../../../../projects/http11/java/http1_1_parser/README.md)

```sh
python3 parsarium.py build http11 java http1_1_parser
python3 parsarium.py run http11 java http1_1_parser controls/http11/request.http
```
