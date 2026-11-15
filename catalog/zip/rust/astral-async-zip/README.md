# astral_async_zip — ZIP / Rust

- **Pinned release:** `0.0.22`
- **License:** MIT
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** rs-async-zip lineage
- **Local input API:** `base::read::mem::ZipFileReader::new(Vec<u8>).reader_with_entry(0)`
- **Documentation:** [API reference](<https://docs.rs/astral_async_zip/0.0.22/async_zip/>)
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
