# github.com/daaku/go.zipexe — ZIP / Go

- **Pinned release:** `v1.0.2`
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `OpenCloser(path); zip.Reader.File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/daaku/go.zipexe@v1.0.2>)
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
