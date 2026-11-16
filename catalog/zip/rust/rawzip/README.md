# rawzip — ZIP / Rust

- **Pinned release:** `0.5.2`
- **License:** MIT
- **Parsed scope:** Entry name and externally DEFLATE-decoded text
- **Underlying family:** rawzip engine
- **Local input API:** `ZipArchive::from_slice(&[u8]).entries().next_entry(); get_entry().verifying_reader()`
- **Documentation:** [API reference](<https://docs.rs/rawzip/0.5.2/rawzip/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/rawzip/README.md)

```sh
python3 parsarium.py build zip rust rawzip
python3 parsarium.py run zip rust rawzip controls/zip/hello.zip
```
