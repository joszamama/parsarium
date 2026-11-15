# oxiarc-archive — ZIP / Rust

- **Pinned release:** `0.4.2`
- **License:** Apache-2.0
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** OxiArc ZIP engine
- **Local input API:** `zip::read_zip(Cursor<&[u8]>).entries(); extract(entry)`
- **Documentation:** [API reference](<https://docs.rs/oxiarc-archive/0.4.2/oxiarc_archive/>)
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
