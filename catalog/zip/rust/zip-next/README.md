# zip_next — ZIP / Rust

- **Pinned release:** `1.1.1`
- **License:** MIT
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** zip-rs lineage
- **Local input API:** `ZipArchive::new(Cursor<&[u8]>).by_index(0).read_to_string()`
- **Documentation:** [API reference](<https://docs.rs/zip_next/1.1.1/zip_next/>)
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
