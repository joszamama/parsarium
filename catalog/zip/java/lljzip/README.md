# lljzip — ZIP / Java

- **Pinned release:** `2.1.0`
- **License:** MIT
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** LLJZip own ZIP reader
- **Local input API:** `software.coley.lljzip.ZipIO.readJvm(path); archive.getLocalFileByName(name)`
- **Documentation:** [API reference](<https://github.com/Col-E/LL-Java-Zip/blob/2.1.0/README.md>)
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
