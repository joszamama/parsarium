# zip — ZIP / Rust

- **Pinned release:** `9.5.1`
- **Upstream:** [source repository](<https://github.com/zip-rs/zip2>) · [crates.io](<https://crates.io/crates/zip>)
- **License:** MIT
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** zip-rs lineage
- **Local input API:** `ZipArchive::new(Cursor<&[u8]>).by_index(0).read_to_string()`
- **Documentation:** [API reference](<https://docs.rs/zip/9.5.1/zip/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/zip/README.md)

```sh
python3 parsarium.py build zip rust zip
python3 parsarium.py run zip rust zip controls/zip/hello.zip
```
