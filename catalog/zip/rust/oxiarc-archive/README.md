# oxiarc-archive — ZIP / Rust

- **Pinned release:** `0.4.2`
- **License:** Apache-2.0
- **Parsed scope:** Entry name and decompressed text
- **Underlying family:** OxiArc ZIP engine
- **Local input API:** `zip::read_zip(Cursor<&[u8]>).entries(); extract(entry)`
- **Documentation:** [API reference](<https://docs.rs/oxiarc-archive/0.4.2/oxiarc_archive/>)
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

[Docker harness and verification receipt](../../../../projects/zip/rust/oxiarc_archive/README.md)

```sh
python3 parsarium.py build zip rust oxiarc_archive
python3 parsarium.py run zip rust oxiarc_archive controls/zip/hello.zip
```
