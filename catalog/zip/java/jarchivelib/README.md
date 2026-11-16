# jarchivelib — ZIP / Java

- **Pinned release:** `1.2.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** JArchiveLib wrapper over Commons Compress
- **Local input API:** `ArchiverFactory.createArchiver(ArchiveFormat.ZIP).stream(file); getNextEntry()`
- **Documentation:** [API reference](<https://github.com/thrau/jarchivelib>)
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

[Docker harness and verification receipt](../../../../projects/zip/java/jarchivelib/README.md)

```sh
python3 parsarium.py build zip java jarchivelib
python3 parsarium.py run zip java jarchivelib controls/zip/hello.zip
```
