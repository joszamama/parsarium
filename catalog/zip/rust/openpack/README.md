# openpack — ZIP / Rust

- **Pinned release:** `0.2.7`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** zip-rs lineage
- **Local input API:** `OpenPack::open_default(path).entries(); read_entry(name)`
- **Documentation:** [API reference](<https://docs.rs/openpack/0.2.7/openpack/>)
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
