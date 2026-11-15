# github.com/codeclysm/extract/v4 — ZIP / Go

- **Pinned release:** `v4.0.2`
- **License:** MIT
- **Parsed scope:** entry_name+decompressed_text
- **Underlying family:** Go archive/zip wrapper
- **Local input API:** `Zip(context,io.Reader,destination,nil)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/codeclysm/extract/v4@v4.0.2>)
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
