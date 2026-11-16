# libarchive2 — ZIP / Rust

- **Pinned release:** `0.2.1`
- **License:** BSD-2-Clause
- **Parsed scope:** ZIP entry name and decompressed text
- **Underlying family:** libarchive native engine
- **Local input API:** `ReadArchive::open(path).next_entry(); read_data_to_vec()`
- **Documentation:** [API reference](<https://docs.rs/libarchive2/0.2.1/libarchive2/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/libarchive2/README.md)

```sh
python3 parsarium.py build zip rust libarchive2
python3 parsarium.py run zip rust libarchive2 controls/zip/hello.zip
```
