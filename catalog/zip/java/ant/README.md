# ant — ZIP / Java

- **Pinned release:** `1.10.18`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Apache Ant ZIP reader; historically related to Commons Compress
- **Local input API:** `new org.apache.tools.zip.ZipFile(file).getEntry(name); getInputStream(entry)`
- **Documentation:** [API reference](<https://ant.apache.org/manual/api/org/apache/tools/zip/ZipFile.html>)
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
