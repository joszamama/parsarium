# tinyzip — ZIP / Rust

- **Pinned release:** `0.4.0`
- **License:** MIT
- **Parsed scope:** Entry name and externally DEFLATE-decoded text
- **Underlying family:** tinyzip engine
- **Local input API:** `Archive::try_from(File).find_file(b"hello.txt").reader()`
- **Documentation:** [API reference](<https://docs.rs/tinyzip/0.4.0/tinyzip/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/tinyzip/README.md)

```sh
python3 parsarium.py build zip rust tinyzip
python3 parsarium.py run zip rust tinyzip controls/zip/hello.zip
```
