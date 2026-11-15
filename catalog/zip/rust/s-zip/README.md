# s-zip — ZIP / Rust

- **Pinned release:** `0.15.0`
- **License:** MIT
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** s-zip engine
- **Local input API:** `StreamingZipReader::open(path).entries(); read_entry_by_name(name)`
- **Documentation:** [API reference](<https://docs.rs/s-zip/0.15.0/s_zip/>)
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
