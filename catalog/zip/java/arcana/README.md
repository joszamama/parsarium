# arcana — ZIP / Java

- **Pinned release:** `1.1.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Arcana own ZIP parser
- **Local input API:** `Arcana.read(file); ArchiveReader iteration and ArchiveItem.openStream()`
- **Documentation:** [API reference](<https://realburst.github.io/arcana/>)
- **Catalog evidence:** [parser record](../../../../data/java/zip/parsers.json) · [control verification](../../../../data/java/zip/verification.json) · [within-ecosystem ranking](../../../../data/java/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/java/arcana/README.md)

```sh
python3 parsarium.py build zip java arcana
python3 parsarium.py run zip java arcana controls/zip/hello.zip
```
