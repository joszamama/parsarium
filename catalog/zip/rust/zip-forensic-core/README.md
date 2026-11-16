# zip-forensic-core — ZIP / Rust

- **Pinned release:** `0.2.3`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed text
- **Underlying family:** zip-forensic-core engine
- **Local input API:** `ZipArchive::new(Cursor<&[u8]>).file_names(); by_index(0).read_to_string()`
- **Documentation:** [API reference](<https://docs.rs/zip-forensic-core/0.2.3/zip_core/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/zip_forensic_core/README.md)

```sh
python3 parsarium.py build zip rust zip_forensic_core
python3 parsarium.py run zip rust zip_forensic_core controls/zip/hello.zip
```
