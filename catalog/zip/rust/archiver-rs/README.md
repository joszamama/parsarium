# archiver-rs — ZIP / Rust

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** ZIP entry name and count
- **Underlying family:** zip-rs lineage
- **Local input API:** `Zip::new(Cursor<&[u8]>).files()`
- **Documentation:** [API reference](<https://docs.rs/archiver-rs/0.5.1/archiver_rs/struct.Zip.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/zip/parsers.json) · [control verification](../../../../data/rust/zip/verification.json) · [within-ecosystem ranking](../../../../data/rust/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "entry_count": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
