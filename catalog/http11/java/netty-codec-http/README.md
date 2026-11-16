# netty-codec-http — HTTP/1.1 / Java

- **Pinned release:** `4.2.20.Final`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** Netty 4 HTTP request decoder
- **Local input API:** `new HttpRequestDecoder() in EmbeddedChannel; writeInbound(ByteBuf); readInbound() as HttpRequest`
- **Documentation:** [API reference](<https://netty.io/4.2/api/io/netty/handler/codec/http/HttpRequestDecoder.html>)
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

[Docker harness and verification receipt](../../../../projects/http11/java/netty_codec_http/README.md)

```sh
python3 parsarium.py build http11 java netty_codec_http
python3 parsarium.py run http11 java netty_codec_http controls/http11/request.http
```
