# truezip-driver-zip — ZIP / Java

- **Pinned release:** `7.7.10`
- **License:** EPL-1.0
- **Parsed scope:** ZIP entry name and decompressed content from a local archive
- **Underlying family:** TrueZIP ZIP driver
- **Local input API:** `new TFileInputStream(new TFile(zipFile, entryName))`
- **Documentation:** [API reference](<https://christian-schlichtherle.bitbucket.io/truezip/apidocs/de/schlichtherle/truezip/file/TFileInputStream.html>)
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
