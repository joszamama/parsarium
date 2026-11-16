# zip-extract — ZIP / Rust

- **Pinned release:** `0.4.1`
- **License:** MIT
- **Parsed scope:** Extracted entry name and text
- **Underlying family:** zip-rs lineage
- **Local input API:** `extract(Cursor<&[u8]>, destination, false)`
- **Documentation:** [API reference](<https://docs.rs/zip-extract/0.4.1/zip_extract/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/zip_extract/README.md)

```sh
python3 parsarium.py build zip rust zip_extract
python3 parsarium.py run zip rust zip_extract controls/zip/hello.zip
```
