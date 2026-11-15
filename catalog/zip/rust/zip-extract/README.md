# zip-extract — ZIP / Rust

- **Pinned release:** `0.4.1`
- **License:** MIT
- **Parsed scope:** Extracted entry name and text
- **Underlying family:** zip-rs lineage
- **Local input API:** `extract(Cursor<&[u8]>, destination, false)`
- **Documentation:** [API reference](<https://docs.rs/zip-extract/0.4.1/zip_extract/>)
- **Catalog evidence:** [parser record](../../../../data/rust/zip/parsers.json) · [control verification](../../../../data/rust/zip/verification.json) · [within-ecosystem ranking](../../../../data/rust/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content": "parsarium\n",
  "size": 10
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
