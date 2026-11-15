# code.cloudfoundry.org/ykk — ZIP / Go

- **Pinned release:** `v0.0.0-20170424192843-e4df4ce2fd4d`
- **License:** Apache-2.0
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `NewReader(io.ReadSeeker+io.ReaderAt,size); zip.Reader.File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/code.cloudfoundry.org/ykk@v0.0.0-20170424192843-e4df4ce2fd4d>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

Wrapper over Go archive/zip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
