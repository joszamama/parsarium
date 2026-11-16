# tp-http-request-response-parser — HTTP/1.1 / Python

- **Pinned release:** `2026.5.18`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request method and version
- **Underlying family:** TP Python HTTP parser
- **Local input API:** `TP_HTTP_Request_Response_Parser.TP_HTTP_REQUEST_PARSER(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/tp-http-request-response-parser/2026.5.18/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "version": "HTTP/1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/python/tp_http_request_response_parser/README.md)

```sh
python3 parsarium.py build http11 python tp_http_request_response_parser
python3 parsarium.py run http11 python tp_http_request_response_parser controls/http11/request.http
```
