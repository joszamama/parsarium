# truevfs-driver-zip — ZIP / Java

- **Pinned release:** `0.14.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** TrueVFS ZIP driver (TrueZIP successor family)
- **Local input API:** `new TFile(zipFile, entryName); new TFileInputStream(entry); TVFS.umount()`
- **Documentation:** [API reference](<https://truevfs.namespace.global/kick-start/tutorial.html>)
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
