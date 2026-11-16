# archive-core — ZIP / Rust

- **Pinned release:** `0.1.6`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed text
- **Underlying family:** zip-forensic-core engine
- **Local input API:** `Archive::open(&[u8], Some("hello.zip")).entries(); read(0)`
- **Documentation:** [API reference](<https://docs.rs/archive-core/0.1.6/archive_core/>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/rust/archive_core/README.md)

```sh
python3 parsarium.py build zip rust archive_core
python3 parsarium.py run zip rust archive_core controls/zip/hello.zip
```
