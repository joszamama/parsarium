# gnalloy.org/codec-http1 — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20261006130159-161e7f51078b`
- **Upstream:** [source repository](<https://gitsbyte.com/gnalloy/codec-http1>) · [pkg.go.dev](<https://pkg.go.dev/gnalloy.org/codec-http1>)
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** gnalloy codec-http1 parser
- **Local input API:** `NewRequestDecoder(int, int).Decode(nil, *buffer.CompositeByteBuf)`
- **Documentation:** [API reference](<https://pkg.go.dev/gnalloy.org/codec-http1@v0.0.0-20261006130159-161e7f51078b>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test",
  "proto": "HTTP/1.1"
}
```

Own HTTP/1.x header and request-line parser in a Netty-style codec for the gnalloy channel framework (splitRequestLine, parseHeaderFieldsWithFramingInto); not a net/http or fasthttp derivative. The adapter calls the exported RequestDecoder.Decode directly on a local CompositeByteBuf with a nil HandlerContext, as the package tests do; no channel, socket or listener is opened.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/gnalloy_org_codec_http1/README.md)

```sh
python3 parsarium.py build http11 go gnalloy_org_codec_http1
python3 parsarium.py run http11 go gnalloy_org_codec_http1 controls/http11/request.http
```
