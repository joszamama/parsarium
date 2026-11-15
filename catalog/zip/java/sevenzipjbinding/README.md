# sevenzipjbinding — ZIP / Java

- **Pinned release:** `23.01-2.2`
- **License:** LGPL-2.1
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** 7-Zip C++ archive parser via JNI
- **Local input API:** `SevenZip.openInArchive(ArchiveFormat.ZIP, new RandomAccessFileInStream(file)); item.extractSlow(output)`
- **Documentation:** [API reference](<https://sevenzipjbind.sourceforge.net/snippets/index.html>)
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
