# httpp — HTTP/1.1 / C

- **Pinned release:** `2.0.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version
- **Underlying family:** httpp C single-header request parser
- **Local input API:** `httpp_init_req(...); httpp_parse_request(char *local request bytes, size_t len, httpp_req_t *out)`
- **Documentation:** [API reference](<https://github.com/cebem1nt/httpp#api>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
