# sutegi-http — HTTP/1.1 / Rust

- **Pinned release:** `0.13.0`
- **License:** MIT
- **Parsed scope:** request: method, path, query, version
- **Underlying family:** sutegi-http
- **Local input API:** `parse_request(&mut BufReader<Cursor<&[u8]>>, &Limits)`
- **Documentation:** [API reference](<https://docs.rs/sutegi-http/0.13.0/sutegi_http/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium",
  "query": "x=1",
  "version": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
