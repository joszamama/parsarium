# eazip — ZIP / Rust

- **Pinned release:** `0.2.7`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** eazip engine
- **Local input API:** `ArchiveReader::open(path).get_by_index(0).read()`
- **Documentation:** [API reference](<https://docs.rs/crate/eazip/0.2.7/source/src/lib.rs>)
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
