# zt-zip — ZIP / Java

- **Pinned release:** `1.18.2`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** zt-zip wrapper over JDK ZipFile
- **Local input API:** `org.zeroturnaround.zip.ZipUtil.iterate(file, ZipEntryCallback)`
- **Documentation:** [API reference](<https://github.com/zeroturnaround/zt-zip>)
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
