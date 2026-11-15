# commons-vfs2 — ZIP / Java

- **Pinned release:** `2.10.0`
- **License:** Apache-2.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** Commons VFS ZIP provider over JDK ZipFile
- **Local input API:** `VFS.getManager().resolveFile("zip:" + fileUri + "!/hello.txt"); getContent().getInputStream()`
- **Documentation:** [API reference](<https://commons.apache.org/proper/commons-vfs/filesystems.html>)
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
