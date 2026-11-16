# zip_structs — ZIP / Rust

- **Pinned release:** `0.2.1`
- **License:** MIT
- **Parsed scope:** ZIP local-header entry name and declared size
- **Underlying family:** zip_structs header reader
- **Local input API:** `ZipLocalFileHeader::read_and_generate_from_signature(&mut Cursor<&[u8]>)`
- **Documentation:** [API reference](<https://docs.rs/zip_structs/0.2.1/zip_structs/zip_local_file_header/>)
- **Catalog evidence:** [parser record](../../../../data/rust/zip/parsers.json) · [control verification](../../../../data/rust/zip/verification.json) · [within-ecosystem ranking](../../../../data/rust/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content": null,
  "size": 10
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/rust/zip_structs/README.md)

```sh
python3 parsarium.py build zip rust zip_structs
python3 parsarium.py run zip rust zip_structs controls/zip/hello.zip
```
