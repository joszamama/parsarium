# tika-parser-pkg-module — ZIP / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Apache Tika ZipParser over Commons Compress
- **Local input API:** `new ZipParser().parse(TikaInputStream.get(path), handler, metadata, context)`
- **Documentation:** [API reference](<https://tika.apache.org/4.2.0/api/org/apache/tika/parser/pkg/ZipParser.html>)
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
