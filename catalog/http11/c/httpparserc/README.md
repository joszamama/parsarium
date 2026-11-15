# HTTPParserC — HTTP/1.1 / C

- **Pinned release:** `9.2.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse
- **Underlying family:** Building42 packaged llhttp 9.2.0 generated C source; shares the llhttp engine and is a separate versioned distribution
- **Local input API:** `Bundled llhttp_init(..., LLHTTP_REQUEST, ...); llhttp_execute(llhttp_t *, local request bytes, length); on_url and on_headers_complete callbacks`
- **Documentation:** [API reference](<https://github.com/Building42/HTTPParserC#documentation>)
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
