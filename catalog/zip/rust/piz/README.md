# piz — ZIP / Rust

- **Pinned release:** `0.5.1`
- **License:** Zlib
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** piz engine
- **Local input API:** `ZipArchive::new(&[u8]).entries(); archive.read(entry)`
- **Documentation:** [API reference](<https://docs.rs/piz/0.5.1/piz/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/piz/README.md)

```sh
python3 parsarium.py build zip rust piz
python3 parsarium.py run zip rust piz controls/zip/hello.zip
```
