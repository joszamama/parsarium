# compress4j — ZIP / Java

- **Pinned release:** `5.1.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Compress4J wrapper over Commons Compress
- **Local input API:** `ZipArchiveExtractor.builder(path).build().stream(); ArchiveItem.content()`
- **Documentation:** [API reference](<https://github.com/hominux/compress4j>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/compress4j/README.md)

```sh
python3 parsarium.py build zip java compress4j
python3 parsarium.py run zip java compress4j controls/zip/hello.zip
```
