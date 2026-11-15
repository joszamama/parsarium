# rc-zip-sync — ZIP / Rust

- **Pinned release:** `4.4.2`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** rc-zip engine
- **Local input API:** `ReadZip::read_zip(Vec<u8>).entries().next().bytes()`
- **Documentation:** [API reference](<https://docs.rs/rc-zip-sync/4.4.2/rc_zip_sync/>)
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
