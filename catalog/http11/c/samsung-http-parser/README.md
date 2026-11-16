# samsung-http-parser — HTTP/1.1 / C

- **Pinned release:** `2.5.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse from local bytes
- **Underlying family:** Samsung tagged fork of the Node/Joyent http-parser C engine; separate 2.5.0 source distribution, shared parser family with nodejs/http-parser 2.9.4 and libhv-bundled 2.9.1, not an independent decoder
- **Local input API:** `http_parser_init(HTTP_REQUEST); http_parser_execute(parser, callbacks, local request bytes, length); on_url and on_headers_complete callbacks`
- **Documentation:** [API reference](<https://github.com/Samsung/http-parser/blob/v2.5.0/README.md>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/c/samsung-http-parser/README.md)

```sh
python3 parsarium.py build http11 c samsung-http-parser
python3 parsarium.py run http11 c samsung-http-parser controls/http11/request.http
```
