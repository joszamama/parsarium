# zip4j — ZIP / Java

- **Pinned release:** `2.11.6`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** zip4j ZIP parser
- **Local input API:** `new net.lingala.zip4j.ZipFile(file).getFileHeader(name); getInputStream(header)`
- **Documentation:** [API reference](<https://github.com/srikanth-lingala/zip4j>)
- **Catalog evidence:** [parser record](../../../../data/java/zip/parsers.json) · [control verification](../../../../data/java/zip/verification.json) · [within-ecosystem ranking](../../../../data/java/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
