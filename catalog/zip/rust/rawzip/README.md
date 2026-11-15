# rawzip — ZIP / Rust

- **Pinned release:** `0.5.2`
- **License:** MIT
- **Parsed scope:** Entry name and externally DEFLATE-decoded text
- **Underlying family:** rawzip engine
- **Local input API:** `ZipArchive::from_slice(&[u8]).entries().next_entry(); get_entry().verifying_reader()`
- **Documentation:** [API reference](<https://docs.rs/rawzip/0.5.2/rawzip/>)
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
