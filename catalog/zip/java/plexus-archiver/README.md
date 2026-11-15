# plexus-archiver — ZIP / Java

- **Pinned release:** `4.15.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Plexus Archiver wrapper over Commons Compress
- **Local input API:** `new ZipUnArchiver(file).setDestDirectory(dir); extract()`
- **Documentation:** [API reference](<https://codehaus-plexus.github.io/plexus-archiver/apidocs/org/codehaus/plexus/archiver/zip/ZipUnArchiver.html>)
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
