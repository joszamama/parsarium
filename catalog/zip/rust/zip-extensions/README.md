# zip-extensions — ZIP / Rust

- **Pinned release:** `0.14.1`
- **License:** MIT
- **Parsed scope:** Decompressed named ZIP entry
- **Underlying family:** zip-rs lineage
- **Local input API:** `inflate::zip_extract::zip_extract_file_to_memory(path, entry_path, &mut Vec<u8>)`
- **Documentation:** [API reference](<https://docs.rs/zip-extensions/0.14.1/zip_extensions/>)
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
