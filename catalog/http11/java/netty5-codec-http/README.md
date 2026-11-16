# netty5-codec-http — HTTP/1.1 / Java

- **Pinned release:** `5.0.0.Alpha5`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** Netty 5 HTTP request decoder, alpha branch; shares project ancestry with Netty 3 and 4
- **Local input API:** `new EmbeddedChannel(new HttpRequestDecoder()); writeInbound(BufferAllocator.copyOf(localBytes)); readInbound() as HttpRequest`
- **Documentation:** [API reference](<https://github.com/netty/netty/blob/netty-5.0.0.Alpha5/codec-http/src/main/java/io/netty5/handler/codec/http/HttpRequestDecoder.java>)
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

[Docker harness and verification receipt](../../../../projects/http11/java/netty5_codec_http/README.md)

```sh
python3 parsarium.py build http11 java netty5_codec_http
python3 parsarium.py run http11 java netty5_codec_http controls/http11/request.http
```
