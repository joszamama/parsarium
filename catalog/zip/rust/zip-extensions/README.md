# zip-extensions — ZIP / Rust

- **Pinned release:** `0.14.1`
- **Upstream:** [source repository](<https://github.com/matzefriedrich/zip-extensions-rs>) · [crates.io](<https://crates.io/crates/zip-extensions>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/rust/zip_extensions/README.md)

```sh
python3 parsarium.py build zip rust zip_extensions
python3 parsarium.py run zip rust zip_extensions controls/zip/hello.zip
```
