# github.com/sourcegraph/lazyzip — ZIP / Go

- **Pinned release:** `v0.0.0-20180104141618-672a4b512c09`
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip fork
- **Local input API:** `OpenReader(path); Reader.Next(); File.Open()`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/sourcegraph/lazyzip@v0.0.0-20180104141618-672a4b512c09>)
- **Catalog evidence:** [parser record](../../../../data/go/zip/parsers.json) · [control verification](../../../../data/go/zip/verification.json) · [within-ecosystem ranking](../../../../data/go/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

Shared underlying parser lineage or wrapper; package count is not an independent engine count.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
