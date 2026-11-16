# http-parser — HTTP/1.1 / C

- **Pinned release:** `2.9.4`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse
- **Underlying family:** Node http-parser C state machine, predecessor design to llhttp
- **Local input API:** `http_parser_init(..., HTTP_REQUEST); http_parser_execute(..., local request bytes, length); on_url and on_headers_complete callbacks`
- **Documentation:** [API reference](<https://github.com/nodejs/http-parser#usage>)
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

[Docker harness and verification receipt](../../../../projects/http11/c/http-parser/README.md)

```sh
python3 parsarium.py build http11 c http-parser
python3 parsarium.py run http11 c http-parser controls/http11/request.http
```
